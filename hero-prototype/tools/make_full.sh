#!/usr/bin/env bash
# Make a web version of a full film for the player: 720p H.264 + AAC, loudness set to
# -14 LUFS with peaks under -1.5 dBTP, sized to stay under ~14 MB (the preview link's
# per-file limit is 15 MB). The real site streams from Gumlet instead.
#
#   tools/make_full.sh <film.mp4> <id>
set -euo pipefail

src="$1"
id="$2"
here="$(cd "$(dirname "$0")/.." && pwd)"
out="$here/media/full"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
mkdir -p "$out"

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")
# video bitrate (kbit/s) so video + 96k audio lands near 14 MiB
vb=$(python3 -c "d=float('$dur'); print(int(min(2500, (14.0*8*1024*1024/d - 96000)/1000)))")

# pass 1 of the loudness fix: measure
stats=$(ffmpeg -hide_banner -nostats -i "$src" -vn -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
read -r mi mtp mlra mth off < <(python3 -c "
import json,sys; j=json.loads(sys.stdin.read())
print(j['input_i'], j['input_tp'], j['input_lra'], j['input_thresh'], j['target_offset'])" <<<"$stats")
af="loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$mi:measured_TP=$mtp:measured_LRA=$mlra:measured_thresh=$mth:offset=$off:linear=true,aresample=48000"

vf="scale=1280:720:flags=lanczos,fps=30"
x264="aq-mode=3:aq-strength=0.9"
ffmpeg -v error -y -i "$src" -vf "$vf" -c:v libx264 -preset slow -b:v "${vb}k" -x264-params "$x264" \
  -pass 1 -passlogfile "$work/p" -an -f null /dev/null
ffmpeg -v error -y -i "$src" -vf "$vf" -c:v libx264 -preset slow -b:v "${vb}k" -maxrate "$((vb * 16 / 10))k" \
  -bufsize "$((vb * 2))k" -x264-params "$x264" -pass 2 -passlogfile "$work/p" -pix_fmt yuv420p \
  -af "$af" -c:a aac -b:a 96k -movflags +faststart "$out/$id.mp4"

size=$(stat -f %z "$out/$id.mp4" 2>/dev/null || stat -c %s "$out/$id.mp4")
echo "$id: ${vb}k video, $((size / 1024)) KB, was ${mi} LUFS / ${mtp} dBTP"
