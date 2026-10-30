# Motion-Design Promo Style ("Sound is half the video")

Learned from one reference reel (720×1280, 30 fps, 32.7 s, HEVC): a promo for
"Claude Code sounds" by @damianodesu. It shows three mini-demos (product
launch, music video, animation), then a timeline that reveals that Claude
placed every sound, and ends on a "Comment SOUND" CTA.

## Measured specs
| Spec | Value |
|------|-------|
| Format | 9:16, 720×1280, 30 fps, ~33 s |
| Loudness | **-13.7 LUFS integrated**, LRA 3.9 LU (dense and compressed), peaks at 0 dBFS |
| Silence | Only one gap, a 0.6 s drop to silence at 30.2 s just before the end card ("breath before the CTA") |
| Hard cuts | **None.** Scene detection finds zero cuts even at a 0.12 threshold. Every change is a morph, glitch, push or wipe. |
| Audio transients | ~37 detected hits in 33 s (≈1.1/s), clustered in bursts on each reveal |

## Structure (four acts plus a CTA)
```
0.0–2.0   HOOK      Two-line sticker title "Free sounds / at the end 🔊" + black
                    caption bar "Claude code sounds 🤮". The promise is a reward for watching to the end.
2.0–8.5   DEMO 1    "01 Product launch": fintech dashboard ("Kite", $0 → $48,210)
                    played once SILENT, then glitch-rewind ◀◀ "Let's try with this
                    sound package." and replayed WITH sound.
8.5–13    DEMO 2    "02 Music video": lime vinyl with a magenta label "NOVA",
                    tonearm drops, "TURN IT UP / LOUDER!" kinetic type.
13–17     DEMO 3    "03 Animation": flat paper-cut landscape, smiling sun, paper
                    plane, bird. "Now listen. An animation."
17–22     REVEAL    "This video" NLE timeline: PICTURE track (Launch / Music
                    video / Animation clips), SOUND tracks fill with waveform
                    chips, then "PLACED BY Claude · 84 → 258 sounds", "FRAME BY
                    FRAME … ✓ On the frame". VO: "Every sound placed on the exact
                    frame by Claude."
22–32.7   THESIS    Split screen: lime top "Motion is half the video." / black
                    bottom "Sound is the other half." + lime waveform, pill CTA
                    "💬 Comment SOUND", Instagram logo + @handle end card.
```
The core trick is **show it silent, rewind, show it with sound**. The before/after
is the argument, and the final line states the thesis in a symmetrical couplet.

## Visual language
- **Palette:** acid lime `#D9FF1F`-ish as the single hero colour; ink black
  `#0E0E10`; hot magenta `#E8338F` (music section only); off-white UI cards
  `#F7F7F5`; pastel mesh-gradient backgrounds (lime / lavender / peach blobs,
  soft and blurred). Each demo owns a world: pastel glass UI, then black/magenta
  vinyl, then beige paper-cut, then lime/black split.
- **Type:**
  - Ultra-condensed heavy grotesque for display (`TURN IT UP / LOUDER!`,
    `Motion is half the video.`). Anton or Bebas for caps, and *Inter Display Black*
    with tight negative tracking (-4 to -6%) for the sentence-case lines.
  - Clean geometric sans (Inter/SF) for UI and captions; monospace caps for UI
    micro-labels (`REVENUE · THIS WEEK`, `LIVE · SUN`, `00:16:21`, `PICTURE`, `SOUND`).
  - Sticker title: black text on a lime highlighter box, slightly rotated, with an emoji.
- **Captions:** white rounded pill, black semibold text, 1–3 words, lower
  third (~70% height), swapped on every phrase. They act as karaoke-style word groups, not full subtitles.
- **Section chip:** top-left white pill `01 Product launch ━━━` with a black
  number badge and a progress dash, persistent per section. It plays the same role as
  the chapter label in the Field Notebook style.
