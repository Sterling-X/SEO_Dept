#!/bin/sh
# Activate the content-workflow pilot on this checkout by adding symlinks into the host
# discovery paths. Adds exactly eight symlinks; edits no existing file. Idempotent.
# Rollback: scripts/rollback.sh (removes exactly these eight symlinks).
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
cd "$repo"
link() {
  target=$1; name=$2
  if [ -L "$name" ]; then
    current=$(readlink "$name")
    if [ "$current" = "$target" ]; then echo "exists   $name -> $target"; return; fi
    echo "ERROR: $name is a symlink to $current, not $target; refusing to replace" >&2; exit 1
  fi
  if [ -e "$name" ]; then echo "ERROR: $name exists and is not a pilot symlink; refusing to overwrite" >&2; exit 1; fi
  ln -s "$target" "$name"; echo "linked   $name -> $target"
}
mkdir -p .claude/agents .codex/agents .claude/skills .agents/skills
link ../../pilot/content-workflow/adapters/claude/agents/content-writer.md      .claude/agents/content-writer.md
link ../../pilot/content-workflow/adapters/claude/agents/legal-reviewer.md      .claude/agents/legal-reviewer.md
link ../../pilot/content-workflow/adapters/claude/agents/editorial-reviewer.md  .claude/agents/editorial-reviewer.md
link ../../pilot/content-workflow/adapters/codex/agents/content_writer.toml     .codex/agents/content_writer.toml
link ../../pilot/content-workflow/adapters/codex/agents/legal_reviewer.toml     .codex/agents/legal_reviewer.toml
link ../../pilot/content-workflow/adapters/codex/agents/editorial_reviewer.toml .codex/agents/editorial_reviewer.toml
link ../../pilot/content-workflow/skill/content-workflow                        .claude/skills/content-workflow
link ../../pilot/content-workflow/skill/content-workflow                        .agents/skills/content-workflow
echo "Activated. Candidate skills under pilot/content-workflow/candidates/ are NOT linked; runs pin them by path."
echo "Claude Code: start a new session (or wait for the agents directory watcher) so the three agents and /content-workflow load."
echo "Codex: start a new session at the repository root; custom agents load from .codex/agents and the skill from .agents/skills."
