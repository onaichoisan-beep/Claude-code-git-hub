#!/usr/bin/env bash
# One-time setup: Python env + audio tools + offline voice models (~1 GB).
set -euo pipefail
cd "$(dirname "$0")"
VENV=${VENV:-/opt/alab}
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q -r requirements.txt
"$VENV/bin/pip" install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu
"$VENV/bin/pip" install -q demucs

mkdir -p voices/kokoro voices/piper
K=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s voices/kokoro/kokoro-v1.0.onnx ] || curl -sSL -o voices/kokoro/kokoro-v1.0.onnx $K/kokoro-v1.0.onnx
[ -s voices/kokoro/voices-v1.0.bin ]  || curl -sSL -o voices/kokoro/voices-v1.0.bin  $K/voices-v1.0.bin

for v in en_US/ryan/high en_US/lessac/high en_US/joe/medium en_US/amy/medium \
         en_US/hfc_male/medium en_GB/alan/medium en_US/libritts_r/medium; do
  n=$(echo "$v" | awk -F/ '{print $1"-"$2"-"$3}')
  for e in onnx onnx.json; do
    [ -s "voices/piper/$n.$e" ] || curl -sSL -o "voices/piper/$n.$e" \
      "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/$v/$n.$e"
  done
done
echo "Ready. Try: $VENV/bin/python scripts/tts.py --list kokoro"
