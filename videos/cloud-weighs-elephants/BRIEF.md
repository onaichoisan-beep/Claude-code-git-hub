---
message: "A 1 km cumulus weighs about 83 elephants; a thundercloud about 330,000. Tiny droplets stay up until they grow into rain."
destination: reels / shorts
aspect: 1080x1920
length: 61.5s
---

## Intent

Remake of an owner-supplied reference reel (a presenter explaining how heavy clouds are) in the owner's
pixel style, keeping her script but with a new female voice. This one is narrated, because the owner
asked for a voice. Small centred captions are synced word by word to the narration, and SFX are ducked under the voice.

Script: the reference's, line for line. Two changes: the reference's ending was a teaser for another
of her videos ("what about tornadoes… follow along"), so the droplet line now finishes the story
("…grow a million times bigger… they fall as rain"), and a closing line loops back to the opening hook.

## Voice

Microsoft neural voices via `edge-tts` (`scripts/make_voices.py`, 15 female English voices).
Shipped voice: **en-US-AvaMultilingualNeural** (rate +6%). Samples of all 15 are in `renders/voices/`.
To swap the voice, run `make_voices.py <dir> <voice>`, copy that voice's `NN.wav`/`NN.json` into
`assets/audio/vo/`, run `python3 scripts/synth_audio.py`, then render again. Lines snap to fixed slots,
so the picture stays in sync, and the captions follow the new voice's word timings.

## Facts

- A typical 1 km³ cumulus holds ~0.5 g/m³ of water, about 500 t, or 83 elephants at ~6 t each (USGS Water Science School; Peggy LeMone, NCAR)
- A large thunderstorm can hold ~2 million t of water. That is ~330,000 elephants, or ~800 Olympic pools at 2,500 t each (NCAR / UCAR estimates)
- Cloud droplets are ~10–20 µm across; a human hair is ~70 µm; a raindrop (~2 mm) has about a million times the volume of a cloud droplet (NOAA / UCAR Center for Science Education)
- Cirrus: thin ice clouds 6–12 km up with far less water per volume. The "≈5 elephants" for the same size is the reference's figure and an order-of-magnitude estimate
