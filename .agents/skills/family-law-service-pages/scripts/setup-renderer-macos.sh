#!/bin/sh
# Install the pinned LibreOffice renderer dependency inside this skill only.
set -eu

skill_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tools_dir="$skill_root/.tools"
app_path="$tools_dir/LibreOffice.app"
dmg_path="$tools_dir/LibreOffice_26.8.0_MacOS_aarch64.dmg"
source_url="https://download.documentfoundation.org/libreoffice/stable/26.8.0/mac/aarch64/LibreOffice_26.8.0_MacOS_aarch64.dmg"
expected_sha="8858d8058da4f862f47559486814e65efc27294da67c5e4bb56b006b1ee59f89"
mount_dir=$(mktemp -d /private/tmp/core-hub-libreoffice.XXXXXX)
mounted=0

cleanup() {
  if [ "$mounted" -eq 1 ]; then
    hdiutil detach "$mount_dir" -quiet || true
  fi
  rmdir "$mount_dir" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

mkdir -p "$tools_dir"
if [ -x "$app_path/Contents/MacOS/soffice" ]; then
  echo "Isolated LibreOffice already installed: $app_path"
  exit 0
fi

curl --fail --location --output "$dmg_path" "$source_url"
actual_sha=$(shasum -a 256 "$dmg_path" | awk '{print $1}')
if [ "$actual_sha" != "$expected_sha" ]; then
  echo "ERROR: LibreOffice DMG SHA-256 mismatch: $actual_sha" >&2
  exit 1
fi

hdiutil attach "$dmg_path" -nobrowse -readonly -mountpoint "$mount_dir" -quiet
mounted=1
ditto "$mount_dir/LibreOffice.app" "$app_path.installing"
mv "$app_path.installing" "$app_path"
rm "$dmg_path"
echo "Installed isolated LibreOffice: $app_path"
