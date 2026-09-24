#!/usr/bin/env python3
"""Retrieve a current source for a run and write a hash-bound research evidence record.

Usage:
  research_fetch.py <run-dir> --init [--force]
  research_fetch.py <run-dir> --id EV1 --url <url> --kind legal-authority|client-fact|link-destination|statistic|other
                    --excerpt "<verbatim text that must appear on the page>"
                    [--source-id S1] [--authority "Wis. Stat. § 767.001"] [--jurisdiction Wisconsin]
                    [--legislation-status effective|enacted-not-effective|proposed|repealed|superseded|unknown]
                    [--current-through-date YYYY-MM-DD] [--effective-date YYYY-MM-DD] [--future-effective-date YYYY-MM-DD]
                    (--currency-marker "<the page's own current-through / published / effective statement>" | --no-currency-marker "<why the page states none>")
                    [--amendments "<note>"] [--supports C1 C2 ...] [--notes "..."] [--force]

`--init` issues the run's research nonce and opening time in run.json. Every record written afterwards
carries that nonce; the readiness check treats a record with another nonce, or retrieved before the
opening time, as reused evidence and refuses it. `--force` on `--init` rotates the nonce and thereby
invalidates every existing record for the run (say so in the coordinator log).

A record is written only when the page was actually fetched now with HTTP 200 and the named excerpt
(and currency marker, when given) is present in the extracted text. Nothing is written otherwise, so a
record can never be produced from memory, from a saved note, or from an earlier run. The extracted
text is saved beside the record and hashed into it so reviewers' quoted excerpts can be checked
against what was retrieved.

Reserved and fixture hosts (.example, .test, example.com, ...) are never fetched. A fixture run
(run.json fixture: true) may map such a prefix to a local test server with CW_FIXTURE_URL_REWRITE;
a real run ignores that variable.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cw_common as cw  # noqa: E402
import cw_research as rs  # noqa: E402


def init_research(run_dir: Path, *, force: bool = False) -> dict:
    run_path = run_dir / "run.json"
    run = cw.load_json(run_path)
    if rs.research_block(run) and not force:
        raise SystemExit(f"REFUSED: {run_path} already has a research block (opened {rs.research_block(run).get('opened_at')}); use --force only to rotate the nonce, which invalidates every existing record")
    if rs.research_dir(run_dir).is_dir() and any(rs.research_files(run_dir)) and force:
        print("NOTE: rotating the nonce; every existing research record in this run is now reused evidence and must be re-fetched")
    run["research"] = rs.new_research_block()
    cw.dump_json(run_path, run)
    rs.research_dir(run_dir).mkdir(exist_ok=True)
    return run["research"]


def fetch_and_record(run_dir: Path, *, evidence_id: str, url: str, kind: str, excerpt: str | None, source_id: str | None, authority: str | None, jurisdiction: str | None, legislation_status: str | None, effective_date: str | None, future_effective_date: str | None, currency_marker: str | None, amendments: str | None, supports: list[str], notes: str | None, force: bool, current_through_date: str | None = None, marker_absent_reason: str | None = None) -> dict:
    run = cw.load_json(run_dir / "run.json")
    problems = rs.research_block_problems(run)
    if problems:
        raise SystemExit("REFUSED: " + "; ".join(problems))
    if not rs.EVIDENCE_ID_RE.match(evidence_id):
        raise SystemExit("REFUSED: --id must match EV<n> (EV1, EV2, ...)")
    if kind not in rs.RESEARCH_KINDS:
        raise SystemExit(f"REFUSED: --kind must be one of {rs.RESEARCH_KINDS}")
    target = rs.research_dir(run_dir) / f"{evidence_id}.json"
    if target.exists() and not force:
        raise SystemExit(f"REFUSED: {target} exists; choose another id or pass --force to re-fetch and supersede it")
    if kind != "link-destination" and len(cw.norm_ws(excerpt or "")) < rs.MIN_EXCERPT_CHARS:
        raise SystemExit(f"REFUSED: --excerpt must quote at least {rs.MIN_EXCERPT_CHARS} characters of the page; a fetch without a checkable excerpt is not evidence")
    if kind == "legal-authority":
        if legislation_status not in rs.LEGISLATION_STATUSES:
            raise SystemExit(f"REFUSED: a legal authority needs --legislation-status from {rs.LEGISLATION_STATUSES}")
        if not cw.norm_ws(jurisdiction or "") or not cw.norm_ws(authority or ""):
            raise SystemExit("REFUSED: a legal authority needs --jurisdiction and --authority")
        if legislation_status == "enacted-not-effective" and not future_effective_date:
            raise SystemExit("REFUSED: enacted-not-effective law needs --future-effective-date")
        for label, value in (("--effective-date", effective_date), ("--future-effective-date", future_effective_date), ("--current-through-date", current_through_date)):
            if value and rs.parse_date(value) is None:
                raise SystemExit(f"REFUSED: {label} must be an ISO date")
        if len(cw.norm_ws(currency_marker or "")) < 20 and len(cw.norm_ws(marker_absent_reason or "")) < 20:
            raise SystemExit("REFUSED: a legal authority needs --currency-marker (the page's own current-through, published, or effective statement, 20+ characters) or --no-currency-marker \"<why the page states none>\" (20+ characters); an operator-typed status bound to nothing on the page is not currency evidence")
        if currency_marker and marker_absent_reason:
            raise SystemExit("REFUSED: give either --currency-marker or --no-currency-marker, not both")
        if currency_marker and excerpt and rs.excerpt_overlaps_marker(excerpt, currency_marker):
            raise SystemExit("REFUSED: the excerpt is the currency marker (or part of it); quote the operative text of the authority")
    if source_id and not any(s.get("id") == source_id for s in run.get("sources") or []):
        raise SystemExit(f"REFUSED: --source-id {source_id} is not declared in run.json sources")
    result = rs.fetch(url, run)
    if not result.ok:
        raise SystemExit(f"REFUSED: retrieval failed for {url}: {result.error or result.status}. Nothing was recorded; the source is unavailable now and the affected claims are unverified")
    text, extraction = rs.body_to_text(result.body, result.content_type)
    if extraction == "unsupported" or not text.strip():
        raise SystemExit(f"REFUSED: {url} returned {result.content_type or 'unknown content'} that yields no text; retrieve the HTML or text page that carries the authority")
    if kind != "link-destination" and not rs.excerpt_present(excerpt or "", text):
        raise SystemExit("REFUSED: the excerpt is not present in the page text retrieved just now. Nothing was recorded. Quote the page as it reads today, or treat the claim as unverified")
    if currency_marker and not rs.excerpt_present(currency_marker, text):
        raise SystemExit("REFUSED: the currency marker is not present in the page text retrieved just now; copy the page's own current-through or effective-date statement")
    if kind == "legal-authority" and not rs.section_token_present(authority or "", text):
        raise SystemExit(f"REFUSED: no section identifier from {authority!r} appears on the page retrieved just now; the URL does not carry the cited section")
    if kind == "legal-authority" and amendments and not rs.excerpt_present(amendments, text):
        raise SystemExit("REFUSED: the --amendments note is not present in the page text retrieved just now; copy the section's own History line (the line after the '<section> History' marker), or omit it when the rendered window does not reach it")
    if kind == "link-destination" and (result.redirects != 0 or rs.canonical_url(result.final_url or result.fetched_url) != rs.canonical_url(result.fetched_url)):
        raise SystemExit(f"REFUSED: link destination {url} did not resolve directly (redirects={result.redirects}, final {result.final_url}); the page contract requires a direct HTTP 200")
    rs.research_dir(run_dir).mkdir(exist_ok=True)
    text_path = rs.research_dir(run_dir) / f"{evidence_id}.txt"
    if target.exists():
        stamp = cw.now_iso().replace(":", "")
        superseded = rs.research_dir(run_dir) / "superseded"
        superseded.mkdir(exist_ok=True)
        target.rename(superseded / f"{evidence_id}.{stamp}.json")
        if text_path.exists():
            text_path.rename(superseded / f"{evidence_id}.{stamp}.txt")
    text_path.write_text(text, encoding="utf-8")
    record = {
        "schema": rs.RESEARCH_SCHEMA,
        "evidence_id": evidence_id,
        "run_id": run.get("run_id"),
        "nonce": rs.research_block(run).get("nonce"),
        "fixture": bool(run.get("fixture", False)),
        "kind": kind,
        "source_id": source_id,
        "url": url,
        "fetched_url": result.fetched_url if result.rewritten else url,
        "final_url": result.final_url,
        "http_status": result.status,
        "redirects": result.redirects,
        "content_type": result.content_type,
        "retrieved_at": result.retrieved_at,
        "retrieval_method": "research_fetch.py (python urllib, live)",
        "content_sha256": cw.sha256_text(result.body.decode("utf-8", "replace")),
        "content_bytes": len(result.body),
        "text_extraction": extraction,
        "text_path": str(text_path.relative_to(run_dir)),
        "text_sha256": cw.sha256_file(text_path),
        "excerpt": cw.norm_ws(excerpt or "") if kind != "link-destination" else None,
        "authority": authority,
        "jurisdiction": jurisdiction,
        "currency": {
            "legislation_status": legislation_status,
            "current_through_date": current_through_date,
            "effective_date": effective_date,
            "future_effective_date": future_effective_date,
            "marker": cw.norm_ws(currency_marker or "") or None,
            "marker_absent_reason": cw.norm_ws(marker_absent_reason or "") or None,
            "amendments_note": amendments,
        } if kind == "legal-authority" else None,
        "supports_claims": supports or [],
        "notes": notes,
        "notice": "Retrieval evidence only: this record's metadata is consistent with the run's nonce and opening time, and the excerpt and marker were present in the page text stored beside it. It does not prove the page supports any claim (the legal reviewer's judgment), and declared jurisdiction and status are checked for consistency, not correctness.",
    }
    cw.dump_json(target, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--init", action="store_true", help="issue the run's research nonce and opening time")
    parser.add_argument("--id", dest="evidence_id")
    parser.add_argument("--url")
    parser.add_argument("--kind", choices=rs.RESEARCH_KINDS)
    parser.add_argument("--excerpt")
    parser.add_argument("--source-id")
    parser.add_argument("--authority")
    parser.add_argument("--jurisdiction")
    parser.add_argument("--legislation-status", choices=rs.LEGISLATION_STATUSES)
    parser.add_argument("--current-through-date", help="the compilation's current-through date stated on the page (legal authorities)")
    parser.add_argument("--effective-date", help="the provision's own effective date when the page states one; not the compilation date")
    parser.add_argument("--future-effective-date")
    parser.add_argument("--currency-marker")
    parser.add_argument("--no-currency-marker", dest="marker_absent_reason", help="legal authority only: why the page states no current-through or effective marker (20+ characters); recorded and printed in the ledger")
    parser.add_argument("--amendments")
    parser.add_argument("--supports", nargs="*", default=[])
    parser.add_argument("--notes")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    if args.init:
        block = init_research(run_dir, force=args.force)
        print(f"research opened for {run_dir.name} at {block['opened_at']} (nonce {block['nonce'][:8]}…, max age {block['max_age_days']} days)")
        return 0
    if not (args.evidence_id and args.url and args.kind):
        parser.error("--id, --url, and --kind are required unless --init is given")
    record = fetch_and_record(run_dir, evidence_id=args.evidence_id, url=args.url, kind=args.kind, excerpt=args.excerpt, source_id=args.source_id, authority=args.authority, jurisdiction=args.jurisdiction, legislation_status=args.legislation_status, effective_date=args.effective_date, future_effective_date=args.future_effective_date, currency_marker=args.currency_marker, amendments=args.amendments, supports=args.supports, notes=args.notes, force=args.force, current_through_date=args.current_through_date, marker_absent_reason=args.marker_absent_reason)
    print(f"recorded {record['evidence_id']} <- {record['url']} (HTTP {record['http_status']}, {record['content_bytes']} bytes, retrieved {record['retrieved_at']}, text sha256 {record['text_sha256'][:12]}…) -> research/{record['evidence_id']}.json")
    if record.get("currency"):
        c = record["currency"]
        print(f"  currency: declared {c['legislation_status']}; current through {c.get('current_through_date') or 'not stated'}; provision effective {c.get('effective_date') or 'not stated'}; marker {'present on page' if c.get('marker') else 'absent, reason recorded'}")
    print(f"  NOTICE: {record['notice']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
