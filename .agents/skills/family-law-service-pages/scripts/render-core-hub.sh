#!/bin/sh
# LOCAL WRAPPER: run Codex's packaged renderer with isolated project tooling.
set -eu

skill_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
codex_root=${CODEX_HOME:-"$HOME/.codex"}
renderer_release="26.819.11345"
renderer="$codex_root/plugins/cache/openai-primary-runtime/documents/$renderer_release/skills/documents/render_docx.py"
expected_renderer_sha="d8fe979f76e11215e146e53484bb4cb4e5f3906b58debed6844171073b187286"
soffice_dir="$skill_root/.tools/LibreOffice.app/Contents/MacOS"
python_bin="$skill_root/.venv/bin/python"
output_dir=""
expect_output_dir=0

for argument in "$@"; do
  if [ "$expect_output_dir" -eq 1 ]; then
    output_dir=$argument
    expect_output_dir=0
    continue
  fi
  case "$argument" in
    --output_dir)
      expect_output_dir=1
      ;;
    --output_dir=*)
      output_dir=${argument#--output_dir=}
      ;;
  esac
done

if [ ! -f "$renderer" ]; then
  echo "ERROR: Pinned Codex renderer was not found at $renderer" >&2
  exit 2
fi
actual_renderer_sha=$(shasum -a 256 "$renderer" | awk '{print $1}')
if [ "$actual_renderer_sha" != "$expected_renderer_sha" ]; then
  echo "ERROR: Pinned Codex renderer SHA-256 mismatch: $actual_renderer_sha" >&2
  exit 2
fi
if [ ! -x "$soffice_dir/soffice" ]; then
  echo "ERROR: Isolated LibreOffice is missing at $soffice_dir/soffice" >&2
  exit 2
fi
if [ ! -x "$python_bin" ]; then
  echo "ERROR: Isolated Python environment is missing at $python_bin" >&2
  exit 2
fi
if [ "$expect_output_dir" -eq 1 ] || [ -z "$output_dir" ]; then
  echo "ERROR: An explicit --output_dir is required by the local Core render contract." >&2
  exit 2
fi
if [ -d "$output_dir" ] && [ -n "$(find "$output_dir" -mindepth 1 -maxdepth 1 -print -quit)" ]; then
  echo "ERROR: Render output directory must be absent or empty: $output_dir" >&2
  exit 2
fi
if [ -e "$output_dir" ] && [ ! -d "$output_dir" ]; then
  echo "ERROR: Render output path exists and is not a directory: $output_dir" >&2
  exit 2
fi

PATH="$soffice_dir:$PATH" PYTHONPATH="$skill_root/scripts/render_support" \
  "$python_bin" "$renderer" "$@"
