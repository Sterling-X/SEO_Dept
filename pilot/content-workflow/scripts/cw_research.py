#!/usr/bin/env python3
"""Current-source research evidence for the content-workflow pilot (mechanical layer).

A run may rely on a legal authority, a client fact, or a link destination only if the page was
retrieved *during this run* and the retrieval left a checkable record under `<run>/research/`:

    research/EV1.json    the evidence record (schema content-workflow-research/v1)
    research/EV1.txt     the text extracted from the page at retrieval time (hashed in the record)

A record is written only by `scripts/research_fetch.py`, which refuses to write anything it did not
fetch, and only when the verbatim `excerpt` the operator names is present in the fetched text. Every
record carries the run's research nonce (issued once per run by `research_fetch.py --init`), so a
record copied from an earlier run, or written before this run opened, is detected as reused.

This module holds the shared, deterministic parts: URL handling, fetching, HTML-to-text extraction,
record validation, coverage rules, live re-verification, and the Verification-Log linkage that the
recorder and the gate both apply. Nothing here judges whether a source supports a claim; that is the
legal reviewer's recorded judgment. What this layer proves is narrower and mechanical: the page was
fetched in this run, the quoted text was on it, the run's currency declarations are present on the
page, and at delivery the page still says what was quoted. "Retrieved in this run" means the record's
nonce, run id, and retrieval time are consistent with the run's opening; the run directory is writable,
so this is consistency evidence, not authenticated provenance.
"""

from __future__ import annotations

import datetime as _dt
import html
import json
import os
import re
import secrets
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

import cw_common as cw

RESEARCH_SCHEMA = "content-workflow-research/v1"
EVIDENCE_ID_RE = re.compile(r"^EV[0-9]{1,3}$")
RESEARCH_KINDS = ("legal-authority", "client-fact", "link-destination", "statistic", "other")
LEGISLATION_STATUSES = ("effective", "enacted-not-effective", "proposed", "repealed", "superseded", "unknown")
MIN_EXCERPT_CHARS = 40
DEFAULT_MAX_AGE_DAYS = 14
MAX_MAX_AGE_DAYS = 30
NONCE_HEX_CHARS = 32
RESERVED_HOST_SUFFIXES = (".example", ".test", ".invalid", ".localhost", "example.com", "example.net", "example.org")
FIXTURE_REWRITE_ENV = "CW_FIXTURE_URL_REWRITE"
USER_AGENT = "SEO_Dept-content-workflow-research/1.0 (+https://github.com/Sterling-X/SEO_Dept)"
FETCH_TIMEOUT_SECONDS = 30
MAX_BODY_BYTES = 8 * 1024 * 1024
# Verification Log results that do not need retrieval evidence because no retrieval succeeded. They
# still block delivery through LEGAL_LOG_UNVERIFIED; the point is that they cannot be dressed as verified.
UNVERIFIED_RESULTS = ("unverifiable",)
JURISDICTION_NEUTRAL = ("federal", "united states")
SECTION_TOKEN_RE = re.compile(r"\d+(?:\.\d+)+[a-z]?|\b\d{1,4}\b")


# --------------------------------------------------------------------------- text handling

_QUOTE_MAP = str.maketrans({
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    " ": " ", " ": " ", " ": " ", " ": " ",
    "–": "-", "—": "-", "−": "-",
    "­": "",
})


def norm_match(text: str) -> str:
    """Normalization used for every excerpt comparison: NFC, straight quotes, plain spaces and hyphens,
    collapsed whitespace, casefold. Deliberately conservative: words and punctuation are preserved."""
    text = unicodedata.normalize("NFC", text or "").translate(_QUOTE_MAP)
    return re.sub(r"\s+", " ", text).strip().casefold()


def excerpt_present(excerpt: str, text: str) -> bool:
    needle = norm_match(excerpt)
    return bool(needle) and needle in norm_match(text)


