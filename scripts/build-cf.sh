#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist
cp -R deploy/public/. dist/
cp cloudflare/_headers dist/_headers
