#!/bin/bash
set -e

G='\033[1;32m'
D='\033[2;32m'
B='\033[1m'
R='\033[0m'

INSTALL_DIR="$HOME/.local/share/lnk"
BIN_DIR="$HOME/.local/bin"

echo ""
echo -e "${G}      ██╗     ██╗███╗   ██╗██╗  ██╗${R}"
echo -e "${G}      ██║     ██║████╗  ██║██║ ██╔╝${R}"
echo -e "${G}      ██║     ██║██╔██╗ ██║█████╔╝ ${R}"
echo -e "${G}      ██║     ██║██║╚██╗██║██╔═██╗ ${R}"
echo -e "${G}      ███████╗██║██║ ╚████║██║  ██╗${R}"
echo -e "${G}      ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝${R}"
echo -e "${D}      Live Instant Network Kommunication${R}"
echo ""

# Remove old system-level install if present
sudo rm -f /usr/local/bin/link /usr/local/bin/lnk 2>/dev/null || true
sudo rm -rf /usr/local/share/link /usr/local/share/lnk 2>/dev/null || true

echo -e "  ${G}▸${R} ${B}Installing lnk...${R}"

mkdir -p "${INSTALL_DIR}"
mkdir -p "${BIN_DIR}"

cp "$(dirname "$0")/lnk" "${INSTALL_DIR}/"
cp "$(dirname "$0")/server.py" "${INSTALL_DIR}/"
cp "$(dirname "$0")/client.py" "${INSTALL_DIR}/"
chmod +x "${INSTALL_DIR}/lnk"

ln -sf "${INSTALL_DIR}/lnk" "${BIN_DIR}/lnk"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo -e "  ${B}Add this to your shell profile (~/.zshrc or ~/.bash_profile):${R}"
    echo -e "  ${D}export PATH=\"\$HOME/.local/bin:\$PATH\"${R}"
    echo ""
fi

echo ""
echo -e "  ${G}✓ Installed successfully!${R}"
echo ""
echo -e "  ${B}Usage:${R}"
echo -e "    ${D}lnk server${R}              Start the chat server"
echo -e "    ${D}lnk create${R}              Create a room and get an invite code"
echo -e "    ${D}lnk start${R}               Open the interactive menu"
echo -e "    ${D}lnk join <CODE>${R}         Join a room by invite code"
echo ""
