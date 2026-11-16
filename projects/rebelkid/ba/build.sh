#!/bin/bash
# usage: ba/build.sh "Video/RebelKid v2.mp4" "Video/RebelKid v2 - Before After.mp4"
ffmpeg -v error -n -loop 1 -framerate 30 -i ba/bg.png -i src/aroll.mp4 -i "$1" -i ba/sh.png -loop 1 -i ba/mask_before.png -loop 1 -i ba/mask_after.png -filter_complex "\
[1:v]scale=394:700:flags=lanczos,format=rgba[b0];[4:v]format=gray[mb];[b0][mb]alphamerge[b];\
[2:v]scale=520:926:flags=lanczos,format=rgba[a0];[5:v]format=gray[ma];[a0][ma]alphamerge[a];\
[0:v][b]overlay=90:609:shortest=1[x1];[x1][3:v]overlay=0:0[x2];[x2][a]overlay=455:497,format=yuv420p[v]" \
-map "[v]" -map 2:a -t 85.567 -c:v libx264 -crf 16 -preset medium -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart "$2"
