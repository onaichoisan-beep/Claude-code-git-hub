---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Zeus vs Lord Shiva — an imagined cosmic duel that ends with neither god defeated."
destination: youtube / reels (landscape)
aspect: 1920x1080
language: en
length: 240s
angle: narrative
source: Zeus_vs_Shiva_AI_Pixel_Art_Production_Blueprint.pdf (owner's script, 48 units x 5 s)
---

## Intent

The owner's own 4-minute script, built as written: 48 five-second shots, 16:9, bright 16-bit pixel art,
**no on-screen text of any kind**, voice-over + sound effects, and a cliffhanger that cuts to black at 4:00.
This overrides the house 30 s vertical / SFX-only defaults because the script asks for it explicitly.

Mythology note (from the script): an imagined crossover, not a canonical event from either tradition.
Both deities are shown with dignity — Zeus forceful and aerial, Shiva composed and precise — and the
story never declares a winner. No injury detail: impacts are bright flashes and shield hits.

## Character anchors (constant in every shot)

- Zeus: white beard and hair, gold laurel, gold cuirass with ivory toga sash and pleated kilt, red cape,
  blue eyes, golden thunderbolt in the right hand, electric-blue lightning.
- Shiva: blue skin, matted jata with crescent moon, tripundra and third-eye mark, serpent and rudraksha,
  tiger-skin dhoti, trishul with damaru, cyan/violet aura.
- Screen direction: Zeus on the left facing right, Shiva on the right facing left (except where the
  script moves them, e.g. the pursuit in shot 14).

## Build

- `index.html` mounts a 320x180 world canvas (6x upscale) — `pixel-engine.js` in landscape mode
  (`PX_W`/`PX_H`), `chars.js` (palette, effects, the two rigs), `sets.js` (backdrops),
  `shots-a/b/c.js` (shots 1–16, 17–32, 33–48; each is `fn(u, t)` over its 5 s slot).
- Audio: `scripts/make_vo.sh` voices the 48 script lines with the local Kokoro TTS (`bm_george`),
  `scripts/synth_audio.py` builds the score bed + per-shot SFX from the script's sound notes, ducks them
  under the narration and cuts to silence with the picture at 4:00.
  Outputs `assets/audio/mix.wav` (used by the film) and `assets/audio/sfx_only.wav` (no narration).
