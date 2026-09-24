#!/bin/sh
# LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL. PILOT CANDIDATE v1.
#
# Self-contained render wrapper for the FL-M008 candidate. Runs Codex's packaged DOCX renderer
# at the exact release pinned in ../renderer-tools.lock.json with the isolated LibreOffice and
# Python environment installed by the baseline Core skill (reused by path; both are Git-ignored
# local installs). Every integrity check of the baseline wrapper is kept: exact release path,
# SHA-256 pin, isolated soffice and Python, explicit and empty --output_dir. It fails closed.
set -eu

skill_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
lock="$skill_root/renderer-tools.lock.json"
if [ ! -f "$lock" ]; then echo "ERROR: renderer lock is missing: $lock" >&2; exit 2; fi
repo_root=${SEO_DEPT_ROOT:-}
if [ -z "$repo_root" ]; then
  probe=$skill_root
  while [ "$probe" != "/" ]; do
    if [ -f "$probe/AGENTS.md" ] && [ -d "$probe/.agents" ]; then repo_root=$probe; break; fi
    probe=$(dirname -- "$probe")
  done
fi
if [ -z "$repo_root" ]; then echo "ERROR: repository root not found above $skill_root" >&2; exit 2; fi

codex_root=${CODEX_HOME:-"$HOME/.codex"}
renderer_release=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["renderer"]["package_version"])' "$lock")
expected_renderer_sha=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["renderer"]["sha256"])' "$lock")
renderer="$codex_root/plugins/cache/openai-primary-runtime/documents/$renderer_release/skills/documents/render_docx.py"
core_skill="$repo_root/.agents/skills/family-law-service-pages"
soffice_dir="$core_skill/.tools/LibreOffice.app/Contents/MacOS"
python_bin="$core_skill/.venv/bin/python"
output_dir=""
expect_output_dir=0

for argument in "$@"; do
  if [ "$expect_output_dir" -eq 1 ]; then output_dir=$argument; expect_output_dir=0; continue; fi
  case "$argument" in
    --output_dir) expect_output_dir=1 ;;
    --output_dir=*) output_dir=${argument#--output_dir=} ;;
  esac
done

if [ ! -f "$renderer" ]; then
  echo "ERROR: Pinned Codex renderer $renderer_release was not found at $renderer" >&2; exit 2
fi
actual_renderer_sha=$(shasum -a 256 "$renderer" | awk '{print $1}')
if [ "$actual_renderer_sha" != "$expected_renderer_sha" ]; then
  echo "ERROR: Pinned Codex renderer SHA-256 mismatch: $actual_renderer_sha (expected $expected_renderer_sha)" >&2; exit 2
fi
if [ ! -x "$soffice_dir/soffice" ]; then
  echo "ERROR: Isolated LibreOffice is missing at $soffice_dir/soffice (run the Core skill's setup-renderer-macos.sh)" >&2; exit 2
fi
if [ ! -x "$python_bin" ]; then
  echo "ERROR: Isolated Python environment is missing at $python_bin" >&2; exit 2
fi
if ! "$python_bin" -c 'import fitz' 2>/dev/null; then
  echo "ERROR: PyMuPDF is not importable from $python_bin" >&2; exit 2
fi
if [ "$expect_output_dir" -eq 1 ] || [ -z "$output_dir" ]; then
  echo "ERROR: An explicit --output_dir is required by the render contract." >&2; exit 2
fi
if [ -d "$output_dir" ] && [ -n "$(find "$output_dir" -mindepth 1 -maxdepth 1 -print -quit)" ]; then
  echo "ERROR: Render output directory must be absent or empty: $output_dir" >&2; exit 2
fi
if [ -e "$output_dir" ] && [ ! -d "$output_dir" ]; then
  echo "ERROR: Render output path exists and is not a directory: $output_dir" >&2; exit 2
fi

echo "INFO: rendering with pinned Codex renderer $renderer_release (sha256 ${actual_renderer_sha%????????????????????????????????????????????????}...) via isolated LibreOffice and PyMuPDF" >&2
PATH="$soffice_dir:$PATH" PYTHONPATH="$skill_root/scripts/render_support" \
  "$python_bin" "$renderer" "$@"
