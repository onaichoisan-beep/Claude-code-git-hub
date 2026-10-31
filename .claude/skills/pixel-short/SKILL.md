---
name: pixel-short
description: Make a viral vertical pixel-art science, mythology or fiction short in the owner's house style (SHARP HD pixel art, dark outlines on every living character, NO narration (text cards + speech bubbles + sound only), open-source sound effects, cold-open hook, small centred captions, loop ending), built with the shared engine in videos/_engine. Use for any "make a video about X" request in this repo, and for writing the matching Instagram caption.
---

# Pixel HD — the owner's house style

The owner makes Instagram Reels / Shorts. Everything below is their confirmed preference,
learned over many videos (see `videos/` for 25+ finished examples; `videos/style-sample/` shows the
current look). The one-page rules are in `/STYLE_GUIDE.md`. Follow them without re-asking.

## How to work with the owner

- **Don't ask questions. Don't run storyboard/sketch review checkpoints.** Build, find every fault
  yourself (snapshot key moments, look at them, fix, re-snapshot), render, verify, then deliver.
  They said: "I don't want to answer any of your questions… find every fault… deliver me the videos."
- Make the **complete story** start to finish — never half a story.
- Facts must be accurate and sourced; hedge where the science is uncertain. Avoid misinformation,
  gore (imply violence with a white flash), and anything that would get flagged.
- When done: send the MP4(s), summarise the story beat by beat, note any fixes and fact corrections,
  and include an **Instagram caption** in their format (below). Commit and push.

## Engagement (owner's rule, Oct 31 2026): read STYLE_GUIDE.md section 6 first

Handle `@SCROLL2STUDY.IN` on every frame (engine does it), an 8-bit beat bed that never stops, a sound on every text card /
counter tick / cut (3+ hits per second), the main object as a character with a face, a live counter on screen the whole time,
one continuous camera journey, a call to action inside the video, and a perfect loop. Text-only (no narration) is the default.

## The look: SHARP HD pixel art (owner's rule, Oct 2026; full rules in /STYLE_GUIDE.md)

- 9:16, **1080×1920 @ 30fps**. Scenes are written in a **180×320 world**, rendered **sharp at 360×640**
  (3×3 screen px per art pixel) with a **light dither** — the engine defaults (`PX_RES 2`, `PX_DITHER 6`).
  The owner rated the old 180×320 + heavy dither look "too much pixel, not visually clear": never go back to it
  unless asked. Use half-pixel coordinates (0.5) for fine detail (eyes, highlights, whiskers, fingers).
- **Dark outline on every living character** (humans, animals, creatures, gods): draw them inside
  `character(function () { ... })` → automatic 1-pixel dark outline. Don't hand-draw ink underlays.
  `character(fn, { col, px })` changes the colour/thickness (e.g. a white flash outline on a reveal).
- **Big, readable characters** (main one ≈ a third of the frame tall), clear faces, mouths that flap with
  their own voice (`talk(who, t)` from `MOUTH`).
- **Brightest colours possible** that still read clearly; one accent colour per video for the key thing.
- **Text: only important words, small, centred in the middle of the frame** (engine default, scale 2,
  black box, gold for the key word), word-synced to the narration. Frame every scene so the action sits
  **below/around** the caption band (world y≈150–172) — never behind it. Use `cam.y` ≈ object_y − 70.
- Optional upper-left **counter/timeline box** when numbers matter (lives left, years, seconds) via `cfg.ui`.

## The pacing (viral format)

0. **Pick topics whose FIRST FRAME is the weird/disgusting fact itself** (owner, Oct 31 2026): a louse staring out of a
   fish's mouth, babies peeking out of holes in a toad's back, a fish sliding into a sea cucumber's butt. The first 2 s must
   make people stop; then the story explains how it got that way.
