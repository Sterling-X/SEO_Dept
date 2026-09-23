#!/bin/sh
# LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL.
#
# Reuses only the already pinned document-rendering wrapper from the local Core
# skill. No Core template, generator, validator, content, or link rule is used.
set -eu

skill_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
# PILOT CANDIDATE v1: resolve the repository root by marker instead of assuming the skill sits in .agents/skills.
repo_root=${SEO_DEPT_ROOT:-}
if [ -z "$repo_root" ]; then
  probe=$skill_root
  while [ "$probe" != "/" ]; do
    if [ -f "$probe/AGENTS.md" ] && [ -d "$probe/.agents" ]; then repo_root=$probe; break; fi
    probe=$(dirname -- "$probe")
  done
fi
if [ -z "$repo_root" ]; then echo "ERROR: repository root not found above $skill_root" >&2; exit 2; fi
core_renderer="$repo_root/.agents/skills/family-law-service-pages/scripts/render-core-hub.sh"

if [ ! -x "$core_renderer" ]; then
  echo "ERROR: Proven local renderer wrapper is unavailable: $core_renderer" >&2
  exit 2
fi

echo "INFO: FL-M008 local wrapper is delegating generic DOCX rendering only to $core_renderer" >&2
exec "$core_renderer" "$@"
