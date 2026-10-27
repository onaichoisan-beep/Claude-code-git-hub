---
name: pixel-short
description: Make a viral 15–30-second vertical pixel-art science, mythology or fiction short in the owner's established style (bright pixel art, cold-open hook, small centred key-fact captions, cinematic sound effects only, loop ending), built with the shared engine in videos/_engine. Use for any "make a video about X" request in this repo, and for writing the matching Instagram caption.
---

# Pixel short — the owner's house style

The owner makes ~30s Instagram Reels / Shorts. Everything below is their confirmed preference,
learned over many videos (see `videos/` for 15+ finished examples). Follow it without re-asking.

## How to work with the owner

- **Don't ask questions. Don't run storyboard/sketch review checkpoints.** Build, find every fault
  yourself (snapshot key moments, look at them, fix, re-snapshot), render, verify, then deliver.
  They said: "I don't want to answer any of your questions… find every fault… deliver me the videos."
- Make the **complete story** start to finish — never half a story.
- Facts must be accurate and sourced; hedge where the science is uncertain. Avoid misinformation,
  gore (imply violence with a white flash), and anything that would get flagged.
- When done: send the MP4(s), summarise the story beat by beat, note any fixes and fact corrections,
  and include an **Instagram caption** in their format (below). Commit and push.

## The look

- 9:16, **1080×1920 @ 30fps, 30.0s exactly** for explainers; **15–20s** when the owner asks for short
  viral ones (hook 0–1.5s, rewind, 3–5 beats of ~3s, twist, loop). World canvas **180×320** upscaled 6×, captions on a
  **360×640** layer upscaled 3×. Palette-locked + 4×4 Bayer dither (the engine does this).
- **Brightest colours possible** that still read clearly; one accent colour per video for the key thing.
- **Text: only important facts, small, centred in the middle of the frame** (engine default, scale 2,
  black box, gold for the key word). 1–3 short lines. Frame every scene so the action sits
  **below/around** the caption band (world y≈150–172) — never behind it. Use `cam.y` ≈ object_y − 70.
- Optional upper-left **counter/timeline box** when time matters (Big Bang timeline, hours awake) via `cfg.ui`.

## The pacing (viral format)

1. **Hook in the first 1.5–2s**: cold open on the most shocking moment (flash, shake, boom) + one punchy line.
2. **Rewind glitch** (`glitchRows`) into the story at ~1.6s.
3. A new beat every **2–4s**, continuous camera moves (zooms/dives/pull-backs), scene changes via dither dissolve.
4. Twist near the end ("Hanu means jaw", "Blue is the hardest to make", "Don't try this").
5. **Loop**: the last frame returns to the hook so replays are seamless.

## Sound

- **Sound effects only by default.** No narration unless the owner asks for it in that request (they did
  for e.g. "2 of the 5 narrated"). Never put sounds on captions/text.
- **Narration, when asked:** `cp ../_engine/make_voices.py scripts/`, write `scripts/lines.json`
  ([speaker, text]) + `scripts/voices.json` ({speaker: [voice, rate, pitch]}), run
  `python3 scripts/make_voices.py .` (edge-tts, word timings), then a synth_audio that places lines at
  fixed SLOTS, ducks SFX under the voice and writes word-synced `captions.js` (copy
  `../dream-film-crew/scripts/synth_audio.py`). Voices that worked: playful/insider →
  en-US-AndrewMultilingualNeural +10%; epic trailer → en-US-ChristopherNeural −4%, −12 Hz + low boost and
  hall reverb; casual human → en-US-EmmaMultilingualNeural; shouty director → en-US-GuyNeural.
- **Real foley** to sit on top of the procedural kit: `python3 ../_engine/fetch_sfx.py . name="query" ...`
  (Openverse CC0/CC BY, slow and flaky; run it in the background) → `assets/sfx/<name>.wav` + CREDITS.md.
  **Check every pick's title** (searches return wrong sounds, e.g. "sizzle" → cabinets): delete bad ones and
  run `python3 ../_engine/prune_credits.py .`. Load with `load()` and always give a procedural fallback.
  The bundled HyperFrames library (`LIB`: whoosh, whoosh-short, whoosh-cinematic, pop, sparkle, glitch-1/2/3,
  notification, error, chime, riser, impact-bass-1/2, ping, click, typing) is available offline.
