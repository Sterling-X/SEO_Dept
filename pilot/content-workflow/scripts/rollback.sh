#!/bin/sh
# Remove exactly the eight pilot activation entries: five symlinks and three Codex agent copies.
# Never touches a foreign symlink or a modified copy.
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
cd "$repo"
banner='# GENERATED FILE. Source of truth: pilot/content-workflow/canonical/roles/'
unlink_pilot() {
  name=$1
  adapter="pilot/content-workflow/adapters/codex/agents/$(basename "$name")"
  if [ -L "$name" ]; then
    case "$(readlink "$name")" in
      ../../pilot/content-workflow/*) rm "$name"; echo "removed  $name" ;;
      *) echo "SKIP     $name points outside the pilot tree; left in place" ;;
    esac
  elif [ -f "$name" ] && [ -f "$adapter" ] && cmp -s "$name" "$adapter"; then
    rm "$name"; echo "removed  $name (byte copy of its pilot adapter)"
  elif [ -f "$name" ] && head -n 1 "$name" | grep -q "^$banner"; then
    rm "$name"; echo "removed  $name (pilot-generated copy from an earlier adapter build)"
  elif [ -e "$name" ]; then
    echo "SKIP     $name is not a pilot symlink or a pilot-generated copy; left in place"
  else
    echo "absent   $name"
  fi
}
for name in .claude/agents/content-writer.md .claude/agents/legal-reviewer.md .claude/agents/editorial-reviewer.md \
            .codex/agents/content_writer.toml .codex/agents/legal_reviewer.toml .codex/agents/editorial_reviewer.toml \
            .claude/skills/content-workflow .agents/skills/content-workflow; do
  unlink_pilot "$name"
done
echo "Rolled back. Pilot files under pilot/content-workflow/ are untouched; the backup manifest is at ~/SEO_Dept_backups/content-workflow-pilot-2026-09-23/RESTORE.md."
