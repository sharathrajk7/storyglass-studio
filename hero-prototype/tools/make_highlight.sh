#!/usr/bin/env bash
# Make the crystal loop from a film's three best moments: 3 x 3.2 s, joined with soft
# 0.4 s fades, 960x540, silent (~8.8 s, a few hundred KB). Also writes the poster.
#
#   tools/make_highlight.sh <film.mp4> <id> <t1> <t2> <t3> [crop]
#
#   t1 t2 t3  start seconds of the three moments
#   crop      optional ffmpeg crop for letterboxed films, e.g. 2844:1600:498:280
set -euo pipefail

if [ $# -lt 5 ]; then
  sed -n '2,9p' "$0"
  exit 1
fi

src="$1"; id="$2"; t1="$3"; t2="$4"; t3="$5"; crop="${6:-}"
media="$(cd "$(dirname "$0")/.." && pwd)/media"
mkdir -p "$media"

pre="scale=960:540:force_original_aspect_ratio=increase,crop=960:540,fps=30,settb=AVTB,setpts=PTS-STARTPTS"
[ -n "$crop" ] && pre="crop=$crop,$pre"

ffmpeg -v error -y \
  -ss "$t1" -t 3.2 -i "$src" -ss "$t2" -t 3.2 -i "$src" -ss "$t3" -t 3.2 -i "$src" \
  -filter_complex "[0:v]$pre[a];[1:v]$pre[b];[2:v]$pre[c];[a][b]xfade=transition=fade:duration=0.4:offset=2.8[ab];[ab][c]xfade=transition=fade:duration=0.4:offset=5.6,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -preset slow -crf 27 -movflags +faststart "$media/$id.mp4"
ffmpeg -v error -y -i "$media/$id.mp4" -frames:v 1 -q:v 4 "$media/$id.jpg"

echo "Made media/$id.mp4 ($(( $(stat -f %z "$media/$id.mp4") / 1024 )) KB) and media/$id.jpg"