- **Persistent watermark:** Instagram glyph + `@DAMIANODESU` small, left-middle.
- **UI-as-hero:** fake product dashboards (glassmorphism cards, soft shadow,
  big tabular numbers, mini bar chart with one lime bar, sparkline, "Launch"
  lime button, "Best day $9,840" tooltip, "Live in 32 countries").
- **Flat illustration** for the animation demo: layered paper-cut hills,
  houses, a sun with a face. These elements bounce in on stagger.

## Motion and editing
- **Never cut, always transform.** Transitions used:
  - **Glitch / RGB-split / scanline tear + rewind icon ◀◀**, used as a "do it again" device.
  - **Push-through / scale-through** into the next world (the vinyl grows to fill the frame).
  - **Hard colour-flash wipe** (a full lime frame between the launch and music sections).
  - **Card fall-away**: the scene collapses into a black slab or sheet that falls back
    and reveals the next scene.
  - **Dim-down/blur** of the whole frame for the end card.
- **Number count-ups** with motion blur on the digits ($0 → $44,725 → $48,210).
- **Bars grow** with overshoot; the key bar is always the lime one.
- **Kinetic type:** words slam in with heavy scale overshoot plus motion blur,
  and colour-cycle per beat (black → white → lime `!`). Background colour
  flips on the beat (magenta ↔ black ↔ lime stripes).
- **Vinyl** spins continuously; tick-mark ring around it pulses like an audio meter.
- **Waveform chips** pop into timeline lanes one by one in time with the sounds
  they represent. The **playhead** sweeps across. A counter ticks up (84 → 258).
- **Bouncing shapes:** five black rounded squares above the thesis line bob
  and rotate like a loading or bouncing-ball rhythm and react to the audio.
- Every element enters with **overshoot easing** (back.out / elastic) and
  leaves with a fast ease-in. Nothing stays fully still.

## Sound design (the subject is the sound, so it is dense)
- Short, crisp UI foley on every motion: pops, clicks, ticks on number
  rolls, swooshes on every move, a "cha-ching"/success chime on the launch, and a
  record scratch/needle drop on the vinyl.
- A punchy music bed that kicks in hard on "TURN IT UP LOUDER!"
- Glitch stutter and tape-rewind sound on the ◀◀ device.
- The VO is fast, casual and slightly ironic (in English): "Claude code sounds… great
  motion, the sound… let's try with this sound package. A product launch. A
  music video. Now listen. An animation. This video. Every sound placed on
  the exact frame by Claude. Motion is half the video. Sound is the other half."
- Mastered loud (~-14 LUFS, peaks to 0 dBFS), with a deliberate 0.6 s silence before the
  final card so the CTA lands.

## Recipe to reproduce
1. Pick a thesis couplet: "X is half the Y. Z is the other half."
2. Hook with a reward sticker ("Free ___ at the end") and a self-deprecating caption.
3. Build 3 contrasting 3–5 s mini-worlds (UI, music, illustration), each with
   its own palette but sharing one hero colour and a numbered section chip.
4. Play the first one without the key ingredient, glitch-rewind it, and replay it with the ingredient.
5. Reveal the process (the timeline or editor view) with a counter of the work done.
6. Split-screen thesis plus a "Comment KEYWORD" pill CTA, then the handle end card.
7. No hard cuts: chain glitches, push-throughs, colour flashes and card falls.
8. Place an SFX on every visible motion. Master to -14 LUFS with one breath of silence before the CTA.

## HyperFrames notes
- Section chip, captions and watermark go on persistent top tracks. Each mini-world is
  its own sub-composition.
- The glitch-rewind uses a registry glitch / chromatic-aberration block and a reversed
  GSAP timeline segment.
- Count-ups and bars: GSAP `snap` on a number tween; bars use `scaleY` with `back.out(1.7)`.
- Use `hyperframes beats` to snap the kinetic-type slams and colour flips to the music.