class _TextExtractor(HTMLParser):
    _SKIP = {"script", "style", "noscript", "template", "svg"}
    _BLOCK = {"p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "td", "th", "table", "section", "article", "header", "footer", "nav", "main", "aside", "blockquote", "pre", "dd", "dt", "dl", "hr", "title", "body", "html", "head", "form", "fieldset", "legend", "label", "figure", "figcaption", "summary", "details"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag in self._BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1
        elif tag in self._BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self.parts.append(data)


def body_to_text(body: bytes, content_type: str) -> tuple[str, str]:
    """Return (text, extraction) where extraction is 'html', 'text', or 'unsupported'."""
    ctype = (content_type or "").lower()
    charset = "utf-8"
    match = re.search(r"charset=([\w-]+)", ctype)
    if match:
        charset = match.group(1)
    try:
        decoded = body.decode(charset, errors="replace")
    except LookupError:
        decoded = body.decode("utf-8", errors="replace")
    looks_html = "html" in ctype or bool(re.search(r"<\s*(html|body|div|p)\b", decoded[:4000], re.I))
    if looks_html:
        parser = _TextExtractor()
        parser.feed(decoded)
        parser.close()
        text = html.unescape("".join(parser.parts))
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n", text)
        return text.strip() + "\n", "html"
    if "text/" in ctype or "json" in ctype or "xml" in ctype or not ctype:
        return decoded, "text"
    return "", "unsupported"


# --------------------------------------------------------------------------- URLs and fetching


def is_reserved_host(url: str) -> bool:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    for suffix in RESERVED_HOST_SUFFIXES:
        bare = suffix.lstrip(".")
        if host == bare or host.endswith("." + bare):
            return True
    return False


def section_tokens(authority: str) -> list[str]:
    """Numeric identifiers in a citation. Dotted section numbers ('767.001', '61.13', '12.345') are preferred;
    bare numbers ('161', '7') are used only when the citation has no dotted token, because a bare digit
    appears on almost any page. This is a consistency check: a chapter table of contents or a neighbouring
    section that cross-references the cited number also passes it, so the legal reviewer's confirmation that
    the operative subsection is inside the stored text remains the real guard (open question 13)."""
    tokens = [tok for tok in SECTION_TOKEN_RE.findall(authority or "") if tok]
    dotted = [tok for tok in tokens if "." in tok]
    return dotted or tokens


def section_token_present(authority: str, text: str) -> bool:
    haystack = norm_match(text)
    tokens = section_tokens(authority)
    if not tokens:
        return True  # nothing numeric to bind; the excerpt rule still applies
    return any(re.search(r"(?<![\w.])" + re.escape(tok.casefold()) + r"(?![\w])", haystack) for tok in tokens)


def line_present(note: str, text: str) -> bool:
    """True when the note appears in the retrieved text and runs to the end of its line (used for the
    History / amendments line, which some sites render on the same line as a '<section> History'
    marker). A truncated prefix that stops mid-line is not accepted."""
    wanted = norm_match(note)
    return bool(wanted) and any(norm_match(line).endswith(wanted) for line in (text or "").splitlines())


def excerpt_overlaps_marker(excerpt: str, marker: str) -> bool:
    a, b = norm_match(excerpt), norm_match(marker)
    return bool(a and b) and (a in b or b in a)


def parse_rewrite_map(raw: str | None) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in (raw or "").split(";"):
        if "=" in item:
            prefix, replacement = item.split("=", 1)
            if prefix.strip() and replacement.strip():
                pairs.append((prefix.strip(), replacement.strip()))
    return pairs


def rewrite_url(url: str, run: dict) -> tuple[str, bool]:
    """Fixture runs only: map a reserved fixture URL prefix to a local test server. A real run never
    rewrites, so the environment variable cannot redirect real research to a stand-in page."""
    if not bool(run.get("fixture", False)):
        return url, False
    for prefix, replacement in parse_rewrite_map(os.environ.get(FIXTURE_REWRITE_ENV)):
        if url.startswith(prefix):
            return replacement + url[len(prefix):], True
    return url, False


def canonical_url(url: str) -> str:
    parts = urllib.parse.urlsplit((url or "").strip())
    path = parts.path or "/"
    return urllib.parse.urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


class _CountingRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        self.count += 1
        return super().redirect_request(req, fp, code, msg, headers, newurl)


@dataclass
class FetchResult:
    requested_url: str
    fetched_url: str
    final_url: str | None = None
    status: int | None = None
    redirects: int = 0
    content_type: str = ""
    body: bytes = b""
    error: str | None = None
    retrieved_at: str = field(default_factory=cw.now_iso)
    rewritten: bool = False

    @property
    def ok(self) -> bool:
        return self.error is None and self.status == 200


TRANSIENT_RETRIES = 1  # one extra attempt for timeouts and connection errors; never for an HTTP status


def fetch(url: str, run: dict, *, timeout: int = FETCH_TIMEOUT_SECONDS, retries: int = TRANSIENT_RETRIES) -> FetchResult:
    """Fetch once, retrying only a transient transport failure (timeout, reset, DNS) a bounded number of
    times. An HTTP error status, a reserved host, or an oversized body is final on the first attempt."""
    target, rewritten = rewrite_url(url, run)
    result = FetchResult(requested_url=url, fetched_url=target, rewritten=rewritten)
    if is_reserved_host(target):
        result.error = f"reserved or fixture host {urllib.parse.urlsplit(target).hostname!r} is not fetched; a fixture run must map it to a local test server with {FIXTURE_REWRITE_ENV}"
        return result
    attempts = 0
    while True:
        attempts += 1
        handler = _CountingRedirectHandler()
        opener = urllib.request.build_opener(handler)
        request = urllib.request.Request(target, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.5"})
        result.error = None
        transient = False
        try:
            with opener.open(request, timeout=timeout) as response:
                result.status = response.status
                result.final_url = response.geturl()
                result.content_type = response.headers.get("Content-Type", "")
                result.body = response.read(MAX_BODY_BYTES + 1)
                if len(result.body) > MAX_BODY_BYTES:
                    result.error = f"response larger than {MAX_BODY_BYTES} bytes"
        except urllib.error.HTTPError as error:
            result.status = error.code
            result.final_url = error.geturl()
            result.error = f"HTTP {error.code}"
            error.close()
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
            result.error = f"{type(error).__name__}: {getattr(error, 'reason', error)}"
            transient = True
        result.redirects = handler.count
        if transient and attempts <= retries:
            time.sleep(1.5 * attempts)
            continue
        if attempts > 1 and result.error:
            result.error += f" (after {attempts} attempts)"
        result.retrieved_at = cw.now_iso()
        return result


# --------------------------------------------------------------------------- records


def research_dir(run_dir: Path) -> Path:
    return run_dir / "research"


def research_files(run_dir: Path) -> list[Path]:
    folder = research_dir(run_dir)
    return sorted(folder.glob("EV*.json")) if folder.is_dir() else []


def load_records(run_dir: Path) -> list[tuple[Path, dict | None, str | None]]:
    out: list[tuple[Path, dict | None, str | None]] = []
    for path in research_files(run_dir):
        try:
            out.append((path, cw.load_json(path), None))
        except (OSError, json.JSONDecodeError) as error:
            out.append((path, None, f"unreadable ({error})"))
    return out


def parse_iso(value: str | None) -> _dt.datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        parsed = _dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=_dt.timezone.utc)
    return parsed


def parse_date(value: str | None) -> _dt.date | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return _dt.date.fromisoformat(value[:10])
    except ValueError:
        return None


def research_block(run: dict) -> dict:
    return run.get("research") if isinstance(run.get("research"), dict) else {}


def research_block_problems(run: dict) -> list[str]:
    block = research_block(run)
    problems: list[str] = []
    if not block:
        return ["run.json has no research block; run research_fetch.py <run> --init before any source is retrieved"]
    nonce = str(block.get("nonce") or "")
    if not re.fullmatch(r"[0-9a-f]{%d,}" % NONCE_HEX_CHARS, nonce):
        problems.append("research.nonce must be a hex string of at least 32 characters issued by research_fetch.py --init")
    if parse_iso(block.get("opened_at")) is None:
        problems.append("research.opened_at must be an ISO timestamp")
    max_age = block.get("max_age_days", DEFAULT_MAX_AGE_DAYS)
    if not isinstance(max_age, int) or not 1 <= max_age <= MAX_MAX_AGE_DAYS:
        problems.append(f"research.max_age_days must be an integer from 1 to {MAX_MAX_AGE_DAYS}")
    return problems


def max_age_days(run: dict) -> int:
    value = research_block(run).get("max_age_days", DEFAULT_MAX_AGE_DAYS)
    return min(int(value), MAX_MAX_AGE_DAYS) if isinstance(value, int) and value >= 1 else DEFAULT_MAX_AGE_DAYS


def new_research_block() -> dict:
    return {"nonce": secrets.token_hex(NONCE_HEX_CHARS // 2), "opened_at": cw.now_iso(), "opened_by": "research_fetch.py --init", "max_age_days": DEFAULT_MAX_AGE_DAYS}


def validate_record_shape(record: dict) -> list[str]:
    problems: list[str] = []
    if record.get("schema") != RESEARCH_SCHEMA:
        problems.append(f"schema must be {RESEARCH_SCHEMA}")
    if not EVIDENCE_ID_RE.match(str(record.get("evidence_id", ""))):
        problems.append("evidence_id must match EV<n>")
    if record.get("kind") not in RESEARCH_KINDS:
        problems.append(f"kind must be one of {RESEARCH_KINDS}")
    for key in ("run_id", "nonce", "url", "retrieved_at", "retrieval_method", "content_sha256", "text_path", "text_sha256"):
        if not record.get(key):
            problems.append(f"{key} is required")
    if record.get("http_status") != 200:
        problems.append("http_status must be 200 (a record is written only for a successful retrieval)")
    if parse_iso(record.get("retrieved_at")) is None:
        problems.append("retrieved_at must be an ISO timestamp")
    if record.get("kind") != "link-destination" and len(cw.norm_ws(str(record.get("excerpt") or ""))) < MIN_EXCERPT_CHARS:
        problems.append(f"excerpt of at least {MIN_EXCERPT_CHARS} characters is required; a timestamp alone is not retrieval evidence")
    if record.get("text_extraction") not in ("html", "text"):
        problems.append("text_extraction must be html or text")
    if record.get("kind") == "legal-authority":
        currency = record.get("currency") if isinstance(record.get("currency"), dict) else {}
        if currency.get("legislation_status") not in LEGISLATION_STATUSES:
            problems.append(f"currency.legislation_status must be one of {LEGISLATION_STATUSES}")
        if not cw.norm_ws(str(record.get("jurisdiction") or "")):
            problems.append("jurisdiction is required for a legal authority")
        if not cw.norm_ws(str(record.get("authority") or "")):
            problems.append("authority (the citation as the page names it) is required for a legal authority")
        marker = cw.norm_ws(str(currency.get("marker") or ""))
        reason = cw.norm_ws(str(currency.get("marker_absent_reason") or ""))
        if len(marker) < 20 and len(reason) < 20:
            problems.append("a legal authority needs currency.marker (the page's own current-through or effective statement, 20+ characters) or currency.marker_absent_reason (20+ characters) so its currency is bound to the page or its absence is declared")
        if marker and reason:
            problems.append("currency.marker and currency.marker_absent_reason are mutually exclusive")
        for key in ("current_through_date", "effective_date", "future_effective_date"):
            if currency.get(key) and parse_date(currency.get(key)) is None:
                problems.append(f"currency.{key} must be an ISO date")
    if record.get("kind") == "link-destination":
        fetched = str(record.get("fetched_url") or record.get("url") or "")
        final = str(record.get("final_url") or "")
        if record.get("redirects") != 0 or not final or canonical_url(final) not in {canonical_url(fetched), canonical_url(str(record.get("url") or ""))}:
            problems.append("a link destination must resolve directly (redirects recorded as 0 and a final URL equal to the cited URL)")
    return problems


def evidence_text(run_dir: Path, record: dict) -> tuple[str | None, str | None]:
    """Return (text, problem). The text file must exist and match the hash recorded at retrieval."""
    rel = str(record.get("text_path") or "")
    path = run_dir / rel
    if not rel or not path.is_file():
        return None, f"text file {rel!r} is missing"
    if cw.sha256_file(path) != record.get("text_sha256"):
        return None, f"text file {rel} changed after retrieval"
    return path.read_text(encoding="utf-8"), None


def _jurisdiction_matches(record_jurisdiction: str, run_jurisdiction: str) -> bool:
    a, b = norm_match(record_jurisdiction), norm_match(run_jurisdiction)
    return bool(a) and (a == b or a in JURISDICTION_NEUTRAL)


def research_problems(run_dir: Path, run: dict, *, now: _dt.datetime | None = None) -> tuple[list[tuple[str, str]], dict]:
    """Offline research checks. Returns (reasons, ledger). Reason tuples are (code, detail)."""
    reasons: list[tuple[str, str]] = []
    now = now or _dt.datetime.now(_dt.timezone.utc)
    ledger: dict = {"opened_at": research_block(run).get("opened_at"), "max_age_days": max_age_days(run), "records": [], "valid_ids": []}
    block_problems = research_block_problems(run)
    for problem in block_problems:
        reasons.append(("RESEARCH_NOT_OPENED", problem))
    block = research_block(run)
    opened_at = parse_iso(block.get("opened_at"))
    fixture_run = bool(run.get("fixture", False))
    valid: dict[str, dict] = {}
    seen_ids: set[str] = set()
    for path, record, load_error in load_records(run_dir):
        if record is None:
            reasons.append(("RESEARCH_INVALID", f"{path.name}: {load_error}"))
            continue
        problems = validate_record_shape(record)
        if problems:
            reasons.append(("RESEARCH_INVALID", f"{path.name}: " + "; ".join(problems)))
            continue
        eid = str(record["evidence_id"])
        if path.stem != eid:
            reasons.append(("RESEARCH_INVALID", f"{path.name}: file name does not match evidence_id {eid}"))
            continue
        if eid in seen_ids:
            reasons.append(("RESEARCH_INVALID", f"{path.name}: duplicate evidence_id {eid}"))
            continue
        seen_ids.add(eid)
        entry = {"evidence_id": eid, "kind": record.get("kind"), "url": record.get("url"), "final_url": record.get("final_url"), "retrieved_at": record.get("retrieved_at"), "http_status": record.get("http_status"), "jurisdiction": record.get("jurisdiction"), "authority": record.get("authority"), "currency": record.get("currency"), "supports_claims": record.get("supports_claims") or [], "source_id": record.get("source_id"), "excerpt": record.get("excerpt"), "content_sha256": record.get("content_sha256"), "valid": False}
        ledger["records"].append(entry)
        if bool(record.get("fixture", False)) != fixture_run:
            reasons.append(("FIXTURE_FLAG", f"{path.name}: record fixture={record.get('fixture', False)} but run fixture={fixture_run}"))
            continue
        if not block_problems and (record.get("nonce") != block.get("nonce") or record.get("run_id") != run.get("run_id")):
            reasons.append(("RESEARCH_REUSED", f"{path.name}: nonce or run_id does not belong to this run (evidence copied from another run or from before this run opened is not evidence for this run)"))
            continue
        retrieved = parse_iso(record.get("retrieved_at"))
        if opened_at and retrieved and retrieved < opened_at:
            reasons.append(("RESEARCH_REUSED", f"{path.name}: retrieved_at {record.get('retrieved_at')} predates research.opened_at {block.get('opened_at')}"))
            continue
        if retrieved and retrieved > now + _dt.timedelta(minutes=5):
            reasons.append(("RESEARCH_INVALID", f"{path.name}: retrieved_at is in the future"))
            continue
        if retrieved and (now - retrieved) > _dt.timedelta(days=max_age_days(run)):
            reasons.append(("RESEARCH_STALE", f"{path.name}: retrieved {record.get('retrieved_at')}, older than research.max_age_days={max_age_days(run)}; re-retrieve before relying on it"))
            continue
        text, text_problem = evidence_text(run_dir, record)
        if text is None:
            reasons.append(("RESEARCH_INVALID", f"{path.name}: {text_problem}"))
            continue
        if record.get("kind") != "link-destination" and not excerpt_present(str(record.get("excerpt")), text):
            reasons.append(("RESEARCH_INVALID", f"{path.name}: excerpt is not present in the retrieved text"))
            continue
        currency = record.get("currency") if isinstance(record.get("currency"), dict) else {}
        marker = cw.norm_ws(str(currency.get("marker") or ""))
        if marker and not excerpt_present(marker, text):
            reasons.append(("RESEARCH_INVALID", f"{path.name}: currency.marker is not present in the retrieved text"))
            continue
        if marker and record.get("kind") != "link-destination" and excerpt_overlaps_marker(str(record.get("excerpt")), marker):
            reasons.append(("RESEARCH_INVALID", f"{path.name}: the excerpt is the currency marker (or part of it); quote the operative text of the authority, not page chrome"))
            continue
        if record.get("kind") == "legal-authority":
            if not section_token_present(str(record.get("authority") or ""), text):
                reasons.append(("RESEARCH_INVALID", f"{path.name}: no section identifier from authority {record.get('authority')!r} appears in the retrieved text; the page is not the cited section"))
                continue
            if not _jurisdiction_matches(str(record.get("jurisdiction")), str(run.get("jurisdiction") or "")):
                reasons.append(("RESEARCH_JURISDICTION_MISMATCH", f"{path.name}: declared authority jurisdiction {record.get('jurisdiction')!r} is not the run's jurisdiction {run.get('jurisdiction')!r}"))
                continue
            status = currency.get("legislation_status")
            effective = parse_date(currency.get("effective_date"))
            current_through = parse_date(currency.get("current_through_date"))
            future = parse_date(currency.get("future_effective_date"))
            if status != "effective":
                reasons.append(("LEGISLATION_NOT_EFFECTIVE", f"{path.name}: declared legislation_status is {status!r}; only law in effect on the retrieval date may support a claim of current law"))
                continue
            if effective and retrieved and effective > retrieved.date():
                reasons.append(("LEGISLATION_NOT_EFFECTIVE", f"{path.name}: effective_date {currency.get('effective_date')} is after the retrieval date"))
                continue
            if current_through and retrieved and current_through > retrieved.date():
                reasons.append(("RESEARCH_INVALID", f"{path.name}: current_through_date {currency.get('current_through_date')} is after the retrieval date"))
                continue
            if future and retrieved and future <= retrieved.date():
                reasons.append(("RESEARCH_INVALID", f"{path.name}: future_effective_date {currency.get('future_effective_date')} is not in the future; declare the status that applies"))
                continue
        entry["valid"] = True
        valid[eid] = record
    ledger["valid_ids"] = sorted(valid)

    # Coverage: every legal authority and every citation needs current evidence; client facts need first-party evidence.
    by_url: dict[str, list[str]] = {}
    for eid, record in valid.items():
        for key in ("url", "final_url"):
            if record.get(key):
                by_url.setdefault(canonical_url(str(record[key])), []).append(eid)
    for source in run.get("sources") or []:
        kind, sid = source.get("kind"), source.get("id")
        if kind == "legal-authority":
            url = canonical_url(str(source.get("url") or ""))
            if not url or not any(valid[e].get("kind") == "legal-authority" for e in by_url.get(url, [])):
                reasons.append(("RESEARCH_MISSING", f"source {sid}: no valid legal-authority research record retrieved in this run for {source.get('url')}"))
        elif kind == "client-facts":
            ids = source.get("evidence_ids") or []
            if not isinstance(ids, list) or not ids:
                reasons.append(("RESEARCH_MISSING", f"source {sid}: client facts declare no evidence_ids; every changeable client claim needs a first-party page retrieved in this run"))
            else:
                for eid in ids:
                    if str(eid) not in valid or valid[str(eid)].get("kind") != "client-fact":
                        reasons.append(("RESEARCH_MISSING", f"source {sid}: evidence_id {eid} is not a valid client-fact research record in this run"))
    for citation in run.get("citations") or []:
        url = canonical_url(str(citation.get("url") or ""))
        if not url or not any(valid[e].get("kind") == "legal-authority" for e in by_url.get(url, [])):
            reasons.append(("RESEARCH_MISSING", f"citation [{citation.get('id')}]: no valid legal-authority research record for {citation.get('url')}"))
    for destination in run.get("link_destinations") or []:
        url = canonical_url(str(destination or ""))
        if not url or not any(valid[e].get("kind") == "link-destination" for e in by_url.get(url, [])):
            reasons.append(("RESEARCH_MISSING", f"link destination {destination}: no valid link-destination research record (direct HTTP 200, zero redirects) retrieved in this run"))
    return reasons, ledger


def research_live_problems(run_dir: Path, run: dict, ledger: dict) -> list[tuple[str, str]]:
    """Re-fetch every valid record's URL now. The current page must be reachable and still contain the
    recorded excerpt and currency marker; otherwise the authority changed or is unavailable."""
    reasons: list[tuple[str, str]] = []
    records = {r["evidence_id"]: r for r in ledger.get("records", []) if r.get("valid")}
    on_disk = {str(rec.get("evidence_id")): rec for _p, rec, _e in load_records(run_dir) if rec}
    for eid, entry in records.items():
        record = on_disk.get(eid) or {}
        result = fetch(str(record.get("url")), run)
        entry["live_checked_at"] = result.retrieved_at
        entry["live_status"] = result.status
        entry["live_error"] = result.error
        if not result.ok:
            reasons.append(("RESEARCH_UNAVAILABLE", f"{eid}: {record.get('url')} could not be re-verified live ({result.error or result.status}); the authority is unavailable now, so its currency is unknown"))
            continue
        text, extraction = body_to_text(result.body, result.content_type)
        entry["live_content_sha256"] = cw.sha256_text(result.body.decode("utf-8", "replace"))
        entry["changed_since_retrieval"] = entry["live_content_sha256"] != record.get("content_sha256")
        if extraction == "unsupported":
            reasons.append(("RESEARCH_UNAVAILABLE", f"{eid}: live response is not text ({result.content_type}); cannot confirm the excerpt"))
            continue
        if record.get("kind") != "link-destination" and not excerpt_present(str(record.get("excerpt")), text):
            reasons.append(("RESEARCH_EXCERPT_DRIFT", f"{eid}: the page at {record.get('url')} no longer contains the recorded excerpt; the authority or fact changed since retrieval and must be re-researched"))
            continue
        marker = cw.norm_ws(str(((record.get("currency") or {}).get("marker")) or ""))
        if marker and not excerpt_present(marker, text):
            reasons.append(("RESEARCH_EXCERPT_DRIFT", f"{eid}: the currency marker recorded for {record.get('url')} is no longer on the page; re-verify effective dates"))
            continue
        entry["live_verified"] = True
    return reasons


def legal_log_problems(run_dir: Path, run: dict, record: dict) -> list[str]:
    """Every Verification Log row that reports a verified result must point at a research record from
    this run and quote at least MIN_EXCERPT_CHARS characters that appear in that record's retrieved
    text. An access date before the run opened, or a row with no evidence, is not verification."""
    problems: list[str] = []
    rows = record.get("verification_log")
    if not isinstance(rows, list):
        return ["verification_log must be a list"]
    if not rows and record.get("stage") in ("predraft", "final", "checkpoint") and record.get("role") == "legal-reviewer":
        problems.append("a legal record needs at least one Verification Log row")
    valid_records = {str(rec.get("evidence_id")): rec for _p, rec, _e in load_records(run_dir) if rec and not validate_record_shape(rec)}
    block = research_block(run)
    opened = parse_iso(block.get("opened_at"))
    today = _dt.datetime.now(_dt.timezone.utc).date()
    for index, row in enumerate(rows):
        prefix = f"verification_log[{index}]"
        if not isinstance(row, dict):
            problems.append(f"{prefix} must be an object")
            continue
        result = str(row.get("result") or "").strip().lower()
        if not result:
            problems.append(f"{prefix}: result is required")
            continue
        if not cw.norm_ws(str(row.get("claim") or "")):
            problems.append(f"{prefix}: claim is required")
        accessed = parse_date(row.get("accessed"))
        if accessed is None:
            problems.append(f"{prefix}: accessed must be an ISO date (the actual retrieval date in this run)")
        else:
            if opened and accessed < opened.date():
                problems.append(f"{prefix}: accessed {row.get('accessed')} predates research.opened_at; a prior run's retrieval is not this run's verification")
            if accessed > today:
                problems.append(f"{prefix}: accessed {row.get('accessed')} is in the future")
        if result in UNVERIFIED_RESULTS:
            if len(cw.norm_ws(str(row.get("notes") or ""))) < 20:
                problems.append(f"{prefix}: an Unverifiable row must say in notes why retrieval failed")
            continue
        eid = str(row.get("evidence_id") or "")
        if not eid:
            problems.append(f"{prefix}: result {row.get('result')!r} needs evidence_id naming the research record retrieved in this run")
            continue
        evidence = valid_records.get(eid)
        if evidence is None:
            problems.append(f"{prefix}: evidence_id {eid} does not name a valid research record in this run")
            continue
        if evidence.get("nonce") != block.get("nonce") or evidence.get("run_id") != run.get("run_id"):
            problems.append(f"{prefix}: evidence {eid} belongs to another run")
            continue
        retrieved = parse_iso(evidence.get("retrieved_at"))
        if opened and retrieved and retrieved < opened:
            problems.append(f"{prefix}: evidence {eid} was retrieved before this run's research opened")
            continue
        if retrieved and (_dt.datetime.now(_dt.timezone.utc) - retrieved) > _dt.timedelta(days=max_age_days(run)):
            problems.append(f"{prefix}: evidence {eid} is older than research.max_age_days; re-retrieve before relying on it")
            continue
        row_url = canonical_url(str(row.get("url") or ""))
        record_urls = {canonical_url(str(evidence.get(k))) for k in ("url", "final_url") if evidence.get(k)}
        if row_url and row_url not in record_urls:
            problems.append(f"{prefix}: url {row.get('url')} is not the URL retrieved as {eid} ({evidence.get('url')})")
            continue
        excerpt = str(row.get("excerpt") or "")
        if len(cw.norm_ws(excerpt)) < MIN_EXCERPT_CHARS:
            problems.append(f"{prefix}: excerpt of at least {MIN_EXCERPT_CHARS} characters from the retrieved text is required for a {row.get('result')} row")
            continue
        text, text_problem = evidence_text(run_dir, evidence)
        if text is None:
            problems.append(f"{prefix}: {eid} {text_problem}")
            continue
        if not excerpt_present(excerpt, text):
            problems.append(f"{prefix}: excerpt is not in the text retrieved as {eid}; quote the page as retrieved in this run")
    return problems


def ledger_markdown(run: dict, ledger: dict, log_rows: list[dict]) -> str:
    """Human-readable research ledger for the hand-off: what was retrieved, when, its currency, and
    which logged claims rely on it."""
    lines = [f"# Research ledger: {run.get('run_id')}", "", f"Research opened: {ledger.get('opened_at')} (max age {ledger.get('max_age_days')} days). Each row is a research record whose metadata is consistent with this run's nonce and opening time, whose excerpt and currency marker were present in the stored page text, and whose page was re-fetched at the readiness check that produced this ledger. The ledger proves retrieval and consistency, not that a page supports a claim.", "", "| Evidence | Kind | Authority / page | URL | Retrieved (UTC) | Currency (declared status; page statement) | Live re-check | Claims supported |", "|---|---|---|---|---|---|---|---|"]
    supports: dict[str, list[str]] = {}
    seen_rows: set[tuple[str, str]] = set()
    for row in log_rows:
        eid = str(row.get("evidence_id") or "")
        key = (eid, cw.norm_ws(str(row.get("claim") or ""))[:80])
        if eid and key not in seen_rows:
            seen_rows.add(key)
            supports.setdefault(eid, []).append(key[1])
    for entry in ledger.get("records", []):
        currency = entry.get("currency") or {}
        currency_text = "; ".join(filter(None, [
            f"declared {currency.get('legislation_status')}" if currency.get("legislation_status") else None,
            f"current through {currency.get('current_through_date')}" if currency.get("current_through_date") else None,
            f"provision effective {currency.get('effective_date')}" if currency.get("effective_date") else None,
            f"future effective {currency.get('future_effective_date')}" if currency.get("future_effective_date") else None,
            currency.get("marker"),
            f"no page marker: {currency.get('marker_absent_reason')}" if currency.get("marker_absent_reason") else None,
        ])) if currency else "n/a"
        live = "verified" if entry.get("live_verified") else (entry.get("live_error") or f"status {entry.get('live_status')}" if entry.get("live_checked_at") else "not re-checked")
        if entry.get("live_verified") and entry.get("changed_since_retrieval"):
            live += " (page bytes changed; excerpt still present)"
        claims = supports.get(entry["evidence_id"]) or [", ".join(entry.get("supports_claims") or [])]
        lines.append(f"| {entry['evidence_id']} | {entry.get('kind')} | {cw.norm_ws(str(entry.get('authority') or ''))} | {entry.get('url')} | {entry.get('retrieved_at')} | {cw.norm_ws(currency_text)} | {live} | {' / '.join(c for c in claims if c)} |")
    lines += ["", "This ledger records retrieval and consistency facts; nonce, run id, and retrieval time are record metadata checked for consistency, not authenticated provenance. Declared jurisdiction and legislation status are checked for consistency with the run and the page's section identifier; their correctness, and whether a source supports a claim, are the legal reviewer's recorded judgment. Attorney review before publication remains required for legal content."]
    return "\n".join(lines) + "\n"
