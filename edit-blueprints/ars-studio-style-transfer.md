# ARS Studio — "Hey, main ARS Studio se hoon" · Style-Transfer Edit Blueprint

Reference: V1 Forge "My name is Vikas" (10.2 s, red kinetic-type intro).
Client: ARS Studio talking-head clip (10.03 s source → 10.62 s finished edit, 9:16, 24 fps).

---

## 00 — What I measured in the client clip (read this first)

| Fact | Value | Why it matters |
| --- | --- | --- |
| File | 720×1280, 24 fps, 10.03 s, one continuous take, no cuts | Every "cut" must be made with scale + graphics, exactly the problem the reference solves |
| Set | Warm off-white seamless (#F1E3DD wall, #E9E0D8 floor), cognac armchair (#5A3B2F), speaker in **black tee** (#22252C), glasses, white sneakers | **Almost the same set as the reference.** That is the biggest risk in this job: copy the reference's red kit onto this set and the edit becomes a reskin of V1 Forge. Surface style has to move further than usual (§03). |
| Framing | Speaker is small: chair = 38% of frame width (reference: 48%), head top at 44% height, feet at 81% | Native framing is too wide; the base ("wide") state needs a 1.25× scale just to match the reference's wide shot |
| Watermark | AI-generator sparkle, bottom-right (≈ x 600, y 1160 at 720p) | Every scale state in this plan is ≥ 1.25×, which pushes it off-frame. **Never show the clip at 1.00×.** |
| Resolution | 720p source; the plan goes up to 1.65× | That's a 2.5× upscale to 1080×1920. **Upscale the A-roll first** (Topaz Video / CapCut "Enhance quality" / re-export from the generator at 1080p). If stuck on 720p, cap TIGHT at 1.50×. |
| Loudness | −19.5 LUFS integrated | Bring to −14 LUFS |
| Head silence | 0.00–0.67 s silent before "Hey" | **Trim the first 0.34 s** so the first word lands at 0.10 s, like the reference. All times below are output times after this trim. |
| Language | Hinglish | Every *keyword* he says is English (brands, high quality, engaging videos, premium, brand, content, let's connect). The Hindi parts are the connecting words. Typeset only the English keywords (§08). |

### Transcript (word-timed, output time = source − 0.34 s; frames @ 24 fps)

| Out time | Frame | Line |
| --- | --- | --- |
| 0.10 | f2 | **Hey,** |
| 0.60–1.63 | f14–39 | main **ARS** (0.74 / f18) **Studio** (1.18 / f28) se hoon. |
| 1.63–1.78 | f39–43 | *(breath gap)* |
| 1.88–4.58 | f45–110 | Hum **brands** (1.92 / f46) ke liye **high** (2.48 / f60) **quality** (2.74 / f66) aur (3.08 / f74) **engaging** (3.26 / f78) **videos** (3.62 / f87) **create** (3.94 / f95) karte hain. |
| 4.58–4.81 | f110–115 | *(breath gap)* |
| 4.92–6.13 | f118–147 | Jo **actually** (4.94 / f119) **premium** (5.34 / f128) **feel** (5.70 / f137) karein. |
| 6.13–6.62 | f147–159 | *(longest gap, 0.49 s — the pivot)* |
| 6.68–8.69 | f160–209 | Agar aap bhi **apne** (7.12 / f171) **brand** (7.30 / f175) ke liye aisa **content** (7.98 / f192) chaahte hain, |
| 8.69–8.89 | f209–213 | *(breath gap)* |
| 8.96–9.52 | f215–228 | toh **let's** (9.02 / f216) **connect.** (9.28 / f223) |
| 9.52–9.69 | f228–233 | end of footage |

> Check by ear: one transcription pass heard "aap bhi, aap bhi" (a stutter) around 6.8–7.2 s. If it's there, cut the repeat and hide the jump under the slot-card pop at f171 (§05, Beat 05).

---

## 01 — REFERENCE DNA (the 16 things that actually make it work)

1. **The speaker never leaves the frame.** 0% full-screen B-roll. Proof is brought to the speaker as floating inset media.
2. **Scale changes are the cuts.** One locked shot plays like a multi-cam edit via a wide/tight scale ladder; every scale change is hidden inside a transition.
3. **Register by scale:** tight for statements about self, wide when the frame must hold evidence.
4. **One idea = one hero word.** Only the word the viewer must remember is typeset; everything else is a small lead-in or not written at all.
5. **Two-tier type hierarchy:** small lead-in (≈1:4–1:6) + one giant keyword, centered in the top third.
6. **The hero word sits behind the speaker's head** (person matte). Proof sits in front of him. He is sandwiched inside his own brand: depth reads as premium.
7. **The top ~35% of the frame is a typographic stage** that is wiped and rebuilt for each new idea.
8. **One accent hue does all the signalling.** Footage is low-saturation; the accent is the only saturated thing, so "accent = look here now."
9. **Every new claim gets a layered reset** (light element + texture burst + scale change) of 8–14 frames, landing on a breath gap or on the first syllable of the next keyword. Continuing the same claim only adds an element; it doesn't reset.
10. **Fast in, soft settle:** 3–8 frame entrances with motion blur, expo-out, overshoot on objects only, never on the camera.
11. **No frame is ever dead:** something new every ~0.28 s; after landing, elements keep a little life.
12. **Front-loaded speed:** the first two beats are ≤ 1.2 s, and later beats lengthen as information density rises.
13. **Evidence is shown, not said:** client names arrive as recognisable images; "engaging videos" arrives as playing clips.
14. **Biggest sound = biggest word:** one low impact on the core category claim; whooshes into resets; ticks on each object landing.
15. **Clean digital canvas:** no grain, leaks or vignette. Texture lives only inside transitions.
16. **Strict safe zones:** 8% sides, 12% top, nothing important in the bottom 18%.

**Surface-only (reference-specific, not principles):** the red ramp, halftone dots, red pixel confetti, star wipe, comet arc, tilted scrapbook cards with wobble, sepia founder portrait, glow on the name, 3D floor text + perspective grid, mirror-tile first frame, mono red chips.

---

## 02 — CLIENT STORY ANALYSIS

**Who's speaking / to whom:** a video studio pitching to brand owners and marketers (D2C, cafés, founders) scrolling Reels. Hinglish signals an Indian, digitally native SMB audience.

**Message:** "We're ARS Studio → we make high-quality, engaging videos for brands → that feel premium → want that for your brand? → let's connect."

**Emotional arc:** friendly recognition → competence → aspiration (premium) → *it's about you now* → easy invitation.

**The structural difference from the reference:** the reference is a self-introduction that ends on a promise. This script **turns toward the viewer halfway through** ("Agar aap bhi apne brand ke liye…"). The edit has to make that turn visible: the second half needs a layout that has room for *the viewer's brand*.

| Beat | What's said | Why | Viewer should feel | Viewer should see | Best form |
| --- | --- | --- | --- | --- | --- |
| 01 Name | Hey, main ARS Studio se hoon | Identity + hook | "Who's this? Looks sharp." | The name, huge, framed like footage through a lens | Talking head TIGHT + kinetic type behind head |
| 02 For brands / quality | Hum brands ke liye high quality… | Credibility | "They've done real work" | Their actual brand work, playing | Talking head WIDE + inset proof cards |
| 03 Engaging videos | …aur engaging videos create karte hain | Core category claim (peak) | Energy, conviction | The category word being *made* in front of you | TIGHT punch + impact + hero type that gets "rendered" |
| 04 Premium | Jo actually premium feel karein | The standard / aspiration | Calm confidence | Restraint: elegant serif, slow move, almost nothing else | MID, slow linear push, single serif hero |
| 05 Your brand | Agar aap bhi apne brand ke liye aisa content… | Turn to viewer | "This could be mine" | An empty slot labelled YOUR BRAND that fills with "content like this" | WIDE reframed left + slot card |
| 06 CTA | toh let's connect | Action | Easy, warm | Two halves of a word meeting | TIGHT + kinetic hero |
| 07 Close | — | Brand stamp | Closure | Letterbox shutter closes to the logo | Graphic end card |

---

## 03 — STYLE TRANSFER MAP

| Reference element | Reference behavior | Decision | Client application |
| --- | --- | --- | --- |
| Speaker never leaves | 100% of frames show him | **Transfer** | Same. 100% of the edit's footage frames show him; proof arrives as cards. |
| Scale-as-cut ladder | 1.00 / 1.20 / 1.33 | **Transfer (re-measured)** | WIDE 1.25 / MID 1.45 / TIGHT 1.65 of client native (matches the reference's framing and kills the watermark) |
| Hidden scale changes | Every scale move sits inside a transition | **Transfer** | Same. Only one visible camera move: the opening push and the slow linear push in Beat 04. |
| Hero word behind head | Rotoscoped depth | **Transfer** | ARS, ENGAGING, BRAND, CONNECT sit behind his head. *premium* is the exception (in front, see Beat 04). |
| Lead-in + hero hierarchy | Small rose grotesk + giant red keyword | **Adapt** | Three voices instead of one family: heavy grotesk hero in ink, italic serif for accent words, mono for utility labels. The pairing is ARS's own identity, not V1 Forge's. |
| Red one-hue palette | Red ramp on off-white | **Adapt** | One hue kept, red dropped. **Ink + cobalt** on the warm canvas. Ink rhymes with his black tee, so type and speaker read as one system. Cobalt is the complement of the cognac chair, so it pops without clashing. On this near-identical set, a red kit would read as a copy. |
| Halftone burst | Texture in resets | **Inspire** | Replaced by video-studio primitives: **letterbox shutter bars** and a **9:16 frame iris** (the client's actual deliverable shape). |
| Pixel-block confetti | Constant, every frame | **Inspire + reduce** | **Keyframe diamonds (◆)**, the editing-timeline keyframe icon. Only on landings (~10 times), not constant. A studio's texture made from its own tool. |
| Light streaks / laser line | Red light carries the eye | **Adapt** | A **cobalt playhead line** that scrubs across type. It's literal studio grammar and has a job ("create"). |
| Star wipe / comet arc | Decorative wipes | **Ignore** | Too playful for "premium" and too recognisably the reference |
| Tilted scrapbook cards + wobble | ±3–8° tilt, spring, idle wobble | **Adapt** | Cards are **straight and aligned like a contact sheet / timeline row**, with ink hairline and cobalt crop-mark corners. Motion comes from the video playing inside them. Precision = "high quality." |
| Card pop with overshoot | 15% → 118% → 100% | **Adapt** | Softer spring: 70% → 104% → 100%, from +40 px below. Same snap, less bounce. |
| Glow on the name | Red bloom | **Inspire** | **Rack-focus entrance** on ARS (defocus → sharp). Lens language for a camera studio. |
| 3D swing-in italic heroes | Y-rotation, blur | **Ignore** | Swapped for letter cascades and a split-and-join. Fewer 3D gimmicks. |
| Letter cascade (IDEAS) | 1 f stagger | **Transfer** | Used on ENGAGING (fast) and *premium* (deliberately slow) |
| Floor-plane 3D text + grid | BRAND on perspective floor | **Ignore** | Doesn't serve any line here |
| Label chips | Red mono chips | **Adapt** | Cobalt chip with canvas-colored mono text: FOR BRANDS, YOUR BRAND, DM "CONNECT" |
| Self-thumbnail card (B4) | "This is what we make" | **Adapt (upgraded)** | The YOUR BRAND slot fills with a **live miniature of this video's own opening**, so "aisa content" (content like this) literally means *this*. |
| Mirror-tile first frame | Pattern interrupt | **Inspire** | First frame is a **viewfinder**: cobalt crop-mark corners framing him tightly, which snap open on "Hey". |
| Sepia founder portrait | Identity proof | **Ignore** | No line calls for it |
| Audio motif | Whoosh / impact / tick | **Transfer** | Same grammar, studio-flavored sounds: shutter clicks, tape-scrub, UI ticks, one sub impact. |
| Front-loaded pacing | 1.07 → 3.53 s beats | **Adapt** | Fast start, peak at ENGAGING, a **deliberate slowdown on PREMIUM**, the longest beat on YOU, then a snap CTA. |
| Ending | Excerpt, no ending | **Ignore** | Designed fresh: letterbox closes to a logo lockup that rhymes with the opening viewfinder. |

---

## 04 — CREATIVE DIRECTION: "THE EDIT BAY"

**The idea:** ARS Studio *makes* videos, so the visual world around the speaker is built from the tools of making them: the viewfinder, the letterbox, the playhead, the keyframe, the 9:16 frame, the empty media slot. The V1 Forge reference surrounds its founder with brand energy. ARS surrounds its founder with *craft*. Same editorial grammar (anchored speaker, behind-head keyword, scale-as-cut, proof-as-cards); a different creative world.

**Tone:** precise, calm-confident, premium. Less bounce than the reference and more alignment. An event every ~0.35–0.45 s instead of 0.28 s. Restraint is the proof of "premium."

**Signature moments (what people remember):**
1. The viewfinder snapping open on "Hey."
2. ENGAGING drawn as an outline and **rendered solid by a playhead** on "create."
3. *premium* in a slow italic serif with the frame finally breathing.
4. The empty **YOUR BRAND** slot filling with this very video.
5. CONNECT assembling from two halves that lock on a keyframe.

---

## 05 — BEAT-BY-BEAT EDIT PLAN

Coordinates are for a 1080×1920 canvas. "Scale" = scale of the client clip relative to its native fit (1.00 = full 720p frame fitted to 1080×1920). Anchor for all scales = speaker's chest (canvas 540, 1125) unless stated.

### BEAT 01 — 0.00–1.63 s (f0–f39) · NAME

**SCRIPT** "Hey, main ARS Studio se hoon."
**STORY PURPOSE** Hook plus identity. The name has to be the thumbnail frame.
**EDIT DECISION** Stay on him (warmth, eye contact) and push in toward the face. The frame opening up on "Hey" makes the greeting physical.
**PRIMARY VISUAL** Talking head (WIDE → TIGHT) + kinetic type behind head.
**VISUAL DESCRIPTION** f0: speaker at WIDE 1.25, framed by four cobalt crop-mark corners (L-shapes, 70 px arms, 6 px stroke) inset to a tight 9:16 rectangle around him (x 300–780, y 620–1460). Above it, a small mono chip reads `ARS ● 00:00:00:00`. On "Hey" the corners snap out to the safe-zone edges and he pushes in. "Hey," appears in italic serif; ARS racks into focus behind his head; STUDIO types out under it.
**REFERENCE CONNECTION** Opening push-in to tight, lead-in → giant name, name behind head, pattern-interrupt first frame.
**ADAPTATION** Viewfinder instead of mirror tile; rack focus instead of glow; ink instead of red; mono typewriter STUDIO instead of chips.
**MOTION**
- f0–f1: hold (corners already on screen, so the first frame is "mid-shot").
- f2: corners fly from inset to safe-zone positions (x 86/994, y 230/1574) in 5 f, expo-out, 2 f motion trail.
- f2–f22: A-roll push 1.25 → 1.65, expo-out (half the travel in the first 5 f), no overshoot.
- f2: "Hey," fades in 3 f, y −12 px → 0.
- f18–f26: ARS rack-focus: each letter Gaussian blur 40 → 0 and scale 104% → 100%, opacity 0 → 100% in the first 3 f; letter stagger 2 f (A f18, R f20, S f22).
- f28–f34: STUDIO types left→right, 1 letter/f, hard on (no fade), like a timecode.
- Timecode chip counts up in real time from f2 (constant micro-motion).
- Keyframe diamonds: 1 pops at ARS's top-left corner f18, 1 at the end of STUDIO f34.
**TYPOGRAPHY**
- "Hey," Instrument Serif Italic, 96 px, ink #121318, left-aligned at x 150, baseline y 360.
- "ARS" Inter Tight Black, caps, cap height 360 px, tracking −30, ink, centered, spans x ≈ 130–950 (76% width), baseline y 790. His head (top ≈ 653 px at TIGHT) occludes the lower half of "R". **Behind the matte.**
- "STUDIO" JetBrains Mono Medium, caps, 44 px, cobalt #2E3BFF, tracked to the exact width of ARS, baseline y 860, **in front** of the matte, sitting on his shoulders like a lower third.
- Timecode chip: JetBrains Mono 26 px, ink 60%, top-left at x 86, y 230.
**TRANSITION** Out via T1 (letterbox).
**DURATION** 1.63 s.

### T1 — 1.63–1.80 s (f39–f43) · LETTERBOX RESET (breath gap)
- f39–f41: two ink (#121318) bars slam in from top and bottom to 40% of the frame each, leaving a 20% slit across his eyes. 3 f, expo-in.
- Under cover: ARS squashes to 0% height toward its baseline; corners and timecode cut out; A-roll jumps 1.65 → 1.25.
- f42–f45: bars retract in 4 f, expo-out.
- SFX: camera shutter click at f40 plus a short air whoosh starting f36.

### BEAT 02 — 1.80–3.08 s (f43–f74) · FOR BRANDS / HIGH QUALITY

**SCRIPT** "Hum brands ke liye high quality…"
**STORY PURPOSE** Credibility. Every studio claims quality, so prove it immediately.
**EDIT DECISION** Wide frame so there's room for evidence above him. Show their real brand work, not words.
**PRIMARY VISUAL** Talking head WIDE + three inset proof cards (playing video).
**VISUAL DESCRIPTION** A row of three 9:16 cards above his head, perfectly aligned like a contact sheet: x 120–370, 415–665, 710–960; y 270–714 (250×444 each). Each card plays a different ARS brand reel (product, food, fashion/founder). A cobalt chip FOR BRANDS sits on the top-left corner of card 1. Under the row, the italic serif "high-quality."
**REFERENCE CONNECTION** Proof cards arriving on the noun (CEAT/FBF), wide state for evidence, a tick per card.
**ADAPTATION** No tilt, no wobble, no overlapping scrapbook. Straight, gridded, precise. The cards move only inside (the clips play). Cobalt crop-mark corners on each card instead of a maroon border.
**MOTION**
- Card pops: card 1 f46 ("brands"), card 2 f58 ("liye"), card 3 f66 ("quality"). Each goes from scale 70%, y +40 px, opacity 0 → 104% at +4 f → 100% at +9 f (one soft spring, no rotation).
- Chip FOR BRANDS slides in from x −60 px with horizontal motion blur, f46–f50.
- "high-quality" f60: letters fade up with 1 f stagger, y +10 → 0.
- A-roll: static at 1.25 (a hold so the eye can scan the cards).
- Keyframe diamond on each card's top-right corner as it lands (f50, f62, f70).
**TYPOGRAPHY** Chip: JetBrains Mono Medium 30 px caps, tracking +200, canvas-colored (#F1E3DD) on cobalt, radius 8, padding 14×8. "high-quality": Instrument Serif Italic 84 px, cobalt, centered, baseline y 785 (between the row and his head).
**B-ROLL** Real ARS client reels (preferred). AI fallbacks: Flow CLIP 01–03 (§14). Grade all three to the same neutral key (contrast +8, saturation −10) so the row reads as one set.
**GRAPHICS** Card: radius 20 px, 2 px ink hairline, shadow 0 18 px 40 px ink @ 18%. Crop-mark corners 28 px arms, 4 px cobalt, offset 10 px outside the card.
**TRANSITION** Out via T2.
**DURATION** 1.28 s.

### T2 — 3.08–3.26 s (f74–f78) · ROW COLLAPSES INTO THE PLAYHEAD (in-speech, on "aur")
- f74–f77: the three cards squash horizontally toward the center (scale-X 100 → 0, 3 f, expo-in) and become a single vertical **6 px cobalt line**, the playhead, which jumps to x 110 (left edge of the coming hero word).
- f75–f85: A-roll punch 1.25 → 1.65, expo-out (half the travel by f79).
- SFX: low **sub impact** landing exactly at f78 on "engaging". This is the one big hit in the video.

### BEAT 03 — 3.26–4.58 s (f78–f110) · ENGAGING VIDEOS — PEAK

**SCRIPT** "…engaging videos create karte hain."
**STORY PURPOSE** The core category claim, so this is the energy peak.
**EDIT DECISION** Tight punch plus impact plus the biggest sans word. Then visualize "create" by making the word itself get built.
**PRIMARY VISUAL** Talking head TIGHT + kinetic type + playhead scrub.
**VISUAL DESCRIPTION** ENGAGING lands behind his head as an **outline** (2.5 px ink stroke, no fill). "videos" lands in cobalt italic serif to the right of his head. On "create" the cobalt playhead sweeps left→right across ENGAGING, and each letter it passes fills solid ink: the word is rendered as he says *create*.
**REFERENCE CONNECTION** The punch-in + impact + title on the category word (CREATIVE beat); the letter cascade (IDEAS); the footage drift during a hold.
**ADAPTATION** Outline-to-solid render reveal driven by a playhead. It's specific to a video studio and wasn't in the reference.
**MOTION**
- f78–f84: ENGAGING letter cascade, 1 f stagger, each letter y +30 → 0 with vertical motion blur, expo-out.
- f87–f91: "videos" fades in, x +24 → 0, expo-out.
- f95–f109: playhead scrubs x 110 → 970 **linearly** (the one linear move in the edit, because a playhead is mechanical). Letter fill flips 0 → 100% in 2 f as the line crosses each letter's center.
- f88–f110: A-roll slow drift down 24 px, linear (the reference's held-statement drift).
- Keyframe diamond rides the top of the playhead.
**TYPOGRAPHY**
- ENGAGING: Inter Tight Black caps, cap 150 px, tracking −20, width 82% (x 95–985), baseline y 700. **Behind the matte**; his head covers the lower part of "GAG".
- "videos": Instrument Serif Italic 150 px, cobalt, x 640–990, baseline y 830. **In front**, beside the head, never over the face.
**SFX** Sub impact f78. Short **tape-scrub** texture f95–f109, low in the mix.
**TRANSITION** Out via T3.
**DURATION** 1.32 s.

### T3 — 4.58–4.88 s (f110–f117) · HORIZONTAL WHIP (breath gap)
- f110: the playhead flashes (opacity 100 → 0 → 100 in 2 f) at the right edge.
- f111–f113: whole frame directional blur 80 px horizontal, right→left (it continues the playhead's direction). ENGAGING and "videos" exit under the smear.
- Under cover: A-roll 1.65 → 1.45 (MID).
- f114–f117: blur resolves to 0.
- SFX: fast whoosh f108–f113.

### BEAT 04 — 4.88–6.13 s (f117–f147) · PREMIUM — THE BREATH

**SCRIPT** "Jo actually premium feel karein."
**STORY PURPOSE** The standard. ARS sells *feel*.
**EDIT DECISION** Do less. After the peak, the frame slows down: one slow, elegant word, no diamonds, no cards. The restraint is what makes "premium" credible. This is the planned slowdown in the rhythm.
**PRIMARY VISUAL** Talking head MID + single serif hero.
**VISUAL DESCRIPTION** A small mono ACTUALLY, then *premium* in a large italic serif resolving slowly across the top third, with a single cobalt underline drawn on "feel".
**REFERENCE CONNECTION** Lead-in + hero hierarchy; hero in the top third.
**ADAPTATION** The only serif hero and the only slow entrance, so the type style itself says the word. It's placed **in front of** the speaker (it sits above his head, no overlap), deliberately breaking the behind-head pattern to signal a change of register.
**MOTION**
- f117–f147: A-roll **slow linear push 1.45 → 1.53** for the whole beat (the only visible, uncovered camera move after the opening).
- f119: ACTUALLY fades in, 4 f.
- f128–f140: *premium* letters resolve blur 20 → 0, opacity 0 → 100, 2 f stagger, each letter taking 8 f, ease-out sine. About twice as slow as everything else.
- f137–f147: cobalt underline (6 px) draws left→right under *premium*, ease-in-out, 10 f.
**TYPOGRAPHY**
- ACTUALLY: JetBrains Mono Medium caps 32 px, tracking +300, ink 60%, centered, baseline y 330.
- *premium*: Instrument Serif Italic, lowercase, 300 px font size, ink, tracking −10, centered, width ≈ 80%, baseline y 600.
**SFX** None except a soft airy swell under the voice. Music drops its hats for this beat (the mix breathes too).
**TRANSITION** Out via T4.
**DURATION** 1.25 s.

### T4 — 6.13–6.62 s (f147–f159) · 9:16 FRAME IRIS — THE PIVOT (longest gap)
- f147–f153: three rounded-rect outlines at 9:16 aspect (cobalt, 10 px stroke, radius 40) spawn on his face at 8% scale and expand past the frame edges, 2 f apart, each over 6 f, expo-in.
- f153–f156: a fourth 9:16 shape, **solid cobalt fill**, expands and covers the full frame for 2 f (f155–f156). That's the cut point.
- Under cover: *premium* and the underline cut out; A-roll jumps to WIDE 1.25 and **reframes left** (speaker center at x ≈ 400 instead of 540).
- f157–f159: the solid frame keeps expanding past the edges, revealing the new layout.
- SFX: reverse-whoosh f145–f155 into a soft shutter + sub drop at f155.
- Meaning: the frame shape of a phone screen is what ARS delivers, and the pivot from "us" to "you" passes through that shape.

### BEAT 05 — 6.62–8.69 s (f159–f209) · YOUR BRAND — THE TURN

**SCRIPT** "Agar aap bhi apne brand ke liye aisa content chaahte hain,"
**STORY PURPOSE** Turns the video toward the viewer.
**EDIT DECISION** Reframe to make literal room for the viewer: an empty media slot labelled YOUR BRAND, which fills when he says *aisa content* (content like this).
**PRIMARY VISUAL** Talking head WIDE (shifted left) + slot card + split hero.
**VISUAL DESCRIPTION** Right side: a 9:16 card (x 700–1000, y 600–1133) drawn as an **empty timeline slot**: dashed cobalt border, faint cobalt-tinted fill, a thin "+" in the middle, mono label YOUR BRAND. Top: "your" (cobalt italic serif) + BRAND (ink grotesk, behind his head). On "content" the slot fills with a playing miniature of **this video's own Beat 01** (the ARS frame), and the dashed border snaps solid.
**REFERENCE CONNECTION** The reframe to free one side for cards (the reference's final beat); the self-reference card; title plus card stack.
**ADAPTATION** Mirrored (speaker left, card right); one card, not a stack; the card starts *empty*, so it's about the viewer's future rather than past work.
**MOTION**
- f171 ("apne"): slot card pops with the B02 spring (70 → 104 → 100%, +40 px y). If the stutter needs cutting, hide the jump cut on this frame with a 2 f 1.25 → 1.28 nudge.
- f171: "your" fades in, x −20 → 0, 4 f.
- f175–f181 ("brand"): BRAND letter cascade, 1 f stagger, y +30 → 0, blur.
- f192–f197 ("content"): the miniature drops into the slot (scale 112 → 100% inside the card's mask, 5 f, expo-out). The border goes from dashed cobalt to a 2 px ink hairline with crop-mark corners. Keyframe diamonds pop on two diagonal corners.
- f160–f209: A-roll static at WIDE with the left reframe.
**TYPOGRAPHY**
- "your": Instrument Serif Italic 130 px, cobalt, x 110, baseline y 330.
- BRAND: Inter Tight Black caps, cap 230 px, ink, x 100–980, baseline y 640. **Behind the matte** (his head, now at x ≈ 330–470, covers part of "R").
- YOUR BRAND label: JetBrains Mono Medium 26 px caps, tracking +200, cobalt, top-left inside the slot.
**GRAPHICS** Slot dashed border: 4 px cobalt, dash 18 / gap 12, radius 24, fill cobalt @ 5%. "+": 2 px cobalt, 48 px.
**SFX** UI tick at f171; a soft "drop" thunk + tick at f192.
**TRANSITION** Out via T5.
**DURATION** 2.07 s (the longest beat, because the viewer is now the subject).

### T5 — 8.69–8.92 s (f209–f214) · HALF-LETTERBOX SNAP (breath gap)
- f209–f211: ink bars close to 30% each (a half-shutter, echoing T1), 3 f.
- Under cover: slot card and BRAND cut out; A-roll recenters (x back to 540) and jumps 1.25 → 1.65.
- f212–f214: bars retract, 3 f.
- SFX: lighter shutter click f210.

### BEAT 06 — 8.92–9.69 s (f214–f233) · LET'S CONNECT

**SCRIPT** "toh let's connect."
**STORY PURPOSE** The call to action. It should feel effortless and warm.
**EDIT DECISION** Tight on the face (direct ask); the word visualizes its own meaning.
**PRIMARY VISUAL** Talking head TIGHT + split-and-join hero.
**VISUAL DESCRIPTION** "let's" in cobalt italic serif; CONNECT assembles from two halves. CONN slides in from the left, ECT from the right; each half's leading edge carries a keyframe diamond, and the two diamonds meet and merge into one at the join.
**REFERENCE CONNECTION** Hero behind head, punch to tight for statements, lead-in + hero.
**ADAPTATION** The split-and-join (keyframe to keyframe) is new and comes from the meaning of the word.
**MOTION**
- f216: "let's" fades in 3 f, y −10 → 0.
- f222–f229: CONN from x −240, ECT from x +240, expo-out 7 f, horizontal motion blur. The diamonds meet at f228, merge (scale 100 → 140 → 0) by f231.
- A-roll static at TIGHT.
**TYPOGRAPHY**
- "let's": Instrument Serif Italic 110 px, cobalt, x 150, baseline y 400.
- CONNECT: Inter Tight Black caps, cap 170 px, ink, centered, width ≈ 82%, baseline y 720, **behind the matte**.
**SFX** Two soft ticks converging, then a crisp click at f228.
**DURATION** 0.77 s.

### BEAT 07 — 9.69–10.62 s (f233–f255) · END LOCKUP
See §12.

---

## 06 — B-ROLL STRATEGY

There is **no full-screen B-roll**; this is a direct transfer. Every insert is evidence, shown in a card while he stays on screen.

| # | Beat | Content | Type | Still / video | Why |
| --- | --- | --- | --- | --- | --- |
| BR1 | 02, card 1 (f46) | ARS product reel (e.g. a skincare or D2C product ad) | Literal proof | Video, playing | "brands" means real brand work |
| BR2 | 02, card 2 (f58) | ARS food/café reel | Literal proof | Video, playing | Shows range |
| BR3 | 02, card 3 (f66) | ARS founder/fashion talking-head reel with captions | Literal proof | Video, playing | Shows they make *this* format |
| BR4 | 05, slot (f192) | Miniature render of this edit's Beat 01 (f0–f39) | Self-referential | Video (nested comp) | "aisa content" = content like this. Needs no new asset. |

**Rule:** BR1–BR3 should be **real ARS deliverables**. Only use the AI fallbacks (Flow CLIP 01–03) if ARS has no usable work, and then don't caption them as client work. Choose clips whose first 0.5 s are readable (a clear product or face, high contrast) because each card is on screen only ~1 s.

---

## 07 — MOTION GRAPHICS STRATEGY

| Graphic | Job | Where |
| --- | --- | --- |
| Viewfinder crop-mark corners | Says "this is footage, through a studio's lens"; makes the first frame mid-action | B01, then reused on cards |
| Timecode chip | Brand texture + constant micro-motion in the opening | B01 only |
| Letterbox shutter bars | Reset device made from cinema framing; rhymes with the end | T1, T5, end |
| Proof card row | Evidence | B02 |
| FOR BRANDS / YOUR BRAND / DM chips | Utility labels | B02, B05, end |
| Playhead line | Connects T2 → B03 → T3; visualizes "create" | T2–T3 |
| Outline → solid render reveal | The word gets made on "create" | B03 |
| 9:16 frame iris | Pivot wipe in the shape of the deliverable | T4 |
| Empty slot card | The viewer's brand as an empty slot waiting to be filled | B05 |
| Keyframe diamonds ◆ | Landing accents (replaces confetti) | ~10 uses |
| Split-and-join CONNECT | The CTA word does what it says | B06 |

Not used, deliberately: floating decorative circles, particles, HUD frames, grids, starbursts, sparkles, glow, halftone.

---

## 08 — TYPOGRAPHY SYSTEM

| Voice | Font (free) | Use | Color | Rules |
| --- | --- | --- | --- | --- |
| **Hero sans** | Inter Tight Black (900), caps | ARS, ENGAGING, BRAND, CONNECT | Ink #121318 | Cap 150–360 px, 76–82% width, tracking −20 to −30, top third, **behind head** |
| **Accent serif** | Instrument Serif Italic | Hey, high-quality, videos, *premium*, your, let's | Cobalt (ink for *premium*) | Lowercase, never more than 1–3 words, in front of the speaker |
| **Utility mono** | JetBrains Mono Medium, caps | STUDIO, timecode, ACTUALLY, chips | Cobalt / ink 60% / canvas-on-cobalt | 26–44 px, tracking +200 to +600 |

- **Only English keywords are typeset.** Hindi connecting words are spoken, never written. No subtitles.
- Per beat: at most one hero-sans word + one accent-serif word + one mono label.
- Ratio of accent to hero ≈ 1:3. Mono labels are ≈ 1:8.
- Words appear on, or 1–2 frames before, the spoken syllable.
- The sans hero never sits over the face. Serif accents never overlap the head.
- No white type on the footage. The only inverted type is the end card.

---

## 09 — MOTION SYSTEM

| Trait | Value |
| --- | --- |
| Entrances | 3–7 f @ 24 fps, expo-out, motion blur on anything moving > 20 px/f |
| Objects (cards, slot) | Soft spring 70 → 104 → 100%, no rotation |
| Type | Letter cascades at 1 f stagger. Exception: *premium* at 2 f stagger / 8 f per letter |
| Camera (A-roll) | Expo-out scale moves, never overshoot, always hidden in a transition, except the opening push and the B04 linear push |
| Linear moves | Only two, both on purpose: the playhead scrub and the B04 push |
| Exits | Never a plain fade: squash (ARS, cards), smear (ENGAGING), covered by a wipe (*premium*, BRAND) |
| Idle life | Clips playing inside cards, timecode counting, footage drift. No wobble, no flicker |
| Event density | ~1 event / 0.4 s; longest gap with no new event ≈ 0.45 s (inside B04, by design) |

**Scale ladder:** WIDE 1.25 (evidence) → MID 1.45 (premium) → TIGHT 1.65 (name, category, CTA).
Sequence: 1.25 → 1.65 (B01) → 1.25 (B02) → 1.65 (B03) → 1.45 → 1.53 (B04) → 1.25 + left (B05) → 1.65 (B06) → 1.70 (end).

---

## 10 — COLOR & COMPOSITING

**Palette**

| Role | HEX |
| --- | --- |
| Canvas (from footage) | #F1E3DD (lift to ≈ #F3E7E1 in grade) |
| Ink (type, bars, end card) | #121318 |
| Cobalt accent | #2E3BFF |
| Cobalt deep (pressed / shadow states) | #1B23B8 |
| Cobalt tint (slot fill) | #2E3BFF @ 5% |
| Chip text | #F1E3DD |

**Grade:** keep the clean, bright, low-saturation look. Lift the wall slightly and pull orange/red saturation in the background by ~10% so the cobalt is clearly the only saturated hue. Keep skin and the chair natural; the cognac chair is cobalt's complement and makes the accent pop. No grain, no vignette, no leaks.

**Layer order (back → front):**
1. Footage background
2. Hero sans words (ARS, ENGAGING, BRAND, CONNECT)
3. **Speaker matte** (duplicate of the A-roll with background removed: CapCut "Remove background" / AE Roto Brush 3 / Resolve Magic Mask; only head and shoulders need to be clean)
4. Serif accents, mono labels, chips, *premium*
5. Cards + slot + crop-marks
6. Keyframe diamonds, playhead
7. Transition overlays: letterbox bars, frame iris, directional blur (adjustment layer)

The matte must follow the scale ladder exactly. Apply scale keys to a parent/compound clip that contains both the footage and the matte.

---

## 11 — OPENING (0.00–1.63 s)

- **First frame (f0):** speaker at 1.25 inside tight cobalt crop-marks, with the timecode chip at 00:00:00:00. It reads as "a shot being framed," a frame already in progress before any sound, and it's specific to a studio.
- **First sound (f2):** "Hey" on the cut (the 0.34 s head trim), with the music bed starting on the same frame, no fade-in.
- **First movement (f2):** corners burst outward + push-in toward the face (1.25 → 1.65), so greeting and approach happen together.
- **First text:** "Hey," (serif) teaches the accent voice; at f18 ARS teaches the hero voice; at f28 STUDIO teaches the mono voice. **All three type voices are introduced in 1.2 s**, the same way the reference teaches its kit in the opening.
- **Hook strategy:** curiosity about the frame (the viewfinder) → the payoff of the name. Thumbnail frame ≈ f26–f38: ARS behind his head, STUDIO across his shoulders.
- **Into the story:** letterbox shutter (T1) = "cut, next shot."

## 12 — ENDING (9.52–10.62 s)

- Speech ends f228; footage ends f233. Freeze f232 and keep the scale moving 1.65 → 1.70 (f228–f244) so the freeze reads as motion.
- f236–f244: ink letterbox bars close from top and bottom over 8 f (expo-in-out) and meet in the center. This bookends the T1 shutter and the opening viewfinder: the frame opened on "Hey" and closes on "connect."
- f244 (10.17 s): full ink card. Centered, canvas-colored "ARS" (Inter Tight Black, cap 200 px) with "STUDIO" in mono (40 px, tracked to width) below it, then a cobalt chip `DM "CONNECT"` (or the client's handle / link-in-bio, confirm with the client). The lockup appears with a 4 f opacity cut-in. No animation beyond that, because the stillness is the full stop.
- f244: shutter click + the music's final hit with a short tail.
- f255 (10.62 s): hard cut out. **Resolve, don't loop.**

---

## 13 — ASSET CHECKLIST

**Client footage**
- [ ] The A-roll, **upscaled to ≥ 1080×1920** (ideally 1440×2560) before editing
- [ ] Person matte of the A-roll (generated in your NLE)
- [ ] Confirm the "aap bhi" stutter by ear

**B-roll**
- [ ] BR1 — real ARS product reel (≥ 2 s usable, vertical)
- [ ] BR2 — real ARS food/café reel
- [ ] BR3 — real ARS talking-head/founder reel
- [ ] BR4 — nested render of this edit's f0–f39 (make it after Beat 01 is built)
- [ ] Fallbacks only if needed: Flow CLIP 01–03 + start frames IMAGE 01–03

**Motion graphics**
- [ ] Crop-mark corner set (viewfinder size + card size)
- [ ] Timecode chip
- [ ] Letterbox bars (full + half variants)
- [ ] Card template (radius, hairline, shadow, corners, mask)
- [ ] Chips: FOR BRANDS, YOUR BRAND, DM "CONNECT"
- [ ] Playhead line + render-reveal setup on ENGAGING
- [ ] 9:16 frame iris (3 outlines + 1 solid)
- [ ] Empty slot card (dashed) + filled state
- [ ] Keyframe diamond (cobalt fill + ink-outline variants)
- [ ] CONNECT split-and-join
- [ ] End lockup card

**Typography**
- [ ] Hey, · ARS · STUDIO · FOR BRANDS · high-quality · ENGAGING · videos · ACTUALLY · premium · your · BRAND · YOUR BRAND · let's · CONNECT · ARS STUDIO · DM "CONNECT"
- [ ] Fonts: Inter Tight (Black), Instrument Serif (Italic), JetBrains Mono (Medium). All free on Google Fonts.

**Sound**
- [ ] Music: minimal, clean house/UK-garage-adjacent bed at ~120 BPM. Muted kick, round sub, sparse pluck, no vocals. Ducked 16–18 dB under the voice. Hats drop out in B04. Final hit lands at f244.
- [ ] SFX: camera shutter ×3 (T1, T5, end), air whoosh (T1), fast whoosh (T3), reverse-whoosh + sub drop (T4), **sub impact** (f78 only), tape-scrub (f95–f109), soft UI ticks ×5 (card pops, slot pop, slot fill), soft drop thunk (f192), converging ticks + click (f228)
- [ ] Master to −14 LUFS integrated, true peak ≤ −1 dBTP

**AI-generated assets**
- Generate in Flow: only CLIP 01–03, and only if real ARS work isn't available.
- **Don't** generate: proof of real clients, the end card, any type, the slot fill (use the nested comp), or extra A-roll.

---

## 14 — GOOGLE FLOW VIDEO PROMPTS (fallback proof cards only)

All three are styled to sit inside the edit's world: warm off-white, ink-black and one cobalt accent, a clean commercial look. Generate at 9:16, 5 s. If Flow allows, use IMAGE 01–03 as start frames for consistency.

**CLIP 01 — Product (serum)**
Prompt:
> Vertical 9:16 commercial product shot, 5 seconds. A frosted-glass serum bottle with a matte black dropper cap stands on a smooth warm off-white plaster plinth in front of a seamless warm off-white studio backdrop. The liquid inside is a vivid cobalt blue. A hard key light from camera-left at 45 degrees casts a crisp, clean shadow to the right; a slow band of light sweeps across the glass from left to right over the full clip, making the edges glint. Camera at eye level with the bottle, 85mm macro lens feel, very slow steady push-in, shallow depth of field with the backdrop softly out of focus. Minimal, premium, clean commercial grade, low saturation everywhere except the cobalt liquid. No text, no logos, no hands, no people.

**CLIP 02 — Food & beverage (café)**
Prompt:
> Vertical 9:16 close-up, 5 seconds. A barista's hands, sleeves of a black apron visible, pour steamed milk into an espresso in a matte off-white ceramic cup on a warm off-white stone counter, forming smooth latte art. Soft daylight from a large window on the left, gentle shadows, clean warm-neutral palette with deep black accents. Camera slightly above the cup at a 35-degree angle, 50mm lens feel, locked off with a barely perceptible slow push-in, shallow depth of field. Believable real-time motion of the milk pour, fine steam rising. Premium café commercial look, natural textures, no text, no logos.

**CLIP 03 — Founder / creator talking head (format proof)**
Prompt:
> Vertical 9:16 medium close-up, 5 seconds. A confident young South Asian woman in her late twenties wearing a tailored black blazer speaks warmly to camera, gesturing lightly with one hand, seated against a seamless cobalt-blue studio backdrop. Soft frontal key light with gentle fill, natural skin tones, subtle rim light separating her from the background. Camera at eye level, 50mm lens feel, locked-off with a very slow push-in, shallow depth of field. Clean, modern, premium social-media brand video look. Natural lip and head movement. No captions, no text, no logos.

---

## 15 — IMAGE / B-ROLL PROMPTS (start frames for CLIP 01–03)

**IMAGE 01 — Serum start frame (still)**
Prompt:
> Vertical 9:16 studio product photograph. A frosted-glass serum bottle with a matte black dropper cap, filled with vivid cobalt-blue liquid, centered on a smooth warm off-white plaster plinth against a seamless warm off-white backdrop. Hard key light from the left at 45 degrees, crisp shadow falling right, a thin highlight along the bottle's left edge. 85mm macro perspective at eye level, shallow depth of field. Minimal premium commercial look, low saturation except the cobalt. No text, no logos, no hands.

**IMAGE 02 — Café start frame (still)**
Prompt:
> Vertical 9:16 photograph. Close-up of a matte off-white ceramic cup holding fresh espresso on a warm off-white stone counter; a barista's hand in a black apron sleeve holds a steel milk pitcher tilted just above the cup, about to pour. Soft window daylight from the left, gentle shadows, warm-neutral palette with deep black accents, light steam. Camera 35 degrees above, 50mm lens perspective, shallow depth of field. Premium café commercial photography, no text, no logos.

**IMAGE 03 — Creator start frame (still)**
Prompt:
> Vertical 9:16 portrait photograph. A confident young South Asian woman in her late twenties in a tailored black blazer, seated, looking directly into the camera mid-sentence with a warm half-smile, one hand slightly raised. Seamless cobalt-blue studio backdrop, soft frontal key light, gentle fill, subtle rim light, natural skin tones. Eye-level 50mm perspective, medium close-up, shallow depth of field. Clean modern premium brand-video look. No text, no logos.

---

## 16 — MOTION GRAPHIC BUILD NOTES

**Global setup**
- Comp/project: 1080×1920, 24 fps, 10.62 s (255 f). Import the upscaled A-roll; trim the first 0.34 s (8 f).
- Put the A-roll + its matte in **one compound clip (CapCut) / pre-comp (AE)** and keyframe scale + position on that, so the matte always lines up.
- AE easing for "expo-out": Graph Editor, outgoing influence ≈ 90%, incoming ≈ 10% (or a Flow/Motion preset "Expo Out"). CapCut: custom curve, steep start, long tail.

**Crop-mark corners** — Shape layer: 4 L-paths (70 px arms, 6 px cobalt stroke, square cap). Animate the group's Scale from the inset rectangle to the safe-zone rectangle (f2–f7) with Echo or CC Force Motion Blur for the trail. CapCut: 4 PNG corners, each with a position keyframe.

**Rack-focus ARS** — Per-letter text animator (AE: Range Selector by character, offset animated) driving Blur 40 → 0, Scale 104 → 100, Opacity 0 → 100. CapCut: split ARS into 3 text layers, each with Gaussian Blur + scale keyframes, offset 2 f.

**Typed STUDIO** — AE: Text animator Opacity 0 with Range Selector Start animated, Shape: Square, smoothness 0% (hard on). CapCut: "Typewriter" text animation, duration adjusted to 6 f.

**Timecode chip** — AE: Timecode effect (or a Source Text expression `timeToTimecode(time)`) inside a rounded rect. CapCut: use a pre-rendered transparent clip.

**Letterbox bars** — Two ink solids (1080×768 each, i.e. 40%), positioned off-frame; keyframe Y in 3 f (expo-in) and out in 4 f (expo-out). Half variant: 30% (576 px).

**Card template** — Pre-comp 250×444: clip → mask (rounded rect, radius 20) → 2 px ink stroke → Drop Shadow (ink, 18%, distance 18, softness 40) → 4 corner marks. Pop: Scale 70 → 104 (f+4) → 100 (f+9), Position y +40 → 0, Opacity 0 → 100 in the first 3 f.

**Row → playhead collapse (T2)** — Parent all three cards to a null at the row center; Scale X 100 → 0 over 3 f (expo-in). On f77 reveal a 6 px × 520 px cobalt solid (the playhead) at the center, then move it to x 110 in 1 f.

**ENGAGING render reveal** — Two copies of the text layer: (A) stroke only, 2.5 px ink; (B) fill only, ink. Mask B with a rectangle whose right edge is linked to the playhead's x position (AE expression on the mask path, or a Linear Wipe on B with Transition Completion tied to playhead x). Letters snap fully on as they're crossed. CapCut approximation: duplicate the fill layer and keyframe a linear "wipe" mask from left to right over 14 f, in sync with the playhead clip.

**Horizontal whip (T3)** — Adjustment layer, Directional Blur, direction 90°, blur 0 → 80 → 0 over f111–f117. Add Transform position x −40 px over the same frames for the smear feel.

**Slow *premium*** — Per-character animator: Blur 20 → 0, Opacity 0 → 100, offset so each letter takes 8 f, 2 f stagger, Ease Out (sine). Underline: a 6 px shape path, Trim Paths End 0 → 100 over 10 f, Easy Ease.

**9:16 frame iris (T4)** — 4 rounded rects (aspect 9:16, radius 40). Three are stroke only (10 px cobalt), one is solid cobalt. Each scales 8% → 260% over 6 f (expo-in), started at f147, f149, f151, f153 (the solid one). Anchor point on the speaker's face. The A-roll reframe keyframes go on f155 (fully covered).

**Slot card** — Same template, but the stroke uses Dashes (dash 18, gap 12, 4 px cobalt), fill cobalt @ 5%, centered "+" (two 48 px lines). At f192 swap to the filled version: nested render of f0–f39 inside the mask, scale 112 → 100% over 5 f; crossfade the stroke dashed → solid over 2 f.

**CONNECT split-and-join** — Two text layers, "CONN" and "ECT", kerned as one word at rest. Position from ∓240 px over 7 f (expo-out) with motion blur. Diamonds (cobalt, 22 px, rotated 45°) parented to each half's inner edge; on contact, scale 100 → 140 → 0 over 3 f.

**Keyframe diamond** — A 22 px square rotated 45°, cobalt fill (variant: 3 px ink outline). Life 4–6 f: Scale 0 → 120 → 100, hold, then 100 → 0. Keep it as one preset and reuse it.

**End card** — Ink solid behind the letterbox bars; at f244 cut in the ARS / STUDIO lockup + chip at 100% opacity over 4 f. Nothing else moves.

---

## 17 — FINAL MASTER TIMELINE (editor version)

| Time (s) | Frames | Script | Visual / Treatment | A-roll | Text | B-roll / Graphic | Transition / SFX |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00–0.10 | 0–2 | — | Viewfinder first frame | 1.25 | TC chip | Inset crop-marks | — |
| 0.10–1.63 | 2–39 | Hey, main ARS Studio se hoon | Name hook, push in | 1.25 → 1.65 (f2–22) | Hey, (f2) · ARS rack focus (f18) · STUDIO typed (f28) | Corners snap open; ◆ ×2 | Music starts f2 |
| 1.63–1.80 | 39–43 | (gap) | **T1** letterbox | → 1.25 | ARS squashes | Ink bars 40% | Shutter + whoosh |
| 1.80–3.08 | 43–74 | Hum brands ke liye high quality | Proof row | 1.25 hold | FOR BRANDS chip (f46) · high-quality (f60) | Cards f46 / f58 / f66, ◆ each | Tick ×3 |
| 3.08–3.26 | 74–78 | aur | **T2** row → playhead | → 1.65 | — | Cards squash to line | **Sub impact f78** |
| 3.26–4.58 | 78–110 | engaging videos create karte hain | Peak + render reveal | 1.65 + drift 24 px | ENGAGING outline (f78) · videos (f87) · fills on scrub (f95–109) | Playhead scrub, linear | Tape scrub |
| 4.58–4.88 | 110–117 | (gap) | **T3** horizontal whip | → 1.45 | exits in smear | Directional blur | Whoosh |
| 4.88–6.13 | 117–147 | Jo actually premium feel karein | **Breath** | 1.45 → 1.53 linear | ACTUALLY (f119) · *premium* slow (f128) · underline (f137) | None | Hats drop |
| 6.13–6.62 | 147–159 | (gap) | **T4** 9:16 iris | → 1.25, reframe left | — | 3 outlines + solid | Rev-whoosh + sub drop f155 |
| 6.62–8.69 | 159–209 | Agar aap bhi apne brand ke liye aisa content chaahte hain | Turn to viewer | 1.25 left | your (f171) · BRAND (f175) · YOUR BRAND label | Empty slot pops f171 → fills with B01 mini f192, ◆ ×2 | Tick, drop thunk |
| 8.69–8.92 | 209–214 | (gap) | **T5** half-letterbox | → 1.65 center | — | Ink bars 30% | Light shutter |
| 8.92–9.69 | 214–233 | toh let's connect | CTA | 1.65 | let's (f216) · CONNECT join (f222–229) | ◆ pair merges f228 | Ticks + click |
| 9.69–10.17 | 233–244 | — | Freeze + close | 1.65 → 1.70 | — | Letterbox closes f236–244 | — |
| 10.17–10.62 | 244–255 | — | End lockup | — | ARS / STUDIO · DM "CONNECT" | Ink card | Shutter + final hit f244 · hard out |

---

## 18 — DO / DON'T (this edit)

| Do | Don't |
| --- | --- |
| Keep every frame ≥ 1.25× (watermark + framing) | Show the native 1.00× frame, ever |
| Upscale the 720p A-roll before punching to 1.65× | Punch a 720p file to 1.65× and call it premium |
| Ink + cobalt only; cobalt = "look here" | Use red, or any second accent |
| Typeset only the English keywords | Subtitle the Hindi, or caption every word |
| Put sans heroes behind his head | Put text over his face |
| Keep cards straight and gridded | Tilt, wobble or scrapbook-stack them (that's V1 Forge's look) |
| Let B04 *premium* breathe with no diamonds or cards | Fill the premium beat with effects |
| Use the letterbox / playhead / 9:16 iris for resets | Use halftone, star wipes, comet arcs or pixel confetti |
| Hide every scale jump inside a transition | Let a scale change happen in the open (except the opening push and the B04 push) |
| Use real ARS work in the cards | Present AI fallback clips as real client work |
| One sub impact, on ENGAGING only | Put impacts on every transition |
| Resolve on the letterbox close + logo | Loop, fade to white or end mid-motion |

---

### Final quality check
1. Influenced by the reference? Yes: anchored speaker, behind-head keyword, scale-as-cut, proof cards, one-accent signalling, the same reset logic and audio grammar.
2. Original to the client? Yes: different palette, three-voice type system, studio-tool motifs, a viewer-facing second half, the self-referential slot fill.
3. Principles over surface? 11 of the 16 DNA items transferred; nearly all reference-specific components were ignored or redesigned.
4. Every visual comes from a spoken line (name → proof → create → premium → your brand → connect).
5. AI B-roll is fallback-only and art-directed to the palette.
6. Every graphic has a stated job (§07).
7. Every animation maps to meaning (rack focus = lens, playhead = create, iris = deliverable, join = connect).
8. A restrained, precise studio look.
9. Executable in AE, or in CapCut with the noted approximations.
10. Without the reference, it still stands as "a video studio showing its craft."