1. **No cold-open hook, no rewind glitch at the start** (owner's rule, Oct 31 2026): start straight in the story's flow;
   the first text card is the hook line.
2. (removed: the old 1.6 s rewind glitch)
3. A new beat every **2–4s**, continuous camera moves (zooms/dives/pull-backs), scene changes via dither dissolve.
4. Twist near the end ("Hanu means jaw", "Blue is the hardest to make", "Don't try this").
5. **Loop**: the last frame returns to the hook so replays are seamless.

## Voice: NO narration (owner's rule, Oct 31 2026: "don't add narration")

**Never add narration unless the owner explicitly asks for it.** Every video is text cards (3-6 words, gold keyword, a new
one every ~2 s) + speech bubbles for the characters + the 8-bit bed and sound effects (see `videos/zombie-ant-fungus`,
`videos/tongue-eating-louse`: `CT.write_captions` + `short-kit.js`). The rest of this section applies only when narration
is requested.


- **Every video is narrated**, and **every character speaks with their own voice that fits them** (age,
  gender, culture/accent, personality, size). The narrator fits the story's mood and setting. Never reuse a
  voice for two characters in one video. Casting table: `videos/_engine/VOICES.md`.
- `scripts/lines.json` = `[[speaker, text], ...]`, `scripts/voices.json` = `{speaker: [voice, rate, pitch]}`,
  then `SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3 scripts/make_voices.py .` (edge-tts + word timings).
- `scripts/synth_audio.py` (template in `videos/_template/scripts/`) lays lines out with `voicelib.py`,
  writes `captions.js` (`CAPS` word-synced captions with `|` line breaks, `VO` word times, `MOUTH` flaps,
  `BEATS` shared beat times), ducks SFX under the voices and limits the mix. Scenes key off `A(i)`,
  `WT(i, word)`, so a re-voice stays in sync. Length follows the narration (stories 30–45 s, quick ones 15–20 s).
- Add room to the narrator where it fits (hall reverb + low boost for epic/dark, light room for intimate).

## Sound: open-source sound effects (owner's rule)

- Every sound effect comes from **open-source / openly licensed** sources via `scripts/osfx.py`, best first:
  1. **CC0 recordings**: `osfx.sound(name)` — Kenney.nl + OpenGameArt packs, 1,099 sounds (footsteps,
     impacts, doors, books, glass, metal, coins, cards, sci-fi, creatures, water, bangs/fireworks, UI,
     jingles). Catalog: `videos/_engine/SOUNDS.md`; search: `python3 ../_engine/osfx.py find <word>`.
  2. **Openverse** (Freesound…, CC0 / CC BY only): `osfx.openverse(name, query, fallback=...)` — cached,
     credited, gives up fast when the API is down (it often is). Check what came back is the right sound.
  3. **Open-source generators**: `osfx.sfxr(preset, seed)` (jsfxr 8-bit: pickupCoin laserShoot explosion
     powerUp hitHurt jump blipSelect synth tone click random) and the numpy kits — `sfxlib.py` cinematic
     hits (`impact braam taiko conch gong sub_drop rewind drum_roll roar shing bell blip thump sweep riser
     bubble heartbeat noise_hit reverb`) and `foley.py` story foley (sea, splash, sizzle, boil, creak, gull,
     crickets, wind, ice, fire, fireworks, meow, purr, tick, gears, page flips, whispers, glass, rumble…).
  4. The bundled HyperFrames library: `osfx.lib(name)` (whoosh, whoosh-cinematic, pop, sparkle, glitch-1/2/3,
     chime, riser, impact-bass-1/2, ping, notification…).
- Layer them: a real recording for the "what", a synth hit for the punch, always with a fallback.
  `osfx.project(ROOT)` freezes every sound used into `assets/sfx/` so the project re-synthesises identically;
  CC BY credits land in `assets/sfx/CREDITS.md` and go into the post caption.
- Cinematic and easy to hear: impacts, braams, taiko drum rolls, risers, sub drops, conch, gong, bells,
  roars, whooshes, story-specific foley. Calm/awe topics (e.g. the Big Bang) use **soft ambient** sound.
  No sounds on captions. Target ~ −12 to −17 dB mean, −1 dB peak; verify with ffmpeg volumedetect
  (you cannot listen).

## Build recipe

```bash
videos/_engine/new_video.sh <slug>          # template + fresh engine/kits; prints the next steps
cd videos/<slug>
# 1. scripts/lines.json + scripts/voices.json (cast with ../_engine/VOICES.md), then:
SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3 scripts/make_voices.py .
# 2. scripts/synth_audio.py: CAPS, GAPS, TAIL, sound cues (osfx), then:
python3 scripts/synth_audio.py              # prints DUR; set data-duration in index.html to it
# 3. index.html: palette C → characters (drawn inside character(...)) → scene functions →
#    PX.setup(C, {scenes, sceneAt, cuts, post, captions, ui?}) → GSAP proxy (see the template + ../style-sample)
npx hyperframes snapshot --at <12 key moments> --no-end --describe false   # look at the contact sheet, fix, repeat
npx hyperframes check
npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4
ffprobe … ; ffmpeg -i renders/video.mp4 -af volumedetect -f null -   # verify duration + levels
```

Engine notes (`videos/_engine/pixel-engine.js` v2): everything is a pure function of `t` (no Math.random,
use `rng(seed)` / `hash1`). Helpers: `character camAt shake setCam screen disc ell line rect rrect poly vgrad
vignette worldText glow lighter normalBlend glitchRows tintImg mix`. `glow()` and `hex()` need **hex**
colours — passing an `rgb()` string from `mix()` throws and freezes frames. Always reset
`normalBlend()` after `lighter()`. Old projects keep their own engine copy (the chunky v1); new projects get
v2 from `new_video.sh`. Write a short `BRIEF.md` (message, story, voices, sound, sources) per project.

## Instagram caption format

```
<Title> 🎧

<Hook question>? <One-line answer.>

<Short paragraph walking through what the video shows, with real numbers.>

Sources: <Source 1>; <Source 2>; <Source 3>

#<topic> #<topic> #<science|mythology|fable> #pixelart
```

Add any CC BY sound credits from `assets/sfx/CREDITS.md` before the hashtags; label fiction as fiction.

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

## Render audio check

The renderer sometimes lowers the audio (seen: −6 dB). After rendering, compare `ffmpeg -i renders/video.mp4 -af volumedetect`
with `assets/audio/mix.wav`; if it's quieter, re-mux the mix: `ffmpeg -i renders/video.mp4 -i assets/audio/mix.wav -map 0:v
-map 1:a -c:v copy -af volume=-1.2dB -c:a aac -b:a 192k -shortest out.mp4`.
