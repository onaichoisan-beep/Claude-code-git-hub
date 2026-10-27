---
message: "A secret film crew builds your dreams every night — and that falling jolt? Someone dropped you."
destination: reels / shorts
aspect: 1080x1920
length: 20.0s
narration: yes — en-US-AndrewMultilingualNeural (narrator, +10%), en-US-GuyNeural (the director's "ACTION!")
---

## Script (scripts/lines.json)

1. You've never seen this... because you're always asleep for it.  (crew caught sneaking props past the bed — "SHH!")
2. The second your eyes close, a secret crew sneaks in.  (eyes close, lamp off, door creaks, crew tiptoes in)
3. Lights. Fog. A dragon on strings.  (spotlights clunk on, fog rolls, a cardboard dragon hoisted, sunset backdrop)
4. ACTION!  (the director + clapperboard)
5. Tonight's dream? You can fly.  (flying over a cardboard city... pull back: he's on a pole, a crew member with a fan)
6. But the moment your alarm rings...  (a giant alarm clock rips through the painted sky, crew panics)
7. they tear the whole set down.  (backdrop drops, dragon crashes, crew sprints)
8. And that falling feeling that jolts you awake?  (the pole crew shrug... and let go)
9. Someone dropped you.  (he jolts upright; a crew member peeks from behind the bed: "shh") → loop

Fact note: the real "falling" jolt is a hypnic jerk, which happens as you drift off — the line says it
"jolts you awake", which is true either way; the crew is fiction.

## Voice / audio

`python3 scripts/make_voices.py .` (edge-tts, voices in scripts/voices.json) → `python3 scripts/synth_audio.py`
writes assets/audio/mix.wav (SFX ducked under the voice) and captions.js (word-synced). Foley: Openverse
alarm clock + clapperboard (CC0), procedural pizzicato tiptoes, snores, creaks, siren, slide whistle.
