#!/bin/bash
set -euo pipefail

REPO="FloorTech/Floor-Browse"
INSTALL_DIR="/opt/floor-browse"
BIN_NAME="floor-browse"
LINK_PATH="/usr/local/bin/$BIN_NAME"

echo "▶ Fetching latest release info..."
LATEST_URL=$(curl -sL "https://api.github.com/repos/$REPO/releases/latest" \
  | grep "browser_download_url" \
  | grep "linux.tar.gz" \
  | cut -d '"' -f 4)

if [ -z "$LATEST_URL" ]; then
  echo "❌ Could not find a suitable Linux release tarball."
  exit 1
fi

FILENAME=$(basename "$LATEST_URL")
TMP_DIR=$(mktemp -d)

echo "⬇ Downloading $FILENAME..."
curl -L "$LATEST_URL" -o "$TMP_DIR/$FILENAME"

echo "📦 Extracting to $INSTALL_DIR..."
sudo mkdir -p "$INSTALL_DIR"
sudo tar -xzf "$TMP_DIR/$FILENAME" -C "$INSTALL_DIR"

echo "🔗 Creating symlink to $BIN_NAME in $LINK_PATH..."
sudo ln -sf "$INSTALL_DIR/$BIN_NAME" "$LINK_PATH"

echo "✅ Done! You can now run '$BIN_NAME' from anywhere to open Floor Browse."