#!/usr/bin/env bash
# Rebuilds the `hostinger` branch from deploy/public/ (+ .htaccess) and pushes it.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
TMP="$(mktemp -d)"
cp -R "$ROOT/deploy/public/." "$TMP/"
cp "$ROOT/deploy/hostinger.htaccess" "$TMP/.htaccess"
cd "$TMP"
git init -q -b hostinger
git add -A
git commit -q -m "Publish site build"
git push -f "$(git -C "$ROOT" remote get-url origin)" hostinger
rm -rf "$TMP"
