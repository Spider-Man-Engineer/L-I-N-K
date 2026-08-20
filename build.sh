#!/bin/bash
set -e

NAME="link"
VERSION="0.1.0"
TARBALL="${NAME}-${VERSION}.tar.gz"
FORMULA_DIR="$(dirname "$0")/homebrew-link/Formula"
PROJECT_DIR="$(dirname "$0")"

echo "Building ${NAME} ${VERSION}..."

BUILD_DIR=$(mktemp -d)
mkdir -p "${BUILD_DIR}/${NAME}-${VERSION}"

cp "${PROJECT_DIR}/lnk" "${BUILD_DIR}/${NAME}-${VERSION}/"
cp "${PROJECT_DIR}/server.py" "${BUILD_DIR}/${NAME}-${VERSION}/"
cp "${PROJECT_DIR}/client.py" "${BUILD_DIR}/${NAME}-${VERSION}/"

cd "${BUILD_DIR}"
tar czf "${PROJECT_DIR}/${TARBALL}" "${NAME}-${VERSION}"
cd "${PROJECT_DIR}"

SHA=$(shasum -a 256 "${PROJECT_DIR}/${TARBALL}" | awk '{print $1}')
echo "SHA256: ${SHA}"

sed -i '' "s|url .*|url \"https://github.com/Spider-Man-Engineer/L-I-N-K/archive/refs/tags/v${VERSION}.tar.gz\"|" "${FORMULA_DIR}/link.rb"
sed -i '' "s|sha256 .*|sha256 \"${SHA}\"|" "${FORMULA_DIR}/link.rb"

rm -rf "${BUILD_DIR}"

echo ""
echo "Tarball: ${PROJECT_DIR}/${TARBALL}"
echo "Formula: ${FORMULA_DIR}/link.rb"
echo ""
echo "Install via Homebrew:"
echo "  brew tap Spider-Man-Engineer/link"
echo "  brew install link"
echo ""
echo "Or from local formula:"
echo "  brew install --formula ${FORMULA_DIR}/link.rb"
