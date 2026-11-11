#!/usr/bin/env bash
# Скачать ассет ZenCreator по presigned URL и подготовить его как слой футажа для bang-motion.
#   tools/fetch_clip.sh <download_url> <out.mp4|out.png> [W H]
# Видео → H.264 yuv420p, без звука, +faststart, кадрирование cover под W×H (по умолчанию без изменения размера).
# Картинка → сохраняется как есть (PNG/JPEG/WebP), браузер её покажет.
# URL подписанный и живёт несколько минут — вызывать сразу после zencreator_get_asset_download_url(s).
set -euo pipefail
url="$1"; out="$2"; W="${3:-}"; H="${4:-}"
mkdir -p "$(dirname "$out")"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
curl -fsSL --retry 3 --retry-delay 2 -o "$tmp/src" "$url"
kind="$(file -b --mime-type "$tmp/src")"
case "$kind" in
  video/*)
    vf="format=yuv420p"
    if [[ -n "$W" && -n "$H" ]]; then vf="scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},${vf}"; fi
    ffmpeg -loglevel error -y -i "$tmp/src" -vf "$vf" -c:v libx264 -preset medium -crf 18 -an -movflags +faststart "$out"
    ;;
  image/*) cp "$tmp/src" "$out" ;;
  *) echo "unexpected media type: $kind" >&2; exit 1 ;;
esac
ffprobe -v error -show_entries stream=codec_name,width,height:format=duration -of compact=p=0:nk=0 "$out" | head -2
