#!/bin/bash
set -e

INSTALL_DIR="$HOME/.local/share/lnk"
BIN_DIR="$HOME/.local/bin"

echo "  _          _ "
echo " | |    __ _| | | __ _"
echo " | |   / _\` | | |/ _\` |"
echo " | |__| (_| | | | (_| |"
echo " |_____\\__,_|_|_|\\__,_|"
echo ""

# Remove old system-level install if present
sudo rm -f /usr/local/bin/link /usr/local/bin/lnk 2>/dev/null || true
sudo rm -rf /usr/local/share/link /usr/local/share/lnk 2>/dev/null || true

echo "Installing lnk..."

mkdir -p "${INSTALL_DIR}"
mkdir -p "${BIN_DIR}"

cp "$(dirname "$0")/lnk" "${INSTALL_DIR}/"
cp "$(dirname "$0")/server.py" "${INSTALL_DIR}/"
cp "$(dirname "$0")/client.py" "${INSTALL_DIR}/"
chmod +x "${INSTALL_DIR}/lnk"

ln -sf "${INSTALL_DIR}/lnk" "${BIN_DIR}/lnk"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "Add this to your shell profile (~/.zshrc or ~/.bash_profile):"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo ""
echo "Installed successfully! 🎉"
echo ""
echo "Usage:"
echo "  lnk server              Start the chat server"
echo "  lnk create              Create a room and get an invite code"
echo "  lnk start               Open the interactive menu"
echo "  lnk join <CODE>         Join a room by invite code"
echo ""
