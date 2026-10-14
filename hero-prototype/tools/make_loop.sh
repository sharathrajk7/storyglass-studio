#!/usr/bin/env bash
# Make the 6-second silent crystal loop and its poster for a new film.
#
#   tools/make_loop.sh <film.mp4> <id> [start-seconds] [crop]
#
#   id             short name used in films.json, e.g. "acme-demo"
#   start-seconds  where the loop starts (default 10); pick a moment with motion
#   crop           optional ffmpeg crop for letterboxed films, e.g. 2844:1600:498:280
#
# Writes media/<id>.mp4 (960x540, ~150-400 KB) and media/<id>.jpg next to page.html.
set -euo pipefail

if [ $# -lt 2 ]; then
  sed -n '2,10p' "$0"
  exit 1
fi

src="$1"
id="$2"
start="${3:-10}"
crop="${4:-}"
media="$(cd "$(dirname "$0")/.." && pwd)/media"
mkdir -p "$media"

filter="scale=960:540:force_original_aspect_ratio=increase,crop=960:540,fps=30"
[ -n "$crop" ] && filter="crop=$crop,$filter"

ffmpeg -v error -y -ss "$start" -t 6 -i "$src" -vf "$filter" -an \
  -c:v libx264 -preset slow -crf 27 -pix_fmt yuv420p -movflags +faststart "$media/$id.mp4"
ffmpeg -v error -y -i "$media/$id.mp4" -frames:v 1 -q:v 4 "$media/$id.jpg"

echo "Made media/$id.mp4 and media/$id.jpg"
echo "Next: add an entry with \"id\": \"$id\" to films.json and paste the full-film link into \"full\"."
