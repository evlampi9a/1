#!/usr/bin/env bash
# Проверка готового ролика перед отправкой: формат, длительность, контактный лист.
#   tools/qc.sh <video.mp4> <expectedW> <expectedH> [maxSeconds=30]
# Пишет <video>.contact.jpg (3×3 кадра) — ОБЯЗАТЕЛЬНО посмотреть его глазами (Read) перед отправкой.
set -euo pipefail
f="$1"; ew="$2"; eh="$3"; max="${4:-30}"
read -r w h < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$f" | tr x ' ')
d="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")"
ok=1
[[ "$w" == "$ew" && "$h" == "$eh" ]] || { echo "FAIL size ${w}x${h}, expected ${ew}x${eh}"; ok=0; }
awk -v d="$d" -v m="$max" 'BEGIN{exit !(d<=m+0.05)}' || { echo "FAIL duration ${d}s > ${max}s"; ok=0; }
awk -v d="$d" 'BEGIN{exit !(d>=8)}' || { echo "FAIL duration ${d}s is suspiciously short"; ok=0; }
n=9; step="$(awk -v d="$d" -v n="$n" 'BEGIN{printf "%.3f", d/n}')"
tw=$(( w > h ? 480 : 270 ))
ffmpeg -loglevel error -y -i "$f" -vf "fps=1/${step},scale=${tw}:-2,tile=3x3:padding=6:color=black" -frames:v 1 "${f%.*}.contact.jpg"
size="$(du -h "$f" | cut -f1)"
echo "$( [[ $ok == 1 ]] && echo OK || echo CHECK ) ${w}x${h} ${d}s ${size} contact: ${f%.*}.contact.jpg"
[[ $ok == 1 ]]
