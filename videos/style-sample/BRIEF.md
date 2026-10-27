---
message: "The house style in 10 seconds: sharp HD pixel art, dark outlines on every character, a voice that fits each one, open-source sound."
destination: reference / reels
aspect: 1080x1920
length: 9.8s
---

## Intent

The reference video for the owner's house style (STYLE_GUIDE.md). It is also what `videos/_template` contains,
so every new video starts from a working, on-style project.

## Story (line → picture)

| Time | Beat |
|---|---|
| 0–3.0 | Sunset hill, flash. Narrator: "New house style. Sharp, clean pixels." A kid walks in on the grass |
| 3.5–6.0 | The kid waves: "And every character gets a dark outline!" Her outline flashes white with a gold sparkle |
| 6.0–8.1 | A cat leaps onto the rock, smug: "Plus a voice that actually fits." |
| 8.1–9.8 | She waves, flash, back to the start |

## Voices (../_engine/VOICES.md)

- Narrator: `en-US-AndrewMultilingualNeural` +6%, a warm, confident explainer
- Kid: `en-US-AnaNeural` +6%, a child voice for a child character
- Cat: `en-GB-RyanNeural` +12% −2 Hz, smug and British (the same cast as Mittens)

## Sound (open source)

CC0 recordings from the packs (`cc0_footstep_grass_*` Kenney, `cc0_impactPlate_heavy_002` and
`cc0_impactSoft_medium_001` Kenney, `cc0_cute_01` OpenGameArt creatures), jsfxr effects (`sfxr_powerUp_4`,
`sfxr_pickupCoin_11`, `sfxr_jump_21`), the HyperFrames library (whoosh-cinematic, sparkle, whoosh-short) and
synth wind + birdsong. All frozen in `assets/sfx/`; all CC0/Unlicense, so no credits are needed.
