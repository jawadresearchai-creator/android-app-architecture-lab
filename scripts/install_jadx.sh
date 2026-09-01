#!/usr/bin/env bash
set -euo pipefail

JADX_VERSION="1.5.6"
JADX_SHA256="545ea2be9c242511bc145755cf4bda2485ade42966e096f8b4d3da2a230e8974"
JADX_URL="https://github.com/skylot/jadx/releases/download/v${JADX_VERSION}/jadx-${JADX_VERSION}.zip"
DEST="${1:-$PWD/.tools/jadx}"
CACHE_DIR="${RUNNER_TEMP:-/tmp}/jadx-cache"
ZIP_PATH="$CACHE_DIR/jadx-${JADX_VERSION}.zip"

mkdir -p "$CACHE_DIR" "$DEST"

if [[ ! -f "$ZIP_PATH" ]]; then
  echo "Downloading JADX ${JADX_VERSION}..."
  curl --fail --location --retry 3 --retry-delay 2 "$JADX_URL" --output "$ZIP_PATH"
fi

echo "${JADX_SHA256}  ${ZIP_PATH}" | sha256sum --check --status || {
  echo "JADX archive checksum mismatch" >&2
  rm -f "$ZIP_PATH"
  exit 1
}

rm -rf "$DEST"/*
unzip -q "$ZIP_PATH" -d "$DEST"
chmod +x "$DEST/bin/jadx" "$DEST/bin/jadx-gui" 2>/dev/null || true

"$DEST/bin/jadx" --version
