# Pixel Science Explainer — Style Guide

Reverse-engineered from three reference shorts (Blue Morpho, Neuron/Brain, Animal Heart Rates; signed "@BITWONDER").
Goal: retro pixel art that still reads instantly on a phone.

---

## 1. Format & technical specs

| Property | Value |
|---|---|
| Aspect | 9:16 vertical (Shorts/Reels/TikTok) |
| Output | 720×1280 @ 30fps |
| **Native art canvas** | **180×320**, upscaled **4× nearest-neighbour** (measured: 4px pixel grid everywhere) |
| Length | 30–60 s |
| Audio | Music + SFX only, **no voiceover**. A 🎧 headphone icon under the title means "sound on" |
| Cuts | **Almost no hard cuts**. Scene-change detection found 0–1 cuts per video. Every transition is a camera move (zoom/pan/dolly) |

**Hybrid trick:** The world is drawn at pixel resolution, but the *camera* moves smoothly (sub-pixel zoom, parallax, rotation in 3D-ish shots). Bokeh and glow are drawn as soft layers and then posterized and dithered. So the result looks like a modern cinematic render pushed through a pixel filter: "pixel style, but HD clarity."

---

## 2. Why it stays clear (the core rules)

1. **One subject, centred, large.** The hero object (butterfly, neuron, elephant stack) fills 40–60% of frame width. Nothing competes with it.
2. **Value separation.** The background is dark and low-contrast (often 3–5 close tones of one hue). The subject is brighter, more saturated, and has a **dark 1px outline**.
3. **Background is blurred, not detailed.** Big posterized bokeh circles, light shafts and soft gradient bands give depth without adding information. It works like a depth-of-field blur, rendered in pixels.
4. **One accent colour per video** that marks "the important thing":
   - Morpho: electric blue `#1f5fe0`-ish against greens
   - Neuron: hot orange/gold `#ff9a2e` sparks against purples
   - Heart rates: red hearts `#d83a4a` against navy
5. **Limited palette per scene** (~12–20 colours), mostly one hue family + the accent + near-white text.
6. **Dithering only in gradients**: checkerboard/ordered dither in sky bands, glow falloff and bokeh edges. Flat areas on the subject stay clean.
7. **Specular highlight pixels.** White dots on dew drops, the bulb glass, sphere tops and wing edges. A few bright pixels sell "3D".

---

## 3. Palettes (sampled from frames)

**Jungle / Blue Morpho**
`#09140f #0d2514 #1b3320 #284624 #306a29 #488632 #6da340 #9cc155` (greens, dark to light)
`#62753a #8e8e43 #c1a44e #f1d58a` (sun/bokeh golds) · `#945920 #291e18` (bark) · accent blue `#1f5fe0 / #4f8ff0` + purple iridescence `#7a3fe0`

**Neuron / Brain**
`#040109 #0c0515 #160a22 #200f2f #2b143c #37224e` (purple-black base)
`#5a3aa0 #8a5ae0 #b48af0` (cell bodies) · `#5b577c #c8c4d8` (myelin grey-lavender) · accent `#ff9a2e #ffd27a` (signal/glow)

**Night Ocean / Heart Rates**
`#000310 #04091d #081a42 #0d2957 #143b70 #215188` (navy sea/sky)
`#463f4f #5e5767` (elephant greys) · `#f2e8c8` moon · accent red `#d83a4a`, warm `#cc946b`

Text is always near-white `#edecef / #f4f1f6` on near-black `#06050a`, with the accent (gold `#ffd23f`) for key numbers.

---

## 4. Typography (the "caption card")

- **Font:** an all-caps monospace-ish pixel font with square letterforms (similar to *Press Start*-lite / *Silkscreen* / *VT323* / *m5x7*). Strokes are 1 art-pixel wide.
- **Box:** solid black (`#06050a`, ~90% opacity) rectangle tight around the text with about 1 art-pixel padding. No border, no rounded corners.
- **Two sizes:** HEADLINE (about 3× art-pixel scale, 2–3 lines, ≤12 chars/line) and small subcaption (about 2×, for supporting lines like "IT SHEDS ITS SKIN" above a big "4 TIMES").
- **Hierarchy inside one card:** small lead-in + BIG payoff ("THERE IS / **NO BLUE PIGMENT**", "ONE OF / **86 BILLION** / NEURONS").
- **Number highlight:** the key number is in the accent colour (gold `100+ M/S`, `~20 WATTS`, `86 BILLION`).
- **Position:** upper third, centred horizontally (about y = 4–10% from top), clear of the subject. On the heart-rate video, labels sit *next to* each object instead ("30 BPM ♥"), and the newest label is big then shrinks to small when the next one arrives.
- **Copy style:** 2–6 words. Hook as a question ("HOW DOES IT TURN BLUE?", "ONE NEURON FIRES — HOW FAR?"), then facts, then a twist ending ("THIS VIDEO WAS ONE HEARTBEAT").
- **Signature:** "@BITWONDER" is hidden *inside the scene* (carved on a branch, written on the bulb glass, a tag on the animal stack) rather than shown as a watermark.

