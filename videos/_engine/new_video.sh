#!/usr/bin/env bash
# Start a new pixel short in the house style (STYLE_GUIDE.md): sharp HD pixel art, dark outlines on every
# living character, narration with character-matched voices, open-source sound effects.
#
#   videos/_engine/new_video.sh <slug>
#
# Creates videos/<slug>/ from videos/_template (a working 9 s sample to replace scene by scene) plus fresh
# copies of the shared engine and audio kits, so every project stays self-contained and re-renders identically.
set -euo pipefail
V="$(cd "$(dirname "$0")/.." && pwd)"
slug="${1:?usage: new_video.sh <slug>}"
dest="$V/$slug"
[ -e "$dest" ] && { echo "already exists: $dest" >&2; exit 1; }
(cd "$V" && npx hyperframes init "$slug" --non-interactive --example=blank --skill=faceless-explainer >/dev/null)
mkdir -p "$dest/scripts" "$dest/assets/audio" "$dest/assets/sfx" "$dest/renders"
cp "$V/_template/.gitignore" "$V/_template/index.html" "$V/_template/BRIEF.md" "$V/_template/CAPTION.md" "$dest/"
cp "$V/_template/scripts/lines.json" "$V/_template/scripts/voices.json" "$V/_template/scripts/synth_audio.py" "$dest/scripts/"
cp "$V/_engine/pixel-engine.js" "$dest/"
cp "$V/_engine/sfxlib.py" "$V/_engine/chiptune.py" "$V/_engine/foley.py" "$V/_engine/voicelib.py" "$V/_engine/osfx.py" \
   "$V/_engine/fetch_sfx.py" "$V/_engine/make_voices.py" "$dest/scripts/"
cat <<MSG
created $dest
next (from $dest):
  1. write scripts/lines.json ([speaker, text]) and cast scripts/voices.json (../_engine/VOICES.md)
  2. SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3 scripts/make_voices.py .
  3. edit CAPS + sound cues in scripts/synth_audio.py (python3 ../_engine/osfx.py find <word>), then run it
  4. replace the scenes in index.html (characters inside character(...)), set data-duration to window.DUR
  5. npx hyperframes snapshot --at <key moments> --no-end --describe false; fix; npx hyperframes check
  6. npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4
MSG
