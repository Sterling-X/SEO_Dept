#!/usr/bin/env python3
"""Crawl and compare Aurit's live and staging sites using only the Python stdlib.

The crawler discovers URLs from XML sitemaps and recursive same-origin HTML
links. It writes a machine-readable crawl record and a human-readable page map.
It does not submit forms or execute page JavaScript.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import datetime as dt
import difflib
import hashlib
import html
from html.parser import HTMLParser
import json
import re
import ssl
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


LIVE = "https://auritmediation.com"
STAGING = "https://stagingaurit.wpengine.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/141.0.0.0 Safari/537.36 AuritParityAudit/1.0"
)
SKIP_EXTENSIONS = {
    ".7z", ".avi", ".avif", ".bmp", ".css", ".csv", ".doc", ".docx",
    ".eot", ".epub", ".gif", ".gz", ".ico", ".jpeg", ".jpg", ".js",
    ".json", ".m4a", ".map", ".mov", ".mp3", ".mp4", ".mpeg", ".ogg",
    ".otf", ".pdf", ".png", ".ppt", ".pptx", ".rar", ".rss", ".svg",
    ".tar", ".tif", ".tiff", ".tsv", ".txt", ".wav", ".webm", ".webp",
    ".woff", ".woff2", ".xls", ".xlsx", ".xml", ".zip",
}
SKIP_PREFIXES = (
    "/wp-admin/", "/wp-json/", "/wp-login.php", "/xmlrpc.php",
)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def clean_space(value: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def normalize_text(value: str | None, *, replace_hosts: bool = True) -> str:
    value = unicodedata.normalize("NFKC", clean_space(value)).lower()
    value = value.replace("’", "'").replace("“", '"').replace("”", '"')
    if replace_hosts:
        value = value.replace("stagingaurit.wpengine.com", "auritmediation.com")
    return value


def slugify(value: str | None) -> str:
    value = normalize_text(value)
    value = re.sub(r"\b(?:aurit(?: center| mediation)?|arizona)\b", " ", value)
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def normalize_path(path: str) -> str:
    path = urllib.parse.unquote(path or "/")
    path = re.sub(r"/{2,}", "/", path)
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and not re.search(r"/[^/]+\.[a-z0-9]{1,8}$", path, re.I):
        path = path.rstrip("/") + "/"
    return path


def normalize_url(url: str, base: str) -> str | None:
    absolute = urllib.parse.urljoin(base + "/", url)
    parsed = urllib.parse.urlsplit(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    base_host = urllib.parse.urlsplit(base).hostname or ""
    host = (parsed.hostname or "").lower()
    if host.removeprefix("www.") != base_host.removeprefix("www."):
        return None
    path = normalize_path(parsed.path)
    if path.startswith(SKIP_PREFIXES):
        return None
    suffix = "." + path.rsplit(".", 1)[-1].lower() if "." in path.rsplit("/", 1)[-1] else ""
    if suffix in SKIP_EXTENSIONS:
        return None
    if path.endswith("/feed/") or path == "/feed/" or "/trackback/" in path:
        return None
    return urllib.parse.urlunsplit(("https", base_host, path, "", ""))


class RedirectTracker(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.chain: list[dict[str, object]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        self.chain.append({"from": req.full_url, "status": code, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


@dataclasses.dataclass
class FetchResult:
    requested_url: str
    final_url: str
    status: int | None
    headers: dict[str, str]
    body: bytes
    redirects: list[dict[str, object]]
    error: str | None
    elapsed_ms: int


def fetch(url: str, timeout: int = 25, attempts: int = 2) -> FetchResult:
    last: FetchResult | None = None
    for attempt in range(attempts):
        tracker = RedirectTracker()
        opener = urllib.request.build_opener(
            tracker,
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        )
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
            },
        )
        started = time.monotonic()
        try:
            with opener.open(request, timeout=timeout) as response:
                body = response.read(6_000_000)
                result = FetchResult(
                    requested_url=url,
                    final_url=response.geturl(),
                    status=response.status,
                    headers={k.lower(): v for k, v in response.headers.items()},
                    body=body,
                    redirects=tracker.chain,
                    error=None,
                    elapsed_ms=round((time.monotonic() - started) * 1000),
                )
        except urllib.error.HTTPError as exc:
            result = FetchResult(
                requested_url=url,
                final_url=exc.geturl(),
                status=exc.code,
                headers={k.lower(): v for k, v in exc.headers.items()},
                body=exc.read(2_000_000),
                redirects=tracker.chain,
                error=f"HTTP {exc.code}",
                elapsed_ms=round((time.monotonic() - started) * 1000),
            )
        except Exception as exc:  # Network failures are evidence and must be recorded.
            result = FetchResult(
                requested_url=url,
                final_url=url,
                status=None,
                headers={},
                body=b"",
                redirects=tracker.chain,
                error=f"{type(exc).__name__}: {exc}",
                elapsed_ms=round((time.monotonic() - started) * 1000),
            )
        last = result
        if result.status not in {None, 429, 500, 502, 503, 504}:
            return result
        if attempt + 1 < attempts:
            time.sleep(0.75 * (attempt + 1))
    assert last is not None
    return last


class PageParser(HTMLParser):
    SKIP_TEXT = {"script", "style", "noscript", "template", "svg", "canvas"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.description = ""
        self.canonical = ""
        self.meta_robots = ""
        self.lang = ""
        self.body_classes: list[str] = []
        self.headings: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.iframes: list[dict[str, str]] = []
        self.forms: list[dict[str, str]] = []
        self.visible_parts: list[str] = []
        self.jsonld_parts: list[str] = []
        self._in_title = False
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []
        self._in_body = False
        self._body_seen = False
        self._skip_depth = 0
        self._jsonld_depth = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs = {k.lower(): (v or "") for k, v in attrs_list}
        if tag == "html":
            self.lang = attrs.get("lang", "")
        if tag == "title" and not self._body_seen and not self.title_parts:
            self._in_title = True
        if tag == "meta":
            name = attrs.get("name", "").lower()
            prop = attrs.get("property", "").lower()
            if name == "description":
                self.description = attrs.get("content", "")
            elif name in {"robots", "googlebot"} and not self.meta_robots:
                self.meta_robots = attrs.get("content", "")
            elif prop == "og:description" and not self.description:
                self.description = attrs.get("content", "")
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonical = attrs.get("href", "")
        if tag == "body":
            self._in_body = True
            self._body_seen = True
            self.body_classes = attrs.get("class", "").split()
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_tag = tag
            self._heading_parts = []
        if tag == "a" and attrs.get("href"):
            self.links.append({
                "href": attrs["href"],
                "text": attrs.get("aria-label", "") or attrs.get("title", ""),
            })
        if tag == "img":
            self.images.append({
                "src": attrs.get("src", "") or attrs.get("data-src", ""),
                "alt": attrs.get("alt", ""),
            })
        if tag == "iframe":
            self.iframes.append({
                "src": attrs.get("src", "") or attrs.get("data-src", ""),
                "title": attrs.get("title", ""),
            })
        if tag == "form":
            self.forms.append({
                "action": attrs.get("action", ""),
                "method": attrs.get("method", "get").lower(),
                "class": attrs.get("class", ""),
            })
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._jsonld_depth += 1
        if self._in_body and tag in self.SKIP_TEXT:
            self._skip_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        if tag == self._heading_tag:
            self.headings.append({"level": tag, "text": clean_space(" ".join(self._heading_parts))})
            self._heading_tag = None
            self._heading_parts = []
        if tag == "script" and self._jsonld_depth:
            self._jsonld_depth -= 1
        if self._in_body and tag in self.SKIP_TEXT and self._skip_depth:
            self._skip_depth -= 1
        # The live site currently closes its first <body> before most page
        # content. Browsers repair that malformed structure and render the
        # trailing nodes. Keep collecting after the first body has appeared so
        # source extraction matches browser-visible content.
        if tag == "body" and not self._body_seen:
            self._in_body = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._heading_tag:
            self._heading_parts.append(data)
        if self._jsonld_depth:
            self.jsonld_parts.append(data)
        if self._in_body and not self._skip_depth:
            value = clean_space(data)
            if value:
                self.visible_parts.append(value)


def schema_types(jsonld_parts: list[str]) -> list[str]:
    found: set[str] = set()

    def walk(value) -> None:  # noqa: ANN001
        if isinstance(value, dict):
            types = value.get("@type")
            if isinstance(types, str):
                found.add(types)
            elif isinstance(types, list):
                found.update(str(item) for item in types)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    raw = " ".join(jsonld_parts).strip()
    if not raw:
        return []
    try:
        walk(json.loads(raw))
    except json.JSONDecodeError:
        for match in re.findall(r'"@type"\s*:\s*"([^"]+)"', raw):
            found.add(match)
    return sorted(found)


def template_family(body_classes: list[str]) -> str:
    classes = set(body_classes)
    if "home" in classes or "front-page" in classes:
        return "home"
    for prefix, label in (
        ("single-post", "post"),
        ("single-guide", "guide"),
        ("single-city", "city"),
        ("single-team_member", "team-member"),
        ("tax-category", "category"),
        ("category", "category"),
        ("tax-locationstate", "location-state"),
        ("page-template", "page"),
        ("page", "page"),
        ("archive", "archive"),
        ("search", "search"),
        ("error404", "404"),
    ):
        if any(item == prefix or item.startswith(prefix + "-") for item in classes):
            return label
    return "unknown"


def parse_page(result: FetchResult, base: str, sitemap_names: list[str], discovery: list[str]) -> dict[str, object]:
    content_type = result.headers.get("content-type", "")
    record: dict[str, object] = {
        "url": result.requested_url,
        "path": normalize_path(urllib.parse.urlsplit(result.requested_url).path),
        "final_url": result.final_url,
        "final_path": normalize_path(urllib.parse.urlsplit(result.final_url).path),
        "status": result.status,
        "redirects": result.redirects,
        "redirect_count": len(result.redirects),
        "error": result.error,
        "content_type": content_type,
        "x_robots_tag": result.headers.get("x-robots-tag", ""),
        "elapsed_ms": result.elapsed_ms,
        "sitemaps": sorted(sitemap_names),
        "discovery": sorted(discovery),
    }
    if "html" not in content_type.lower() and b"<html" not in result.body[:2000].lower():
        record["is_html"] = False
        return record
    encoding = "utf-8"
    match = re.search(r"charset=([^;\s]+)", content_type, re.I)
    if match:
        encoding = match.group(1).strip('"\'')
    text = result.body.decode(encoding, errors="replace")
    parser = PageParser()
    try:
        parser.feed(text)
    except Exception as exc:
        record["parse_error"] = f"{type(exc).__name__}: {exc}"
    visible = clean_space(" ".join(parser.visible_parts))
    headings = [item for item in parser.headings if item["text"]]
    h1s = [item["text"] for item in headings if item["level"] == "h1"]
    internal_links: list[str] = []
    cross_environment_links: list[str] = []
    base_host = urllib.parse.urlsplit(base).hostname or ""
    other_host = urllib.parse.urlsplit(STAGING if base == LIVE else LIVE).hostname or ""
    for link in parser.links:
        absolute = urllib.parse.urljoin(result.final_url, link["href"])
        parsed = urllib.parse.urlsplit(absolute)
        host = (parsed.hostname or "").removeprefix("www.")
        if host == base_host.removeprefix("www."):
            normalized = normalize_url(absolute, base)
            if normalized:
                internal_links.append(normalized)
        elif host == other_host.removeprefix("www."):
            cross_environment_links.append(absolute)
    family = template_family(parser.body_classes)
    if family == "unknown":
        sitemap_family = {
            "post-sitemap.xml": "post",
            "page-sitemap.xml": "page",
            "guide-sitemap.xml": "guide",
            "city-sitemap.xml": "city",
            "team_member-sitemap.xml": "team-member",
            "category-sitemap.xml": "category",
            "locationstate-sitemap.xml": "location-state",
        }
        family = next((sitemap_family[name] for name in sitemap_names if name in sitemap_family), family)
        if record["path"] == "/":
            family = "home"
    record.update({
        "is_html": True,
        "title": clean_space(" ".join(parser.title_parts)),
        "meta_description": clean_space(parser.description),
        "canonical": parser.canonical,
        "meta_robots": clean_space(parser.meta_robots),
        "lang": parser.lang,
        "body_classes": parser.body_classes,
        "template_family": family,
        "headings": headings,
        "h1": h1s,
        "h1_count": len(h1s),
        "visible_text": visible,
        "visible_text_sha256": hashlib.sha256(normalize_text(visible).encode()).hexdigest(),
        "word_count": len(re.findall(r"\b[\w'-]+\b", visible)),
        "links": parser.links,
        "internal_links": sorted(set(internal_links)),
        "internal_link_count": len(internal_links),
        "unique_internal_link_count": len(set(internal_links)),
        "cross_environment_links": sorted(set(cross_environment_links)),
        "cross_environment_link_count": len(cross_environment_links),
        "unique_cross_environment_link_count": len(set(cross_environment_links)),
        "images": parser.images,
        "image_count": len(parser.images),
        "iframes": parser.iframes,
        "forms": parser.forms,
        "schema_types": schema_types(parser.jsonld_parts),
    })
    return record


def fetch_sitemaps(base: str) -> tuple[dict[str, set[str]], dict[str, object]]:
    sitemap_index = base + "/sitemap_index.xml"
    pending = [sitemap_index]
    seen_maps: set[str] = set()
    memberships: dict[str, set[str]] = {}
    diagnostics: dict[str, object] = {"index": sitemap_index, "maps": {}}
    while pending:
        sitemap = pending.pop(0)
        if sitemap in seen_maps:
            continue
        seen_maps.add(sitemap)
        result = fetch(sitemap)
        info = {
            "status": result.status,
            "final_url": result.final_url,
            "error": result.error,
            "redirect_count": len(result.redirects),
        }
        diagnostics["maps"][sitemap] = info
        if result.status != 200:
            continue
        try:
            root = ET.fromstring(result.body)
        except ET.ParseError as exc:
            info["parse_error"] = str(exc)
            continue
        root_type = local_name(root.tag)
        if root_type == "sitemapindex":
            for child in root:
                loc = next((clean_space(grand.text) for grand in child if local_name(grand.tag) == "loc"), "")
                if loc:
                    pending.append(loc)
        elif root_type == "urlset":
            map_name = urllib.parse.urlsplit(sitemap).path.rsplit("/", 1)[-1]
            count = 0
            for child in root:
                if local_name(child.tag) != "url":
                    continue
                loc = next((clean_space(grand.text) for grand in child if local_name(grand.tag) == "loc"), "")
                normalized = normalize_url(loc, base) if loc else None
                if normalized:
                    memberships.setdefault(normalized, set()).add(map_name)
                    count += 1
            info["url_count"] = count
    diagnostics["unique_url_count"] = len(memberships)
    return memberships, diagnostics


def crawl_site(base: str, max_urls: int, workers: int) -> dict[str, object]:
    sitemap_memberships, sitemap_diagnostics = fetch_sitemaps(base)
    queued: set[str] = set(sitemap_memberships)
    queued.add(base + "/")
    discovery: dict[str, set[str]] = {url: {"sitemap"} for url in sitemap_memberships}
    discovery.setdefault(base + "/", set()).add("seed")
    records: dict[str, dict[str, object]] = {}
    frontier = sorted(queued)
    while frontier and len(records) < max_urls:
        batch = frontier[: max_urls - len(records)]
        frontier = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            fetched = list(pool.map(fetch, batch))
        for result in fetched:
            url = result.requested_url
            record = parse_page(
                result,
                base,
                sorted(sitemap_memberships.get(url, set())),
                sorted(discovery.get(url, set())),
            )
            records[url] = record
        for url in batch:
            record = records[url]
            for link in record.get("internal_links", []):
                assert isinstance(link, str)
                discovery.setdefault(link, set()).add("internal-link")
                if link not in queued and link not in records and len(queued) < max_urls:
                    queued.add(link)
                    frontier.append(link)
        frontier = sorted(set(frontier))
    robots_result = fetch(base + "/robots.txt")
    site = {
        "base": base,
        "robots": {
            "status": robots_result.status,
            "text": robots_result.body.decode("utf-8", errors="replace"),
            "error": robots_result.error,
        },
        "sitemaps": sitemap_diagnostics,
        "crawl_truncated": bool(frontier),
        "max_urls": max_urls,
        "pages": [records[url] for url in sorted(records)],
    }
    # Concurrent crawls can briefly trigger 5xx responses on the staging host.
    # Recheck only transient failures sequentially so they are not mislabeled
    # as persistent defects.
    for index, record in enumerate(site["pages"]):
        status = record.get("status")
        if status is None or status in {429, 500, 502, 503, 504}:
            result = fetch(str(record["url"]), attempts=3)
            site["pages"][index] = parse_page(
                result,
                base,
                list(record.get("sitemaps", [])),
                list(record.get("discovery", [])) + ["sequential-recheck"],
            )
    close_internal_graph(site, base, max_urls, workers)
    return site


def close_internal_graph(
    site: dict[str, object],
    base: str,
    max_urls: int,
    workers: int,
) -> None:
    """Fetch newly exposed internal targets until the saved graph is closed."""
    pages_by_url = {str(page["url"]): page for page in site["pages"]}
    truncated = bool(site.get("crawl_truncated"))
    while True:
        missing: set[str] = set()
        for page in pages_by_url.values():
            for link in page.get("internal_links", []):
                assert isinstance(link, str)
                if link in pages_by_url:
                    target = pages_by_url[link]
                    target["discovery"] = sorted(set(target.get("discovery", [])) | {"internal-link"})
                else:
                    missing.add(link)
        if not missing:
            break
        capacity = max_urls - len(pages_by_url)
        if capacity <= 0:
            truncated = True
            break
        batch = sorted(missing)[:capacity]
        if len(batch) < len(missing):
            truncated = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            fetched = list(pool.map(fetch, batch))
        for result in fetched:
            if result.status is None or result.status in {429, 500, 502, 503, 504}:
                result = fetch(result.requested_url, attempts=3)
            pages_by_url[result.requested_url] = parse_page(
                result,
                base,
                [],
                ["internal-link", "closure-pass"],
            )
    unresolved = sorted({
        link
        for page in pages_by_url.values()
        for link in page.get("internal_links", [])
        if link not in pages_by_url
    })
    site["pages"] = [pages_by_url[url] for url in sorted(pages_by_url)]
    site["crawl_truncated"] = truncated or bool(unresolved)
    site["graph_closure"] = {
        "recorded_internal_target_count": len({
            link for page in pages_by_url.values() for link in page.get("internal_links", [])
        }),
        "unrecorded_internal_targets": unresolved,
        "closed": not unresolved,
    }


def probe_counterpart_paths(
    source_site: dict[str, object],
    target_site: dict[str, object],
    target_base: str,
    workers: int,
) -> None:
    """Probe direct source paths that discovery did not expose on the target."""
    source_paths = {
        str(page["path"]) for page in source_site["pages"]
        if page.get("is_html") and page.get("status") == 200 and page.get("redirect_count", 0) == 0
    }
    target_paths = {str(page["path"]) for page in target_site["pages"]}
    missing_paths = sorted(source_paths - target_paths)
    urls = [target_base.rstrip("/") + path for path in missing_paths]
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, 4)) as pool:
        fetched = list(pool.map(fetch, urls))
    for result in fetched:
        if result.status is None or result.status in {429, 500, 502, 503, 504}:
            result = fetch(result.requested_url, attempts=3)
        target_site["pages"].append(parse_page(
            result,
            target_base,
            [],
            ["counterpart-probe"],
        ))
    target_site["pages"].sort(key=lambda page: str(page["url"]))


def comparison_similarity(stage: dict[str, object], live: dict[str, object]) -> dict[str, object]:
    stage_title = normalize_text(str(stage.get("title", "")))
    live_title = normalize_text(str(live.get("title", "")))
    stage_desc = normalize_text(str(stage.get("meta_description", "")))
    live_desc = normalize_text(str(live.get("meta_description", "")))
    stage_h1 = normalize_text(" | ".join(stage.get("h1", [])))
    live_h1 = normalize_text(" | ".join(live.get("h1", [])))
    stage_text = normalize_text(str(stage.get("visible_text", "")))
    live_text = normalize_text(str(live.get("visible_text", "")))
    text_ratio = difflib.SequenceMatcher(None, stage_text, live_text, autojunk=False).ratio()
    word_stage = int(stage.get("word_count", 0) or 0)
    word_live = int(live.get("word_count", 0) or 0)
    word_delta = word_stage - word_live
    word_delta_pct = round(word_delta / word_live * 100, 1) if word_live else None
    canonical_stage = normalize_path(urllib.parse.urlsplit(str(stage.get("canonical", ""))).path)
    canonical_live = normalize_path(urllib.parse.urlsplit(str(live.get("canonical", ""))).path)
    title_equal = stage_title == live_title
    description_equal = stage_desc == live_desc
    h1_equal = stage_h1 == live_h1
    canonical_equal = canonical_stage == canonical_live
    status_equal = stage.get("status") == live.get("status")
    if text_ratio == 1.0 and title_equal and description_equal and h1_equal and canonical_equal and status_equal:
        classification = "Exact"
    elif text_ratio >= 0.98 and title_equal and h1_equal and status_equal:
        classification = "Near-match"
    else:
        classification = "Changed"
    return {
        "classification": classification,
        "text_similarity": round(text_ratio, 4),
        "title_equal": title_equal,
        "description_equal": description_equal,
        "h1_equal": h1_equal,
        "canonical_path_equal": canonical_equal,
        "status_equal": status_equal,
        "word_delta": word_delta,
        "word_delta_pct": word_delta_pct,
        "template_equal": stage.get("template_family") == live.get("template_family"),
        "schema_equal": stage.get("schema_types") == live.get("schema_types"),
    }


def page_match_key(page: dict[str, object], field: str) -> str:
    if field == "slug":
        path = str(page.get("final_path") or page.get("path") or "/").strip("/")
        return slugify(path.rsplit("/", 1)[-1] if path else "home")
    if field == "title":
        return slugify(str(page.get("title", "")))
    if field == "h1":
        return slugify(" ".join(page.get("h1", [])))
    raise ValueError(field)


def compare_sites(stage_site: dict[str, object], live_site: dict[str, object]) -> dict[str, object]:
    stage_pages = {
        str(page["path"]): page for page in stage_site["pages"]
        if page.get("is_html") and page.get("status") == 200 and page.get("redirect_count", 0) == 0
    }
    live_pages = {
        str(page["path"]): page for page in live_site["pages"]
        if page.get("is_html") and page.get("status") == 200 and page.get("redirect_count", 0) == 0
    }
    unmatched_stage = set(stage_pages)
    unmatched_live = set(live_pages)
    matches: list[dict[str, object]] = []

    def add(stage_path: str, live_path: str, method: str, confidence: str) -> None:
        stage = stage_pages[stage_path]
        live = live_pages[live_path]
        matches.append({
            "stage_path": stage_path,
            "live_path": live_path,
            "mapping_method": method,
            "mapping_confidence": confidence,
            **comparison_similarity(stage, live),
        })
        unmatched_stage.discard(stage_path)
        unmatched_live.discard(live_path)

    for path in sorted(unmatched_stage & unmatched_live):
        add(path, path, "exact-path", "high")

    for field, method, confidence in (
        ("slug", "unique-slug", "high"),
        ("title", "unique-title", "high"),
        ("h1", "unique-h1", "medium"),
    ):
        stage_keys: dict[str, list[str]] = {}
        live_keys: dict[str, list[str]] = {}
        for path in unmatched_stage:
            key = page_match_key(stage_pages[path], field)
            if key:
                stage_keys.setdefault(key, []).append(path)
        for path in unmatched_live:
            key = page_match_key(live_pages[path], field)
            if key:
                live_keys.setdefault(key, []).append(path)
        for key in sorted(stage_keys.keys() & live_keys.keys()):
            if len(stage_keys[key]) == len(live_keys[key]) == 1:
                add(stage_keys[key][0], live_keys[key][0], method, confidence)

    candidates: list[tuple[float, str, str]] = []
    for stage_path in unmatched_stage:
        stage = stage_pages[stage_path]
        stage_label = " ".join((str(stage.get("title", "")), " ".join(stage.get("h1", []))))
        for live_path in unmatched_live:
            live = live_pages[live_path]
            live_label = " ".join((str(live.get("title", "")), " ".join(live.get("h1", []))))
            ratio = difflib.SequenceMatcher(None, slugify(stage_label), slugify(live_label), autojunk=False).ratio()
            if ratio >= 0.88:
                candidates.append((ratio, stage_path, live_path))
    for ratio, stage_path, live_path in sorted(candidates, reverse=True):
        if stage_path in unmatched_stage and live_path in unmatched_live:
            add(stage_path, live_path, f"label-similarity-{ratio:.2f}", "low")

    matches.sort(key=lambda item: (item["live_path"], item["stage_path"]))
    return {
        "matches": matches,
        "staging_only": sorted(unmatched_stage),
        "live_only": sorted(unmatched_live),
        "counts": {
            "mapped": len(matches),
            "exact": sum(item["classification"] == "Exact" for item in matches),
            "near_match": sum(item["classification"] == "Near-match" for item in matches),
            "changed": sum(item["classification"] == "Changed" for item in matches),
            "staging_only": len(unmatched_stage),
            "live_only": len(unmatched_live),
        },
    }


def md_escape(value: object) -> str:
    return clean_space(str(value)).replace("|", "\\|")


def compact_embedded_value(value: str) -> str:
    if value.startswith("data:") or len(value) > 1_000:
        digest = hashlib.sha256(value.encode()).hexdigest()[:16]
        return f"[embedded-value bytes={len(value)} sha256={digest}]"
    return value


def write_inventory(path: str, result: dict[str, object]) -> None:
    comparison = result["comparison"]
    stage_by_path = {page["path"]: page for page in result["staging"]["pages"]}
    live_by_path = {page["path"]: page for page in result["live"]["pages"]}
    counts = comparison["counts"]
    lines = [
        "# Aurit Full-Site Page Change Inventory",
        "",
        f"Generated: {result['generated_at']}",
        "",
        "Scope: every HTML URL found in either XML sitemap or through recursive same-origin internal links, "
        "plus unmatched direct-page paths probed on the opposite host. The crawl did not execute JavaScript or submit forms.",
        "",
        "## Summary",
        "",
        f"- Mapped page pairs: {counts['mapped']}",
        f"- Exact by source/metadata criteria: {counts['exact']}",
        f"- Near-match by source/metadata criteria: {counts['near_match']}",
        f"- Changed by source/metadata criteria: {counts['changed']}",
        f"- Staging-only URLs: {counts['staging_only']}",
        f"- Live-only URLs: {counts['live_only']}",
        "",
        "## Mapped pages",
        "",
        "| Live path | Staging path | Map | Confidence | Mechanical result | Source-text similarity | Live words | Staging words | Title | H1 | Meta description | Canonical path |",
        "|---|---|---|---|---|---:|---:|---:|---|---|---|---|",
    ]
    for item in comparison["matches"]:
        stage = stage_by_path[item["stage_path"]]
        live = live_by_path[item["live_path"]]
        lines.append(
            "| {live_path} | {stage_path} | {method} | {confidence} | {classification} | {similarity:.1%} | {live_words} | {stage_words} | {title} | {h1} | {description} | {canonical} |".format(
                live_path=md_escape(item["live_path"]),
                stage_path=md_escape(item["stage_path"]),
                method=md_escape(item["mapping_method"]),
                confidence=md_escape(item["mapping_confidence"]),
                classification=item["classification"],
                similarity=item["text_similarity"],
                live_words=live.get("word_count", ""),
                stage_words=stage.get("word_count", ""),
                title="Same" if item["title_equal"] else "Changed",
                h1="Same" if item["h1_equal"] else "Changed",
                description="Same" if item["description_equal"] else "Changed",
                canonical="Same" if item["canonical_path_equal"] else "Changed",
            )
        )
    lines.extend(["", "## Live-only URLs", ""])
    if comparison["live_only"]:
        lines.extend(f"- `{path_value}`" for path_value in comparison["live_only"])
    else:
        lines.append("- None")
    lines.extend(["", "## Staging-only URLs", ""])
    if comparison["staging_only"]:
        lines.extend(f"- `{path_value}`" for path_value in comparison["staging_only"])
    else:
        lines.append("- None")
    lines.extend(["", "## Mapping notes", ""])
    lines.extend([
        "- Exact-path, unique-slug, and unique-title mappings are high-confidence mechanical matches.",
        "- Unique-H1 mappings are medium confidence.",
        "- Label-similarity mappings are low confidence and require human confirmation.",
        "- Exact requires identical normalized source-extracted body text plus matching title, description, H1, canonical path, and status. It is not a pixel-level guarantee.",
        "- Near-match means at least 98% source-text similarity with matching title, H1, and status. It is not a holistic severity rating.",
    ])
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def write_field_changes(path: str, result: dict[str, object]) -> None:
    stage_by_path = {page["path"]: page for page in result["staging"]["pages"]}
    live_by_path = {page["path"]: page for page in result["live"]["pages"]}
    lines = [
        "# Aurit Page Field Changes",
        "",
        f"Generated: {result['generated_at']}",
        "",
        "This appendix preserves the actual values behind changed title, H1, canonical, robots, and schema flags. "
        "A blank value is shown as `(missing or blank)`.",
        "",
        "| Live path | Staging path | Field | Live value | Staging value |",
        "|---|---|---|---|---|",
    ]
    fields = (
        ("Title", "title"),
        ("H1", "h1"),
        ("Canonical", "canonical"),
        ("Meta robots", "meta_robots"),
        ("Schema types", "schema_types"),
    )
    change_count = 0
    for match in result["comparison"]["matches"]:
        stage = stage_by_path[match["stage_path"]]
        live = live_by_path[match["live_path"]]
        for label, key in fields:
            live_value = live.get(key, "")
            stage_value = stage.get(key, "")
            if isinstance(live_value, list):
                live_value = " | ".join(str(item) for item in live_value)
            if isinstance(stage_value, list):
                stage_value = " | ".join(str(item) for item in stage_value)
            if normalize_text(str(live_value)) == normalize_text(str(stage_value)):
                continue
            change_count += 1
            lines.append(
                f"| `{md_escape(match['live_path'])}` | `{md_escape(match['stage_path'])}` | {label} | "
                f"{md_escape(live_value or '(missing or blank)')} | {md_escape(stage_value or '(missing or blank)')} |"
            )
    lines[5:5] = [f"Changed field rows: {change_count}", ""]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def redirected_inlink_target(site: dict[str, object], link: str) -> str:
    by_url = {str(page["url"]): page for page in site["pages"]}
    target = by_url.get(link)
    if not target or target.get("status") != 200:
        return link
    final_path = normalize_path(urllib.parse.urlsplit(str(target.get("final_url", link))).path)
    return str(site["base"]).rstrip("/") + final_path


def orphan_like_paths(site: dict[str, object]) -> list[str]:
    pages = site["pages"]
    inlinks: dict[str, set[str]] = {str(page["url"]): set() for page in pages}
    for source in pages:
        if not source.get("is_html"):
            continue
        for link in source.get("internal_links", []):
            target = redirected_inlink_target(site, str(link))
            if normalize_path(urllib.parse.urlsplit(target).path) != source.get("path"):
                inlinks.setdefault(target, set()).add(str(source.get("path")))
    output = []
    for page in pages:
        robots = f"{page.get('meta_robots', '')} {page.get('x_robots_tag', '')}".lower()
        if (
            page.get("status") == 200
            and page.get("redirect_count", 0) == 0
            and page.get("sitemaps")
            and "noindex" not in robots
            and not inlinks.get(str(page["url"]))
        ):
            output.append(str(page["path"]))
    return sorted(output)


def write_technical_appendix(path: str, result: dict[str, object]) -> None:
    lines = [
        "# Aurit Technical Crawl Appendix",
        "",
        f"Generated: {result['generated_at']}",
        "",
        "Calculations use the saved same-host link graph. An internal target is closed when it has a saved page record, "
        "including redirects and final 404s. Broken-link, redirect, and orphan-like calculations exclude self-links. "
        "Orphan-like counts include direct, indexable sitemap pages and credit links through redirects to their final destination.",
        "",
    ]
    for site_name in ("staging", "live"):
        site = result[site_name]
        by_url = {str(page["url"]): page for page in site["pages"]}
        source_map: dict[str, list[str]] = {}
        for source in site["pages"]:
            for link in source.get("internal_links", []):
                if normalize_path(urllib.parse.urlsplit(str(link)).path) == source.get("path"):
                    continue
                source_map.setdefault(str(link), []).append(str(source.get("path")))
        broken = [
            page for page in site["pages"]
            if page.get("status") == 404 and source_map.get(str(page["url"]))
        ]
        redirecting = [
            page for page in site["pages"]
            if page.get("status") == 200
            and page.get("redirect_count", 0) > 0
            and source_map.get(str(page["url"]))
        ]
        orphan_paths = orphan_like_paths(site)
        cross_sources = [
            page for page in site["pages"] if page.get("cross_environment_link_count", 0)
        ]
        lines.extend([
            f"## {site_name.title()}",
            "",
            f"- Saved page/target records: {len(site['pages'])}",
            f"- Graph closure: {'closed' if site['graph_closure']['closed'] else 'not closed'}",
            f"- Unrecorded same-host internal targets: {len(site['graph_closure']['unrecorded_internal_targets'])}",
            f"- Internally linked final-404 targets: {len(broken)}",
            f"- Internally linked redirect targets: {len(redirecting)}",
            f"- Orphan-like direct/indexable sitemap pages: {len(orphan_paths)}",
            f"- Cross-environment anchor occurrences: {sum(int(page.get('cross_environment_link_count', 0)) for page in cross_sources)} across {len(cross_sources)} source pages",
            "",
            "### Internally linked final-404 targets",
            "",
            "| Target | Source-page count | Source paths |",
            "|---|---:|---|",
        ])
        for target in sorted(broken, key=lambda page: str(page["path"])):
            sources = sorted(set(source_map[str(target["url"])]))
            lines.append(
                f"| `{md_escape(target['path'])}` | {len(sources)} | {md_escape(', '.join(sources))} |"
            )
        lines.extend([
            "",
            "### Internally linked redirect targets",
            "",
            "| Requested path | Final path | Hops | Source-page count |",
            "|---|---|---:|---:|",
        ])
        for target in sorted(redirecting, key=lambda page: str(page["path"])):
            sources = sorted(set(source_map[str(target["url"])]))
            lines.append(
                f"| `{md_escape(target['path'])}` | `{md_escape(target['final_path'])}` | "
                f"{target['redirect_count']} | {len(sources)} |"
            )
        lines.extend(["", "### Orphan-like sitemap pages", ""])
        lines.extend(f"- `{item}`" for item in orphan_paths)
        lines.extend(["", "### Cross-environment source pages", ""])
        if cross_sources:
            lines.extend([
                "| Source path | Anchor occurrences | Unique targets |",
                "|---|---:|---:|",
            ])
            for source in sorted(cross_sources, key=lambda page: str(page["path"])):
                lines.append(
                    f"| `{md_escape(source['path'])}` | {source['cross_environment_link_count']} | "
                    f"{source['unique_cross_environment_link_count']} |"
                )
        else:
            lines.append("- None")
        lines.append("")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, help="Output JSON path")
    parser.add_argument("--inventory", required=True, help="Output Markdown inventory path")
    parser.add_argument("--fields", required=True, help="Output Markdown field-change appendix path")
    parser.add_argument("--technical", required=True, help="Output Markdown technical appendix path")
    parser.add_argument("--max-urls", type=int, default=600)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    live_site = crawl_site(LIVE, args.max_urls, args.workers)
    stage_site = crawl_site(STAGING, args.max_urls, args.workers)
    for _ in range(3):
        before = (len(live_site["pages"]), len(stage_site["pages"]))
        live_source = {"pages": list(live_site["pages"])}
        stage_source = {"pages": list(stage_site["pages"])}
        probe_counterpart_paths(live_source, stage_site, STAGING, args.workers)
        probe_counterpart_paths(stage_source, live_site, LIVE, args.workers)
        close_internal_graph(live_site, LIVE, args.max_urls, args.workers)
        close_internal_graph(stage_site, STAGING, args.max_urls, args.workers)
        after = (len(live_site["pages"]), len(stage_site["pages"]))
        if after == before:
            break
    result = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "method": "XML sitemaps plus recursive same-origin HTML links and cross-environment counterpart-path probes; no JavaScript execution",
        "live": live_site,
        "staging": stage_site,
    }
    result["comparison"] = compare_sites(stage_site, live_site)
    for site in (live_site, stage_site):
        for page in site["pages"]:
            if "visible_text" in page:
                page["visible_text_excerpt"] = str(page["visible_text"])[:500]
                del page["visible_text"]
            for collection_name in ("links", "images", "iframes", "forms"):
                for item in page.get(collection_name, []):
                    for key, value in item.items():
                        if isinstance(value, str):
                            item[key] = compact_embedded_value(value)
            page["heading_counts"] = {
                level: sum(item.get("level") == level for item in page.get("headings", []))
                for level in ("h1", "h2", "h3", "h4", "h5", "h6")
            }
            page["iframe_sources"] = sorted({
                item.get("src", "") for item in page.get("iframes", []) if item.get("src")
            })
            page["form_targets"] = sorted({
                f"{item.get('method', 'get').upper()} {item.get('action', '')}"
                for item in page.get("forms", [])
            })
            page["image_alt_issues"] = [
                item for item in page.get("images", [])
                if not clean_space(item.get("alt", ""))
                or re.fullmatch(r"[A-Za-z0-9+/=]{8,}", clean_space(item.get("alt", "")))
            ][:20]
            for collection_name in ("links", "images", "iframes", "forms", "headings", "body_classes"):
                page.pop(collection_name, None)
    with open(args.json, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    write_inventory(args.inventory, result)
    write_field_changes(args.fields, result)
    write_technical_appendix(args.technical, result)


if __name__ == "__main__":
    main()
