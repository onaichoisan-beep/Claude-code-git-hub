# AUDIO: reference
- Mix loudness (whole reel incl. Before/After overlay): **-14.2 LUFS integrated**, LRA 3.7 LU.
- Music bed: none detected (energy < 120 Hz is 0.4 % of the speech band, median).
- SFX: 44 high-frequency transients found; without Demucs (not installed) they cannot be told apart from sibilants, so **SFX hits are UNVERIFIED**. Sound design is phase 6; it is out of scope for this template builder, which uses only the client's voice (like the skill's templates).
- Word timing (whisper large-v3, first 12 s): text lags the word by +4 f average (see STYLE.md).

## Reference SFX map (v2, Demucs htdemucs two-stem, non-vocal stem -27.6 LUFS vs voice -14.2)
| ref frame | on what | sound | level vs median voice frame |
|---|---|---|---|
| 325 (47 f) | TypeBox typing | keyboard typing, centroid 1.6 kHz | -6.4 dB |
| 779 (14 f) | big serif word "working" | low thump (52 % energy < 300 Hz) | -1.2 dB |
| 937, 1251 | side notes Save/Invest | short bright ding/click, 5-7 kHz | -7.6 .. -18 dB |
| 1148 (27 f) | ArcText | shimmer, 6.2 kHz | -16.6 dB |
| 1418 (14 f) | YellowItalic | mid hit, 2.5 kHz | -2.2 dB |
| 1717 (6 f) | LimeWord "Ice-creams" | sparkle, 8 kHz | +0.4 dB |
| 1814 (23 f) | ScriptFade "Cafe Mocha" | twinkle, 7.5 kHz | -7.5 dB |
| 381 (9 f) | collage photo drop | loud slap | +14.6 dB |
No sound on the cream type card (S02), polaroid, video card or camera cut. v2 synthesises these sound types (audio_build.py) at these levels.
