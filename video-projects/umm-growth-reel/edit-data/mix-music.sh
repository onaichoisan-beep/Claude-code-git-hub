#!/usr/bin/env bash
# Adds the BGM bed (Mixkit "Hip Hop 02", 97 BPM) under the rendered reel with voice-keyed ducking.
# usage: edit-data/mix-music.sh renders/<in>.mp4 renders/<out>.mp4 [music_gain_db]
set -euo pipefail
IN=$1; OUT=$2; G=${3:--7}
ffmpeg -nostdin -v error -y -i "$IN" -i assets/media/bgm-hiphop02.mp3 -filter_complex "
[0:a]aresample=48000,asplit=2[main][sc];
[1:a]aresample=48000,atrim=0:28.5,asetpts=N/SR/TB,volume=${G}dB,afade=t=in:d=0.25,afade=t=out:st=27.3:d=1.2[mus];
[mus][sc]sidechaincompress=threshold=0.05:ratio=3:attack=25:release=350:makeup=1[duck];
[main][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
