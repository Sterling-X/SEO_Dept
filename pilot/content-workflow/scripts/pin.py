#!/usr/bin/env python3
"""Compute and write skill and source pins into a run's run.json.

Usage:
  pin.py <run-dir> [--skills <repo-relative SKILL.md path>...] [--sources <run-relative path>...]

Each named skill is recorded as {name, path, sha256}; each source file's sha256 is
refreshed (the source must already be declared in run.json with id, path, and kind so
that its purpose is explicit). The script never adds an undeclared source.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cw_common as cw  # noqa: E402


def pin_skill(repo_root: Path, rel: str) -> dict:
    """Pin a skill by its SKILL.md hash plus the hash of every required resource and the manifest itself."""
    path = repo_root / rel
    if not path.is_file():
        raise FileNotFoundError(rel)
    files: dict[str, str] = {}
    manifest_path = path.parent / "pilot-manifest.json"
    if manifest_path.is_file():
        files["pilot-manifest.json"] = cw.sha256_file(manifest_path)
        for required in cw.load_json(manifest_path).get("required_files", []):
            target = path.parent / required
            if target.is_file():
                files[required] = cw.sha256_file(target)
    return {"name": path.parent.name, "path": rel, "sha256": cw.sha256_file(path), "files": files}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--skills", nargs="*", default=[])
    parser.add_argument("--sources", nargs="*", default=[])
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    repo_root = cw.find_repo_root()
    run_path = run_dir / "run.json"
    run = cw.load_json(run_path)
    skills = {s["path"]: s for s in run.get("skills", []) if s.get("path")}
    for rel in args.skills:
        try:
            skills[rel] = pin_skill(repo_root, rel)
        except FileNotFoundError:
            print(f"ERROR: skill file not found: {rel}")
            return 1
        print(f"pinned skill {skills[rel]['name']} @ {skills[rel]['sha256'][:12]}… ({len(skills[rel]['files'])} resource hash(es), manifest included)")
    run["skills"] = list(skills.values())
    declared = {s.get("path"): s for s in run.get("sources", [])}
    for rel in args.sources:
        if rel not in declared:
            print(f"ERROR: source {rel} is not declared in run.json (declare id, path, kind first)")
            return 1
        path = run_dir / rel
        if not path.is_file():
            print(f"ERROR: source file not found: {rel}")
            return 1
        declared[rel]["sha256"] = cw.sha256_file(path)
        print(f"pinned source {declared[rel].get('id')} @ {declared[rel]['sha256'][:12]}…")
    cw.dump_json(run_path, run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
