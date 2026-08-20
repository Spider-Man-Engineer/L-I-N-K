#!/bin/bash
set -e

echo "Setting up Homebrew tap for link..."
echo ""
echo "To install link via Homebrew, you need to:"
echo ""
echo "1. Create a GitHub repo named 'link'"
echo "2. Push this project to it"
echo "3. Create a release tagged v0.1.0"
echo "4. Run these commands:"
echo ""
echo "   brew tap nerf/link"
echo "   brew install link"
echo ""
echo "Or install directly from a local formula:"
echo ""
echo "   brew install --formula homebrew-link/Formula/link.rb"
echo ""
