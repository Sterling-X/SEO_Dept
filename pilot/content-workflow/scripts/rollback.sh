#!/bin/sh
# Remove exactly the eight pilot activation symlinks. Never touches a non-symlink or a
# symlink that points somewhere other than the pilot tree.
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
cd "$repo"
unlink_pilot() {
  name=$1
  if [ -L "$name" ]; then
    case "$(readlink "$name")" in
      ../../pilot/content-workflow/*) rm "$name"; echo "removed  $name" ;;
      *) echo "SKIP     $name points outside the pilot tree; left in place" ;;
    esac
  elif [ -e "$name" ]; then
    echo "SKIP     $name is not a symlink; left in place"
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
