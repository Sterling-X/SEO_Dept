#!/usr/bin/env python3
"""Render draft.md from a generator manifest so the reviewed text and the export cannot diverge.

Usage: render_draft.py <manifest.json> <draft.md>

Supports the FL-M008 local-replacement manifest shape (content blocks p/h2/h3/ul/ol with runs
text/strong/internal_link/citation, plus sources). Output: H1, consumer copy, then Sources.
Citation markers are written in the hyperlinked form [[n]](url), which the readiness check
requires in the draft; internal links as [anchor](url); bold lead-ins as **text**.
The publisher block is not rendered: reviewers read consumer copy, and the readiness check
ignores anything before the H1 in both draft and export.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def render(manifest: dict) -> str:
    meta = manifest.get("meta") or {}
    links = {link["id"]: link for link in manifest.get("link_manifest", [])}
    sources = {int(source["id"]): source for source in manifest.get("sources", [])}

    def runs_to_md(runs: list[dict]) -> str:
        out: list[str] = []
        for run in runs or []:
            kind, text = run.get("type"), str(run.get("text", ""))
            if kind == "text":
                out.append(text)
            elif kind == "strong":
                out.append(f"**{text}**")
            elif kind == "internal_link":
                url = links.get(run.get("link_id"), {}).get("client_url", "")
                out.append(f"[{text}]({url})")
            elif kind == "citation":
                source = sources.get(int(run.get("source_id")))
                out.append(f"[[{run.get('source_id')}]]({source['url'] if source else ''})")
            else:
                raise ValueError(f"unsupported run type {kind!r}")
        return "".join(out)

    lines: list[str] = [f"# {meta.get('h1', '')}", ""]
    for block in manifest.get("content", []):
        kind = block.get("type")
        if kind == "p":
            lines += [runs_to_md(block.get("runs", [])), ""]
        elif kind == "h2":
            lines += [f"## {block.get('text', '')}", ""]
        elif kind == "h3":
            lines += [f"### {block.get('text', '')}", ""]
        elif kind in ("ul", "ol"):
            for index, item in enumerate(block.get("items", []), 1):
                prefix = "- " if kind == "ul" else f"{index}. "
                lines.append(prefix + runs_to_md(item.get("runs", [])))
            lines.append("")
        else:
            raise ValueError(f"unsupported block type {kind!r}")
    lines += ["## Sources", ""]
    for source_id in sorted(sources):
        source = sources[source_id]
        lines.append(f"[{source_id}] {source['label']} | {source['url']}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifest", type=Path)
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.draft.parent.mkdir(parents=True, exist_ok=True)
    args.draft.write_text(render(manifest), encoding="utf-8")
    print(f"rendered {args.draft} from {args.manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
