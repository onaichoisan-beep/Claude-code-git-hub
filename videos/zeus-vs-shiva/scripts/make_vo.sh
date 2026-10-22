#!/bin/bash
# Generates the 48 voice-over lines with the local Kokoro TTS (deep British male voice).
cd "$(dirname "$0")/.."
i=0
while IFS= read -r line; do
  i=$((i+1)); n=$(printf "%02d" $i)
  npx hyperframes tts "$line" -v bm_george -s 0.95 -o assets/audio/vo/vo$n.wav --json | tail -1
done < scripts/vo_lines.txt
