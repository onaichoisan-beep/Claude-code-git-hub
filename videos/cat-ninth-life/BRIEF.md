---
message: "A cat on its 9th life tells you how it lost the other eight, and how careful it is now."
destination: reels / shorts
aspect: 1080x1920
length: 45.3s
---

## Intent

The second of four narrated fable shorts. It is a comedy montage narrated by the cat, so the voice is the
character. An upper-left LIVES box counts down 9 → 1 with paw icons. Each death is cartoonish (a white
flash, a "poof", and a translucent ghost cat with a halo floating up), never gory.

## Story (line → picture)

| Time | Beat |
|---|---|
| 0–3.7 | Cold open: Mittens (ginger tabby, white mittens) on a red sofa at night, eight ghost cats with halos above him. LIVES 1/9. "I'm on my ninth life. Want to know what happened to the other eight?" Rewind glitch |
| 3.7–8.2 | 1. Egypt: on a golden pedestal, worshippers bowing. "The crocodile didn't": a croc rises from the Nile and SNAPS |
| 8.2–12.5 | 2. Viking longship in a storm with lightning and rain. A fish jumps; he leaps after it. Overboard, splash |
| 12.5–16.3 | 3. China: asleep on crates under a FIREWORKS sign. The fuse sparks, KABOOM, and he flies up puffed out |
| 16.3–20.1 | 4. Pirates: feathers in his mouth; the captain sees, "!", and kicks him off the plank |
| 20.1–25.1 | 5. Paris: proud on top of the Eiffel Tower. The camera pulls back to the city lights far below. He looks down, gulps, and falls |
| 25.1–29.4 | 6. Peeking out of a rocket's porthole at liftoff. Then floating in space in a fishbowl helmet, with a crossed-out fish thought bubble. "Space has no fish" |
| 29.4–33.3 | 7. A scientist (wild white hair) shuts him in a box under a chalkboard reading ALIVE+DEAD = ?. The box rattles, "?" pops up, and a ghost floats out |
| 33.3–36.7 | 8. Kitchen: eating. A cucumber silently slides in behind him; he leaps straight up, fur puffed |
| 36.7–39.7 | Now: hard hat and bubble wrap on a pile of cushions, LIVES 1/9 blinking red. "I'm being very, very careful" |
| 39.7–45.3 | The owner (off screen, second voice): "Mittens! Get off the counter!" He looks at us: "Very careful." Nudge, nudge, push. The glass falls, SMASH, and it loops back to the opening |

## Voice

`edge-tts` (`scripts/make_voices.py`, `scripts/lines.json`): Mittens is **en-GB-RyanNeural** (+12%,
−2 Hz: dry, smug British), the owner is **en-US-EmmaNeural**. `scripts/synth_audio.py` writes `captions.js`
with the word timings, mouth flaps and the shared death times (`window.DEATHS`, `T_BOOM`, `T_KICK`,
`T_PUSH`, `T_SMASH`) that the scenes key off.

## Sound

Synthesised (`sfxlib.py` + `foley.py`: crocodile snap, storm sea, creaks, fireworks, parrot squawk, fall
whistle, rocket rumble, lab blips, box rattle, hiss, glass smash, purr, kitchen clock), the bundled
HyperFrames library (pop, sparkle and whoosh on every death and scene change, a bass impact for the
fireworks), and real recordings in `assets/sfx/` (cat meow and big splash, CC0; thunder and gulp,
CC BY 4.0, credited in `assets/sfx/CREDITS.md`).

## Facts

- Fiction. The jokes nod to real things: cats were revered in ancient Egypt, "Schrödinger's cat" is a
  physics thought experiment (a cat in a box both alive and dead until observed), and cats famously jump at
  cucumbers placed behind them.
