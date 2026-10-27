# Pixel HD house style: sharp HD pixel-art shorts

The owner's confirmed rules for every video in this repo (October 2026). They override older notes
and older projects; finished videos made before this date keep their original look.

## 1. Picture: SHARP HD pixel art

- **Sharp, not chunky.** Render at **360×640** (each art pixel = 3×3 screen pixels at 1080×1920), never the
  old 180×320 (6×6 blocks). This is the "HD pixel art" look (Stardew Valley / Celeste clarity): clearly
  pixel art, but every face, hand and object is easy to read. Don't go finer than 360×640: at 540×960 it
  stops looking like pixel art.
- **Light dithering only** (engine default `PX_DITHER = 6`). No dotted checkerboard noise on walls, skies
  or glows. Flat, bright, palette-locked colour areas.
- **Dark outline on every living character**: every human, animal, creature, god or monster. Draw them
  inside `character(function () { ... })`, which adds a 1-pixel dark outline around the silhouette
  automatically. Objects and backgrounds don't need outlines.
- **Big, readable characters**: the main character is about a third of the frame tall, with clear
  eyes and mouths (half-pixel coordinates give fine detail). They stand **below the caption band**
  (world y ≈ 150–172), never behind the text.
- Brightest colours that still read clearly; one accent colour for the key thing; small centred captions
  (black box, gold key word).

The engine (`videos/_engine/pixel-engine.js`) does all of this by default. `PX_RES = 1` and `PX_DITHER = 22`
bring back the old chunky look only if the owner asks for it.

## 2. Voice: narrate everything, with voices that fit

- **Every video is narrated.** Narration drives the story; captions follow the words.
- **Every character gets their own voice**, matched to who they are: age, gender, culture/accent,
  personality and size (lower pitch = bigger/older, higher = smaller/younger). The narrator matches the
  story's mood and setting (an Indian legend gets an Indian storyteller, a dark fairy tale a deep voice
  with reverb, an eerie story a hushed one).
- Never reuse one voice for two characters in the same video. Mouths flap with their own voice.
- Casting table: `videos/_engine/VOICES.md`. Engine: free Microsoft neural voices via `edge-tts`
  (`scripts/make_voices.py`), with word timings for the synced captions.

## 3. Sound: open-source sound effects, the best available

Every sound effect comes from **open-source / openly licensed** sources (`videos/_engine/osfx.py`), best first:

1. **Real CC0 recordings**: Kenney.nl packs (impacts, footsteps, doors, books, glass, metal, sci-fi, UI,
   jingles) and OpenGameArt CC0 packs (200 general SFX, 80 creature sounds, water/splash, bangs/fireworks,
   sci-fi, retro synth). 1,099 sounds, listed in `videos/_engine/SOUNDS.md`.
2. **Openverse** (Freesound and others), CC0 or CC BY only, cached and credited.
3. **Open-source generators**: jsfxr (classic sfxr 8-bit effects, Unlicense) and the repo's own numpy kits
   (`sfxlib.py` cinematic hits, `foley.py` story foley), layered under the recordings and used as fallbacks.

Layer them for cinematic, easy-to-hear sound: a real recording for the "what", a synth hit for the punch.
No sounds on captions. SFX duck under the voices. Target −12 to −17 dB mean, −1 dB peak. CC BY sounds are
listed in the project's `assets/sfx/CREDITS.md` and must be credited in the post caption.

## 4. Story and pacing

Hook in the first 1.5–2 s (the most shocking moment), rewind glitch into the story, a new picture every
2–4 s with moving camera, a twist near the end, and a literal loop (the last frame flows into the first).
Length follows the narration: 30–45 s for stories, 15–20 s for quick viral ones.

## 5. Making a new video

```bash
videos/_engine/new_video.sh <slug>      # starts from videos/_template (sharp engine, outlines, voices, open-source SFX)
```

`videos/style-sample/` is the reference: a narrator, a kid and a cat with their own voices, outlined,
sharp, with CC0 + sfxr sound. The full workflow is in `.claude/skills/pixel-short/SKILL.md`.
