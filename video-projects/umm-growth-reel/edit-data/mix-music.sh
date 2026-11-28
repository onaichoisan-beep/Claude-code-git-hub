#!/usr/bin/env bash
# v14 music design (client: "high lifted" vibe, BGM a little louder):
#  Track: Mixkit "Motivating Mornings" (120 BPM uplifting corporate), lighter section then lift at 12.12s.
#  - 0-11.7s   : lighter section under hook/card
#  - 11.7-13.0 : music out under "Our goal is simple." (designed silence)
#  - 13.0s     : the lift lands on the cut to full frame (sudden zoom-in)
#  - 13-32.67  : full energy ~11 dB under voice, carries through the end card, fades out with it
# usage: edit-data/mix-music.sh <in.mp4> <out.mp4> [intro_gain_db] [main_gain_db]
set -euo pipefail
IN=$1; OUT=$2; GA=${3:--4.7}; GB=${4:--9.8}; M=assets/media/bgm-motivating-mornings.mp3
ffmpeg -nostdin -v error -y -i "$IN" -i "$M" -filter_complex "
[0:a]aresample=48000,asplit=2[main][sc];
[1:a]aresample=48000,asplit=2[m1][m2];
[m1]atrim=0.3:12.0,asetpts=N/SR/TB,volume=${GA}dB,afade=t=out:st=11.5:d=0.2[intro];
[m2]atrim=12.12:31.4,asetpts=N/SR/TB,volume=${GB}dB,afade=t=out:st=17.52:d=1.75,adelay=12980|12980[lift];
[intro][lift]amix=inputs=2:normalize=0:duration=longest,apad,atrim=0:32.267[mus];
[mus][sc]sidechaincompress=threshold=0.1:ratio=2:attack=30:release=400:makeup=1[duck];
[main][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
