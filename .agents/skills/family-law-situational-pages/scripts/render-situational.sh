#!/bin/sh
# LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL.
#
# Reuses only the already pinned document-rendering wrapper from the local Core
# skill. No Core template, generator, validator, content, or link rule is used.
set -eu

skill_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
core_renderer="$skill_root/../family-law-service-pages/scripts/render-core-hub.sh"

if [ ! -x "$core_renderer" ]; then
  echo "ERROR: Proven local renderer wrapper is unavailable: $core_renderer" >&2
  exit 2
fi

echo "INFO: FL-M008 local wrapper is delegating generic DOCX rendering only to $core_renderer" >&2
exec "$core_renderer" "$@"
