#!/usr/bin/env bash
# Reference-matched music design (from stem analysis of the two reference reels):
#  - 0-11.7s : C.B.P.D soft intro (no drums) under the hook/card section, ~15 dB under voice
#  - 11.7-13.0: music OUT (designed silence under "Our goal is simple." like ref 1's pocket-watch beat)
#  - 13.0s   : beat DROP lands exactly on the cut to full frame (track drop at 13.24s)
#  - 13-28.5 : full beat ~15 dB under voice, light ducking, fades with the picture
# usage: edit-data/mix-music.sh <in.mp4> <out.mp4> [intro_gain_db] [beat_gain_db]
set -euo pipefail
IN=$1; OUT=$2; GA=${3:--3.8}; GB=${4:--13.1}; M=assets/media/bgm-cbpd.mp3
ffmpeg -nostdin -v error -y -i "$IN" -i "$M" -filter_complex "
[0:a]aresample=48000,asplit=2[main][sc];
[1:a]aresample=48000,asplit=2[m1][m2];
[m1]atrim=0.24:11.94,asetpts=N/SR/TB,volume=${GA}dB,afade=t=in:d=0.3,afade=t=out:st=11.5:d=0.2[intro];
[m2]atrim=13.22:28.74,asetpts=N/SR/TB,volume=${GB}dB,afade=t=out:st=14.7:d=0.82,adelay=12980|12980[beat];
[intro][beat]amix=inputs=2:normalize=0:duration=longest,apad,atrim=0:28.5[mus];
[mus][sc]sidechaincompress=threshold=0.1:ratio=2:attack=30:release=400:makeup=1[duck];
[main][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
