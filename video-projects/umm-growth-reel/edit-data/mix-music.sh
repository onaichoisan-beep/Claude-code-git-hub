#!/usr/bin/env bash
# Adds a BGM bed under the rendered reel with light voice-keyed ducking.
# usage: edit-data/mix-music.sh <in.mp4> <out.mp4> [music_file] [music_offset_s] [music_gain_db]
# v11: assets/media/bgm-hiphop02.mp3 0 -7   |  v12: assets/media/bgm-cbpd.mp3 13.22 <calibrated>
set -euo pipefail
IN=$1; OUT=$2; M=${3:-assets/media/bgm-cbpd.mp3}; OFF=${4:-13.22}; G=${5:--5.2}
END=$(python3 -c "print($OFF+28.5)")
ffmpeg -nostdin -v error -y -i "$IN" -i "$M" -filter_complex "
[0:a]aresample=48000,asplit=2[main][sc];
[1:a]aresample=48000,atrim=${OFF}:${END},asetpts=N/SR/TB,volume=${G}dB,afade=t=in:d=0.05,afade=t=out:st=27.3:d=1.2[mus];
[mus][sc]sidechaincompress=threshold=0.05:ratio=3:attack=25:release=350:makeup=1[duck];
[main][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
