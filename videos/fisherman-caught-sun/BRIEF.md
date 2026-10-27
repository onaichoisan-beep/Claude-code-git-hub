---
message: "An original fable: the night a fisherman caught the Sun, and why every diya holds a crumb of it."
destination: reels / shorts
aspect: 1080x1920
length: 40.3s
---

## Intent

The first of four narrated fable shorts the owner asked for: invented "origin legends" in the pixel
house style, each with its own narrator voice. This story is fiction (it is not a real myth), so the
caption says so. The diya tradition at the end is real.

## Story (line → picture)

| Time | Beat |
|---|---|
| 0–3.4 | Cold open: a net bursts out of the night sea with the blazing Sun in it ("One evening... a fisherman caught the Sun."). Rewind glitch |
| 3.6–7.5 | Sunset: the Sun, with a sleepy face, sinks into the sea to sleep. Gulls, Zzz |
| 7.5–11.7 | Old Raghu casts his net. A glow builds under the water. "...burning": white flash as it comes up with the Sun |
| 11.7–14.2 | He drags the Sun into his hut. Light leaks through the thatch, and he peeks out of the window |
| 14.2–16.7 | "And morning... never came": a rooster crows at a black horizon. The SUNRISE? clock runs 5:30 → 12:00 PM |
| 16.7–22.6 | The sea freezes, the birds go silent under frost, and the villagers shiver round a dead fire in the snow |
| 22.6–24.9 | His wife (second voice): "Raghu! Give it back!" |
| 24.9–29.2 | He rows out into the black sea and hurls the Sun up. Dawn floods the sky |
| 29.2–33.5 | Rewind glitch: "But first..." his fingers pinch one tiny glowing crumb off the Sun, and the Sun winks |
| 33.5–40.3 | Diwali night: rows of diyas light on the ghat steps, fireworks over the sea. The camera dives into one flame, which has a tiny winking Sun in it ("is a crumb of the Sun"). Flash, back to the opening |

## Voice

Microsoft neural voices via `edge-tts` (`scripts/make_voices.py`, lines in `scripts/lines.json`):
narrator **en-IN-PrabhatNeural** (−3%, −3 Hz: an older Indian storyteller), Raghu's wife
**en-IN-NeerjaExpressiveNeural**. `scripts/synth_audio.py` lays the lines out (`voicelib.py`),
writes `captions.js` (captions + word timings the scenes key off), and builds the SFX with
`sfxlib.py` + `foley.py`, all synthesised (sea, splashes, sizzle, rolling boil, rope creaks, gulls,
crickets, wind, ice cracks, teeth chatter, oars, dawn birds, a tanpura-like drone, Diwali
fireworks and bells), ducked under the voice.

## Facts

- Fiction: an original fable, labelled as such in the caption.
- Diyas are small clay oil lamps lit in rows for Diwali, the festival of lights.
