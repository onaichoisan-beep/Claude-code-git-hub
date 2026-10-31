---
message: "Popcorn pops because water inside the kernel turns to steam; at ~180 C and ~9 atm the hull bursts, the starch foams up to ~40x bigger, a starch 'leg' makes it jump, and the pop sound is the steam escaping."
destination: reels / shorts
aspect: 1080x1920
length: 32s
---

## Intent

The owner's script #1, built with the engagement rules learned from the @science_in_8bit / @pixel_art_explains references
(STYLE_GUIDE.md section 6): the kernel is the character, a live counter at the top the whole time, text cards every ~2 s,
no narration, the @SCROLL2STUDY.IN handle on every frame, and sound that follows the story.

## Story

| Time | Text | Picture | Counter |
|---|---|---|---|
| 0–1.6 | THIS KERNEL IS ABOUT TO EXPLODE | scared kernel in a hot pan, "UH OH." | TEMP 150→175°C |
| 1.6–2 | (rewind glitch) | | numbers scramble |
| 2–5 | IT'S HIDING WATER INSIDE | calm kitchen, zoom into the kernel | TEMP 20→75°C |
| 5–9.5 | AT 100°C… / …BUT THE SHELL WON'T LET IT OUT | cutaway: water drops jiggle, become steam puffs bouncing off the shell | TEMP →125°C |
| 9.5–13.75 | PRESSURE: 9 TIMES… / AT 180°C… LIMIT | straining kernel, cracks glow, "HELP." | + PRESSURE 1→9 ATM |
| 13.75–14 | — | everything darkens, the beat stops | |
| 14–15.2 | POP! | white flash, hull shards, steam | POP! |
| 15.2–19 | STARCH TURNS INTO FOAM / UP TO 40X BIGGER | the popcorn puffs up | VOLUME X1→X40 |
| 19–23.5 | IN SLOW MOTION IT GROWS A LEG… / …AND JUMPS! | a starch leg pushes off the pan, it flips up | SLOW MOTION · REC |
| 23.5–25.7 | THE POP SOUND? THAT'S THE STEAM ESCAPING | steam jet + sound rings, "PSSHHH!" | POP = STEAM |
| 25.7–27.6 | DUDS? A CRACKED SHELL LET THE STEAM LEAK | a sad cracked kernel by the popcorn box, "..." | POPPED 99 : DUDS 1 |
| 27.6–30.5 | SEND THIS TO YOUR MOVIE BUDDY | popcorn rains into the box faster and faster | POPPED 99→599 |
| 30.5–32 | (tape stop, rewind) → THIS KERNEL IS ABOUT TO EXPLODE | the picture slows and darkens, glitch back to the hook | TEMP again |

## Sound (scripts/synth_audio.py + chiptune.py)

- Signature: oil crackle whose rate follows TEMP (2 clicks/s at 20°C → 70/s at 180°C, blurring into a sizzle); the steam
  bounces and the final popping frenzy (4 → 40 pops/s) use the same idea.
- Nonstop 8-bit bed, tempo following the tension: 140 (hook) → 100→120 (heating) → 120→165 (pressure) → silence 0.25 s →
  128 with lead melody → 64 half-time octave-down (slow motion) → 150 (frenzy) → tape-stop → rewind → 140 (hook).
- Pressure whine glides with the PRESSURE counter; a blip on every card; a tick every 0.5 s on the counter; whoosh + hit on
  every cut; slow crescendo. OpenGameArt CC0 hits/bangs/springs/bubbles + the HyperFrames library + synth kits.

## Facts

Virot & Ponomarenko (2015), J. R. Soc. Interface 12: 20141247, "Popcorn: critical temperature, jump and sound": kernels pop at
~180°C; a starch "leg" makes the flake jump; the pop sound comes from the release of water vapour. Internal pressure at
popping ~135 psi (~9 atm) (Hoseney et al. 1983, J. Cereal Science). Expansion up to ~40x is the commonly cited figure for good
popcorn; unpopped kernels usually have damaged hulls that leak the steam.
