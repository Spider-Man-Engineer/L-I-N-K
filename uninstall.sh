#!/bin/bash
set -e

INSTALL_DIR="$HOME/.local/share/lnk"
BIN_DIR="$HOME/.local/bin"

echo "Uninstalling lnk..."

rm -f "${BIN_DIR}/lnk"
rm -rf "${INSTALL_DIR}"

echo "Uninstalled successfully!"