### Text animation
- **In:** pops on in 1 frame (no slide), or types/dissolves in.
- **Out:** **dissolves into a dot-matrix/dither pattern**. The letters turn into a sparse checkerboard of dots, fade to dim, and vanish (about 0.3–0.5 s). This is the signature exit.
- On screen for about 2–3 s per card; roughly one card every 3–5 s.

---

## 5. Camera & motion language

- **Continuous "one-take" journey.** Each fact is reached by moving the camera, not by cutting:
  - *Macro zoom-in*: butterfly → wing → scales (blue/purple tiles) → cross-section of ridges ("tiny ridges reflect blue light").
  - *Dive along the subject*: travel down the axon → into the membrane ("sodium rushes in") → along myelin.
  - *Pull-back reveal*: single neuron → network → whole brain → brain inside a light bulb.
  - *Vertical pan/stack*: camera rises as animals stack on the elephant, then pans down into the ocean to the whale.
- **Loop structure:** the final frame matches the first (Morpho ends on the same title + leaf shot; Heart Rates starts and ends on the whale's heart; Neuron returns to the firing neuron). This helps replays.
- **Ambient life in every frame:** drifting particles/dust, slow bokeh drift, light shafts, twinkling stars, dew sparkles, a pulsing glow, waves. Nothing is ever fully still.
- **Easing:** slow ease-in-out camera moves (1.5–3 s); subject actions are snappy (sprite frames at about 8–12 fps "on twos/threes" while the camera runs at 30).
- **Time skips** use a caption ("2 WEEKS LATER") instead of a cut.
- **Diagram moments:** when explaining physics, switch to a simplified side-view diagram (ridges like pixel pine trees, light rays drawn as coloured diagonal lines bouncing) while keeping the same pixel language and palette.

---

## 6. Lighting & atmosphere recipe

1. Base: vertical gradient in 4–6 posterized bands of the scene hue.
2. Big light source (sun/moon/glow) with **concentric posterized halo rings** (clearly banded, dithered at the edges).
3. Diagonal **light shafts** at about 30°, slightly lighter, low opacity.
4. Out-of-focus **bokeh circles** (several sizes, flat-filled, 1–2 tones lighter).
5. Foreground silhouette layer (dark leaves, rocks, waves) for framing and depth.
6. Midground subject: crisp, outlined, with 3–4 tone shading and specular pixels.
7. Particles: 1-px dots (dust, stars, sparks) drifting.
8. Bloom on accent elements (the orange signal, glowing brain): a soft additive glow, then quantized.

---

## 7. Narrative template (30–60 s)

| Beat | Time | Content |
|---|---|---|
| Hook | 0–3 s | Hero shot + question card + 🎧 |
| Setup | 3–10 s | Show the start state (egg, neuron at rest, slow whale heart) |
| Escalate | 10–40 s | 4–8 fact cards, each paired with a camera move into or out of detail; numbers escalate (30→60→120→240→600→1,200 BPM) |
| Reveal | 40–50 s | Counter-intuitive fact ("NO BLUE PIGMENT", "~20 WATTS") |
| Loop | last 3 s | Return to the opening frame/composition; optional twist line |

---

## 8. Production checklist for recreating it

- [ ] Draw/compose at 180×320; export with `image-rendering: pixelated` / nearest-neighbour ×4
- [ ] Snap sprite positions to the art-pixel grid; let only the camera be sub-pixel
- [ ] Post pass: posterize to a scene palette + ordered (Bayer 4×4) dither on gradients
- [ ] Dark low-contrast background, bright outlined subject, one accent colour
- [ ] Captions: black box, pixel font, ≤6 words, accent-coloured number, dither-dissolve exit
- [ ] No hard cuts; zoom, pan and pull-back between facts
- [ ] Constant ambient motion (particles, bokeh, shafts)
- [ ] Music + SFX only; end frame loops to the start
- [ ] Hide a creator tag inside the scene art