- **Narrated fables (35–45s, when the owner asks for story + narration):** `_engine/voicelib.py` (lay out
  lines, word-synced captions with `|` line breaks, ducking, final limiter) + `_engine/foley.py` (synth
  foley: sea, splash, sizzle, boil, creak, gull, crickets, wind, ice, fire, fireworks, meow, purr, tick,
  gears, page flips, whispers, glass, rumble…). Copy `../clockmaker-one-second/scripts/` as the template.
  Voices that worked: Indian storyteller en-IN-PrabhatNeural −3% −3 Hz; Indian woman
  en-IN-NeerjaExpressiveNeural; smug cat en-GB-RyanNeural +12%; hushed librarian en-GB-SoniaNeural −6%;
  dark fairy tale en-US-ChristopherNeural −4% −4 Hz + low boost + hall; child en-GB-MaisieNeural.
  Openverse often times out (504s): don't wait on it. Reuse CC0/CC BY files other projects already
  fetched (copy their CREDITS.md lines) and lean on `LIB` + the synth kit.
- Cinematic and easy to hear: impacts, braams, taiko drum rolls, risers, sub drops, conch, gong,
  bells, roars, whooshes, story-specific foley. Exception: calm/awe topics (e.g. the Big Bang) use
  **soft ambient** sound, no booms. Target ~ −12 to −17 dB mean, −1 dB peak.
- Built procedurally in `scripts/synth_audio.py` using `scripts/sfxlib.py` (`Bus`, `master`, and the
  kit: `impact braam taiko conch gong sub_drop rewind drum_roll roar shing bell blip thump sweep riser
  bubble heartbeat noise_hit reverb seg add`). You cannot listen; verify levels with ffmpeg volumedetect.

## Build recipe

```bash
npx hyperframes init "videos/<slug>" --non-interactive --example=blank --skill=faceless-explainer
cd videos/<slug>
cp ../cracking-knuckles/.gitignore . && mkdir -p scripts assets/audio
cp ../_engine/pixel-engine.js . && cp ../_engine/sfxlib.py scripts/
# write index.html (copy the structure of a finished video, e.g. ../narasimha-loophole/index.html):
#   palette C → scene functions → PX.setup(C, {scenes, sceneAt, cuts, post, captions, ui?}) → GSAP proxy
# write scripts/synth_audio.py, then:
python3 scripts/synth_audio.py
npx hyperframes snapshot --at <12 key moments> --no-end --describe false   # look at the contact sheet, fix, repeat
npx hyperframes check
npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4
ffprobe … ; ffmpeg -i renders/video.mp4 -af volumedetect -f null -   # verify 30.0s + levels
```

Engine notes (`videos/_engine/pixel-engine.js`): everything is a pure function of `t` (no Math.random,
use `rng(seed)` / `hash1`). Helpers: `camAt shake setCam screen disc ell line rect rrect poly vgrad
vignette worldText glow lighter normalBlend glitchRows tintImg mix`. `glow()` and `hex()` need **hex**
colours — passing an `rgb()` string from `mix()` throws and freezes frames. Always reset
`normalBlend()` after `lighter()`. Write a short `BRIEF.md` (message, story, sources) per project.

## Instagram caption format

```
<Title> 🎧

<Hook question>? <One-line answer.>

<Short paragraph walking through what the video shows, with real numbers.>

Sources: <Source 1>; <Source 2>; <Source 3>

#<topic> #<topic> #<science|mythology> #pixelart
```

## Topic taste

Fiction works too: the owner asked for surreal "what if" concepts with loops (Who's Fishing Who, Raindrop
Race, Your Dream's Film Crew, The Last Pixel, Ant Everest). For fiction, keep captions to the hook and
the twist (or word-synced narration) and make the loop literal (the end flows back into the hook).

Viral "what happens if / to your body" science, space news, myth-busters, and Indian mythology
(Narasimha, Hanuman, Neelkanth, Ravana…), timed to festivals (Diwali, Dussehra) when possible.
Ideas not yet made: Samudra Manthan, Ganesha's head, Ganesha's broken tusk, Ganga's descent, Krishna
lifts Govardhan, Vishnu's avatars, Shiva's third eye, Brahma's few temples, drowning doesn't look like
drowning, hot car in 10 minutes, tired driving = drunk driving, stabbed by a knife, tattoo needle,
ice water, mosquito bite, heart attack, hottest pepper, broken bone, choking, 3I/ATLAS, Mars canyon.
