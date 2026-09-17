#!/usr/bin/env python3
"""Deterministic regression checks for recovered-page crawl closure."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


SCRIPT = Path(__file__).with_name("crawl_compare.py")
SPEC = importlib.util.spec_from_file_location("aurit_crawl_compare", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def page(url: str, links: list[str]) -> dict[str, object]:
    path = MODULE.normalize_path(MODULE.urllib.parse.urlsplit(url).path)
    return {
        "url": url,
        "path": path,
        "status": 200,
        "redirect_count": 0,
        "internal_links": links,
        "discovery": ["fixture"],
    }


def run_case(seed_links: list[str], returned_links: dict[str, list[str]]) -> tuple[dict[str, object], list[str]]:
    base = "https://example.com"
    site = {
        "base": base,
        "pages": [page(base + "/", seed_links)],
        "crawl_truncated": False,
    }
    calls: list[str] = []
    original_fetch = MODULE.fetch
    original_parse = MODULE.parse_page

    def fake_fetch(url: str, *args, **kwargs):  # noqa: ANN001, ARG001
        calls.append(url)
        return MODULE.FetchResult(url, url, 200, {"content-type": "text/html"}, b"", [], None, 1)

    def fake_parse(result, base_url, sitemap_names, discovery):  # noqa: ANN001, ARG001
        record = page(result.requested_url, returned_links.get(result.requested_url, []))
        record["discovery"] = list(discovery)
        return record

    MODULE.fetch = fake_fetch
    MODULE.parse_page = fake_parse
    try:
        MODULE.close_internal_graph(site, base, 20, 2)
    finally:
        MODULE.fetch = original_fetch
        MODULE.parse_page = original_parse
    return site, calls


def main() -> None:
    base = "https://example.com"

    # Original failure shape: a link first exposed by a recovered record must
    # be fetched and saved.
    site, calls = run_case([base + "/recovered/"], {})
    assert calls == [base + "/recovered/"]
    assert site["graph_closure"]["closed"] is True
    assert {item["path"] for item in site["pages"]} == {"/", "/recovered/"}

    # Different relevant case: closure must continue through another newly
    # exposed level instead of stopping after one repair pass.
    site, calls = run_case(
        [base + "/level-one/"],
        {base + "/level-one/": [base + "/level-two/"]},
    )
    assert calls == [base + "/level-one/", base + "/level-two/"]
    assert site["graph_closure"]["closed"] is True
    assert {item["path"] for item in site["pages"]} == {"/", "/level-one/", "/level-two/"}

    # Unaffected case: an already closed graph must not perform any fetch.
    site, calls = run_case([], {})
    assert calls == []
    assert site["graph_closure"]["closed"] is True
    assert len(site["pages"]) == 1

    print("PASS: recovered-page crawl closure regression checks")


if __name__ == "__main__":
    main()
