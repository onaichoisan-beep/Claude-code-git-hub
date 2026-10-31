# Serum X: "Glow In My Own Shade", Google Flow prompt pack

Everything you need to make the video from `SCRIPT.md` in **Google Flow**
(Veo video plus Nano Banana / Imagen images), shot by shot, with the
characters kept consistent.

Total ≈ 95 s · 9:16 vertical · 21 Flow clips + 1 end card.

---

## 0. How to work in Flow (read once)

1. **Make the song first** (§6, Suno/Udio). Flow can't make a song with your
   lyrics. The song is the clock: every clip below has a song time.
2. **Make the "ingredients" (§2) as images first** and save them. You'll
   attach them to every clip, and they are what keeps Anaya the same girl
   with the same skin tone in all 21 clips.
3. For each clip in §4, open Flow → **Ingredients to Video** (attach the
   listed ingredient images) → paste the **STYLE BLOCK** (§1) and then the clip
   prompt → aspect **9:16** → generate 2–4 takes and keep the best one.
   - Clips that continue the previous shot say **"Frames to Video"**: use the
     last frame of the previous clip as the start frame.
4. Flow clips are **8 s**. Each clip lists **"Use: x–y s"**, the part to keep.
   Trim in CapCut/Premiere and place it at the given **song time**.
5. **Audio from Flow: off/muted.** The song carries all the sound. Every
   prompt ends with "no dialogue, no music" so Veo doesn't add lip-sync or a
   score.
6. **No text in generated shots.** Veo garbles words. Add captions,
   ingredient names and the end card in the editor (§5). The bottle's label
   is simple shapes; put your real label on in the editor if needed.
7. **Inside one clip**, the timestamps `[0–2s]`, `[2–4s]` describe a
   continuous move. If Veo ignores a timed cut, generate each timed beat as
   its own clip with the same ingredients.

---

## 1. STYLE BLOCK (paste at the start of every video prompt)

```
Stylized photoreal 3D animation, Pixar-meets-realistic, soft subsurface skin,
expressive eyes, detailed hair strands, vertical 9:16, cinematic 35mm lens,
shallow depth of field, warm golden-hour palette (amber, honey, terracotta,
soft teal shadows), gentle film grain, slow smooth camera movement.
Indian college setting. Consistent characters from the reference images.
Anaya always has the SAME deep brown skin tone as her reference, never lighter.
No text, no captions, no logos, no watermarks. No dialogue, no music.
```

---

## 2. Ingredients: generate these images first (Flow → image, 9:16 or 1:1)

Make each one, pick the best, and keep the file names. Generate the **Anaya
AFTER** image by attaching **Anaya BEFORE** as a reference so the face matches.

**I-1 · Anaya BEFORE (character sheet)**
```
Character reference sheet, stylized photoreal 3D Pixar-like, full body front
view and close-up face, 19-year-old Indian college girl named Anaya, deep brown
skin tone, oval face, large expressive dark-brown eyes, thick natural eyebrows,
small nose stud on left nostril, long dark curly hair worn loose over her face,
oversized grey hoodie with hood up, faded blue jeans, white canvas sneakers,
black backpack. Skin looks dull and tired with uneven patches and two small
breakouts on the cheek, slumped shoulders, shy expression. Plain warm-grey
studio background, soft even light. No text.
```

**I-2 · Anaya AFTER (same girl): attach I-1 as reference**
```
The exact same girl from the reference image, same face, same deep brown skin
tone (do not lighten), same nose stud. Now her skin is smooth, even, healthy
and dewy with a natural glow, hair tied back in a high curly ponytail, mustard
yellow kurta-top, light denim jacket, same jeans and sneakers, upright
confident posture, warm smile. Character reference sheet, full body + face
close-up, plain warm-grey studio background. No text.
```

**I-3 · Meera Didi (mentor)**
```
Character reference sheet, stylized photoreal 3D Pixar-like, 26-year-old Indian
woman Meera, Anaya's older cousin, medium-brown skin, short wavy bob haircut,
round gold-rim glasses, small gold hoop earrings, olive-green oversized shirt
over white tee, warm teasing smile, confident big-sister energy. Full body +
face close-up, plain warm-grey studio background. No text.
```

**I-4 · Classmates (same 4 in every class scene)**
```
Group character reference, stylized photoreal 3D Pixar-like, four Indian
college students aged 19, standing in a row: Rohan (tall boy, light-brown
skin, curly hair, maroon t-shirt), Priya (girl, wheatish skin, straight bob,
pink top), Kabir (boy, dark skin, buzz cut, round glasses, navy hoodie),
Zoya (girl, medium-brown skin, braids, white shirt). Friendly expressions.
Plain warm-grey background. No text.
```

**I-5 · Serum X bottle (product)**
```
Product shot, 30ml frosted amber glass serum bottle with a gold dropper cap,
a simple white label with a single bold gold "X" shape, no other writing,
standing on a warm beige stone surface, soft golden backlight, glossy
reflections, photoreal 3D render, vertical 9:16. No other text.
```

**I-6 · Locations (one image each, no people)**
```
L-A Classroom: Indian college classroom, wooden benches in rows, green
chalkboard, ceiling fans, tall windows with warm afternoon sun beams, wall
clock, stylized photoreal 3D, empty, vertical 9:16, no text.

L-B Washroom mirror: college washroom, large rectangular mirror with a thin
brass frame, white tiles, a small frosted window on the left with soft
daylight, stylized photoreal 3D, empty, vertical 9:16, no text.

L-C Anaya's bedroom: cozy small Indian bedroom, fairy lights, study desk with
books, round wall mirror, marigold-orange curtains, evening lamp light,
stylized photoreal 3D, empty, vertical 9:16, no text.

L-D College corridor: open-air college corridor with arches and pillars,
terracotta floor, notice board, golden morning sun streaming through arches,
stylized photoreal 3D, empty, vertical 9:16, no text.
```

**Consistency rules (keep repeating them)**
- Always attach **I-1 or I-2** for Anaya, **I-3** for Didi, **I-4** for classmates,
  **I-5** for the bottle, and the matching **L-** location.
- Always repeat her **identity line**: *"Anaya: deep brown skin (same as
  reference, never lighter), large dark-brown eyes, nose stud, long curly
  hair"*.
- BEFORE outfit = grey hoodie. AFTER outfit = mustard top + denim jacket.
  Never mix them.
- Same camera side for before/after pairs (noted as **CALLBACK**).

---

## 3. Song map (the timing every clip follows)

| Song time | Section | Clips |
|---|---|---|
| 0:00–0:18 | Verse 1, the low point | C01–C05 |
| 0:18–0:28 | Hook 1 | C06–C07 |
| 0:28–0:56 | Verse 2, mentor + serum | C08–C14 |
| 0:56–1:06 | Hook 2 | C15–C16 |
| 1:06–1:25 | Verse 3, the glow-up | C17–C20 |
| 1:25–1:35 | Outro + end card | C21 + END |

---

## 4. Clip prompts (paste the STYLE BLOCK first, then the prompt)

### VERSE 1: the low point

**C01 · 0:00–0:04.4 · "I used to sit at the back of the class / Hoodie up, hair down…"**
Ingredients: I-1, I-4, L-A · Use: 0–4.4 s
```
[0–2.2s] Wide shot from the front of the classroom, slow push-in toward the
last row: Anaya (deep brown skin, same as reference, never lighter, grey
hoodie, hood up, long curly hair over her face) sits alone on the last bench
by the window; the four classmates chat happily in the front rows with their
backs to her. Dusty sun beams.
[2.2–4.4s] Medium close-up on Anaya: she tugs her hood lower with one hand and
glances up at the wall clock, a small sigh, eyes heavy.
Mood: lonely, muted warm light, she sits in shadow while others are in sun.
```

**C02 · 0:04.4–0:07 · "Skin felt dull and patchy, couldn't face the light"**
Ingredients: I-1, L-B · Use: 0–2.6 s
```
Over-the-shoulder shot into the washroom mirror. Anaya (deep brown skin, never
lighter, grey hoodie) looks at her reflection: dull, tired skin with uneven
patches and two small breakouts. Daylight from the small window falls on her
face; she flinches and turns her face away from the light, pulling hair
across her cheek. Slow push-in on the reflection. Soft, slightly desaturated
light.
```

**C03 · 0:07–0:09 · "Camera came around, I'd step out of sight"**
Ingredients: I-1, I-4, L-D · Use: 0–2.2 s
```
In the sunny college corridor the four classmates squeeze together for a
group selfie, Priya holding the phone up high. Anaya (grey hoodie, deep brown
skin) was standing at the edge; as the phone rises she quietly slides
sideways out of the frame and walks away behind a pillar. Camera at selfie
angle, slight handheld drift.
```

**C04 · 0:09–0:13.2 · "Group project names, mine was never said / Raised my hand, they looked right past instead"**
Ingredients: I-1, I-4, L-A · Use: 0–4.2 s
```
[0–2.1s] Classroom. A kind middle-aged Indian male professor in a beige
sweater-vest reads from a clipboard; students stand up and pair off with
smiles. Anaya (grey hoodie) stands up hopefully, then is left alone standing
as everyone pairs up; she slowly sits back down.
[2.1–4.2s] Anaya half-raises her hand from the back row; the professor's eyes
pass right over her and he points to Rohan in the front. Her hand slowly
lowers. Camera behind her shoulder, the class out of focus ahead.
```

**C05 · 0:13.2–0:18 · "Mirror in the washroom, I'd just look away / Told myself 'tomorrow,' every single day"**
Ingredients: I-1, L-B, L-C · Use: 0–4.8 s
```
[0–2.4s] Washroom mirror, close-up of Anaya's reflection (deep brown skin,
never lighter, dull skin, grey hoodie); she meets her own eyes, then drops
her gaze to the sink.
[2.4–4.8s] Quick time-lapse montage in her bedroom: a wall calendar's pages
flip by, the same grey hoodie is pulled on each morning, the light outside
the window cycles day to night. Melancholy, muted.
```

### HOOK 1

**C06 · 0:18–0:23 · "Glow in my own shade, yeah / Glow in my own shade"**
Ingredients: I-1, L-D · Use: 0–5 s
```
[0–2.5s] Empty college corridor at sunrise, a sheet of golden light slowly
sweeps across the terracotta floor and the arches, dust motes glittering.
[2.5–5s] Anaya's silhouette (grey hoodie, hood down for the first time, curly
hair) standing at an arched window, the sun rising behind her, a warm rim
light outlining her curls. Slow push-in. Hopeful, cinematic.
```

**C07 · 0:23–0:28 · "Glow in my own shade, yeah / Glow in my own shade"**
Ingredients: I-5, L-C · Use: 0–5 s
```
[0–2.5s] Bedroom round mirror, a soft lens-flare of golden light glides across
its surface, fairy lights twinkling, out-of-focus.
[2.5–5s] Extreme macro: a glass dropper above the frosted amber bottle (I-5),
one golden drop forms and hangs, catching the light, slow motion. Do not show
the label clearly yet.
```

### VERSE 2: the mentor and the serum

**C08 · 0:28–0:32.4 · "So I called Meera Didi, she just laughed and said / 'Your shade's not the problem…'"**
Ingredients: I-1, I-3, L-C · Use: 0–4.4 s
```
[0–2.2s] Anaya on her bed in her grey hoodie, phone in hand on a video call;
over her shoulder we see Meera Didi (short wavy bob, gold-rim glasses, olive
shirt) on the phone screen, laughing warmly.
[2.2–4.4s] Meera now standing in Anaya's bedroom doorway, walks in and puts a
hand on Anaya's shoulder; both look into the round wall mirror together, Didi
smiling and pointing at Anaya's reflection reassuringly. Anaya: deep brown
skin, never lighter.
```

**C09 · 0:32.4–0:37 · "'Sun and stress and late nights stealing all your shine / Fix the barrier first…'"**
Ingredients: none (cut-away) · Use: 0–4.6 s
```
3D medical visualization, macro cross-section of human skin layers with a deep
brown epidermis, warm amber background bokeh.
[0–2.3s] Thin orange UV rays and grey smoky stress particles hit the skin
surface; the top layer looks cracked and dry like a broken brick wall.
[2.3–4.6s] The cracked bricks of the skin barrier slide back into place one by
one and seal up, a soft golden glow spreads across the surface. Clean, no
labels, no text.
```

**C10 · 0:37–0:41 · "Tried every hack online, lemon, scrubs and more / Left my face more red than it was before"**
Ingredients: I-1, L-C · Use: 0–4 s
```
[0–2s] Fast top-down shot of her desk: cut lemon halves, a gritty walnut scrub
jar, a bowl of DIY paste, a phone with an unreadable social feed; Anaya's
hands rubbing lemon onto a cotton pad.
[2–4s] Close-up in the bedroom mirror: Anaya (deep brown skin, never lighter)
touches her cheeks, which look irritated and reddish, and winces, frustrated.
```

**C11 · 0:41–0:44 · "Then she put a bottle in my hand, she said 'X'"**
Ingredients: I-1, I-3, I-5, L-C · Use: 0–3 s
```
Close-up on hands: Meera Didi places the frosted amber serum bottle with gold
dropper (I-5) into Anaya's open palm, slow motion; a golden glint runs across
the glass. Slow tilt up to Anaya's surprised face and Didi winking behind her.
```

**C12 · 0:44–0:51 · "Niacinamide for the patches… / Vitamin C for the dullness… / Hyaluronic keeps it plump…"**
Ingredients: none (cut-away) · Use: 0–7 s (3 beats)
```
3D macro cross-section of deep brown skin, warm bokeh background, no text.
[0–2.3s] Tiny amber particles drift down into the skin and spread out; uneven
darker patches on the surface blend into an even, smooth tone.
[2.3–4.6s] Bright golden particles light up the surface cells from inside; the
skin surface starts to reflect light with a healthy sheen.
[4.6–7s] Clear water droplets sink in and the skin cells swell plump and
bouncy, the surface becomes dewy and glossy.
```
*(Editor: put the ingredient names on top: NIACINAMIDE / VITAMIN C /
HYALURONIC ACID.)*

**C13 · 0:51–0:53.4 · "'Same rich shade, just healthy, that's the flex'"**
Ingredients: I-1, I-2 · Use: 0–2.4 s
```
Split-screen vertical frame, the same cheek close-up of Anaya on both sides:
left half dull and patchy, right half smooth, dewy and glowing. Exactly the
SAME deep brown skin tone on both sides, only the texture and radiance
differ. A soft light sweep moves left to right.
```

**C14 · 0:53.4–0:56 · "'Two drops at night, sunscreen every day, that's X'"**
Ingredients: I-1, I-5, L-C · Use: 0–2.6 s
```
[0–1.3s] Night, bedroom lamp light: Anaya presses two drops of serum from the
dropper onto her fingertips and pats them onto her cheeks.
[1.3–2.6s] Morning, sunlight at the window: she squeezes sunscreen onto her
fingers and smooths it on, smiling slightly. Deep brown skin, never lighter.
```

### HOOK 2: the turn

**C15 · 0:56–1:01 · "Glow in my own shade, yeah / Glow in my own shade"**
Ingredients: I-2, L-C · Use: 0–5 s
```
[0–2.5s] Anaya (AFTER look: mustard top, denim jacket, deep brown skin same as
reference, never lighter) steps out of her house door into bright morning
sun, hood-less, takes a deep breath. Low-angle camera, slow push-in.
[2.5–5s] In her round bedroom mirror she ties her curly hair into a high
ponytail and gives herself a small, growing smile.
```

**C16 · 1:01–1:06 · "Glow in my own shade, yeah / Glow in my own shade"**
Ingredients: I-2, L-D · Use: 0–5 s
```
[0–2.5s] Anaya (AFTER look) walks confidently through the college gate toward
camera, golden sunlight on her face, hair bouncing, tracking shot backward.
[2.5–5s] Extreme close-up of her face: smooth, dewy, glowing skin, SAME deep
brown tone as the reference, soft golden rim light, she looks up into the
light and smiles.
```

### VERSE 3: the glow-up

**C17 · 1:06–1:10 · "Two weeks in, my skin felt soft and new / One month deep, the dullness faded too"**
Ingredients: I-2, L-C · Use: 0–4.4 s
```
[0–2.2s] Close-up: Anaya's fingertips gently touch her cheek, she smiles at
how soft it feels; a wall calendar behind her is circled in red.
[2.2–4.4s] Round bedroom mirror: her reflection with clearly calmer, even,
glowing skin (same deep brown tone, never lighter); she grins and does a tiny
happy shoulder shimmy.
```

**C18 · 1:10–1:15 · "Hoodie off, I'm sitting in the front row now / Raised my hand, the whole class turned around"**  CALLBACK to C01 + C04
Ingredients: I-2, I-4, L-A · Use: 0–5 s
```
Same classroom and same camera angle as the opening shot (from the front).
[0–2.5s] Anaya (AFTER look) now sits in the FRONT row by the window, in the
sunbeam, confidently opening her notebook.
[2.5–5s] She raises her hand high; the same professor smiles and points at
her; the four classmates turn around in their seats and smile at her.
```

**C19 · 1:15–1:20 · "Presentation day, yeah, I owned that stage / Camera came around, I'm the first face in the frame"**  CALLBACK to C03
Ingredients: I-2, I-4, L-A, L-D · Use: 0–5 s
```
[0–2.5s] Anaya (AFTER look) presents at the front of the classroom next to the
chalkboard, gesturing confidently; the class claps, Rohan and Zoya cheering.
[2.5–5s] The same sunny corridor as before: the same group selfie, but now
Anaya is in the CENTER, Priya and Zoya hugging her from both sides, everyone
laughing into the raised phone.
```

**C20 · 1:20–1:25 · "Same deep shade, just glowing from within / Serum X, yeah, that's my win"**
Ingredients: I-2, I-3, I-5, L-D · Use: 0–5 s
```
[0–2.5s] Hero close-up at golden hour: Anaya (AFTER look) turns her face toward
camera, skin glowing, EXACT same deep brown tone as reference, confident
look straight into the lens. Slow push-in.
[2.5–5s] She lifts the frosted amber Serum X bottle (I-5) up next to her
cheek, smiling; Meera Didi in the soft background gives a wink and a thumbs
up.
```

### OUTRO

**C21 · 1:25–1:30 · "50,000 girls already glowing in their shade / 30-day glow promise, try it…"**
Ingredients: I-2, I-5, L-D · Use: 0–5 s
```
[0–2.5s] Wide shot outside the college gate: a joyful crowd of young Indian
women with a wide range of skin tones from fair to very deep, all laughing
and walking together in golden sunlight; Anaya in the middle.
[2.5–5s] Close-up toward camera: Anaya drops two golden drops of serum onto the
back of her hand and holds it out to the viewer, smiling.
```

**END · 1:30–1:35 · end card (build in the editor, not Flow)**
Optional Flow packshot, Ingredients: I-5 · Use: 0–5 s
```
The frosted amber serum bottle (I-5) slowly rotating on a round glowing
pedestal, deep plum-to-warm-gold gradient background, soft floating light
specks, product hero lighting, centered with empty space above and below for
text. No text.
```

---

## 5. Editor layer (CapCut / Premiere)

- **Captions:** each lyric line in ALL CAPS, white, Montserrat ExtraBold,
  dark 4 px outline + soft shadow, 2 lines max, centred at ~73% of frame
  height. Change it on each line, timed to the song (CapCut "Auto lyrics",
  then fix the words).
- **Ingredient labels (C12):** thin gold serif name (e.g. Playfair Display)
  plus a small grey benefit line under it; fade in over 0.3 s, top third.
- **C13 label:** "SAME SHADE. MORE GLOW."
- **End card text:** "GLOW IN YOUR OWN SHADE" (white, bold) above the bottle;
  a gold pill button "Tap Shop Now" under it.
- **Grade:** slight warm tone across all clips so they match; same LUT on every clip.
- **Mix:** the song only, mastered to −14 LUFS.
- **Cuts:** hard cuts on each lyric line; no fancy transitions.

---

## 6. Song prompt (Suno / Udio)

Style:
```
Feel-good R&B pop, 95 BPM, F minor verses lifting to A-flat major hook,
young female vocalist, melodic half-rap verses, big catchy sung hook,
warm Rhodes piano, finger snaps, soft 808 bass, confident uplifting
```
Lyrics (paste into "custom lyrics"):
```
[Verse 1]
I used to sit at the back of the class
Hoodie up, hair down, hoping time would pass
Skin felt dull and patchy, couldn't face the light
Camera came around, I'd step out of sight
Group project names, mine was never said
Raised my hand, they looked right past instead
Mirror in the washroom, I'd just look away
Told myself "tomorrow," every single day

[Hook]
Glow in my own shade, yeah
Glow in my own shade
Glow in my own shade, yeah
Glow in my own shade

[Verse 2]
So I called Meera Didi, she just laughed and said
"Your shade's not the problem, it's what your skin's been fed
Sun and stress and late nights stealing all your shine
Fix the barrier first, the glow comes in time"
Tried every hack online, lemon, scrubs and more
Left my face more red than it was before
Then she put a bottle in my hand, she said "X"
"Niacinamide for the patches, calm the rest
Vitamin C for the dullness, bring the light
Hyaluronic keeps it plump both day and night
Same rich shade, just healthy, that's the flex
Two drops at night, sunscreen every day, that's X"

[Hook]
Glow in my own shade, yeah
Glow in my own shade
Glow in my own shade, yeah
Glow in my own shade

[Verse 3]
Two weeks in, my skin felt soft and new
One month deep, the dullness faded too
Hoodie off, I'm sitting in the front row now
Raised my hand, the whole class turned around
Presentation day, yeah, I owned that stage
Camera came around, I'm the first face in the frame
Same deep shade, just glowing from within
Serum X, yeah, that's my win

[Outro]
Fifty thousand girls already glowing in their shade
Thirty-day glow promise, try it, that's the way
Glow in my own shade
```
The generated song won't match the times in §3 exactly. After you have it,
note each line's real start time and shift the clips to match. Every "Use"
range has spare seconds for this.

---

## 7. Fixes when a clip goes wrong

| Problem | Fix |
|---|---|
| Anaya's skin looks lighter | Re-attach I-1/I-2; add "skin tone exactly matches reference image, deep brown, do not lighten" at the start of the prompt |
| Face changes between clips | Use **Frames to Video** with a frame from the previous good clip as the start frame |
| Wrong outfit | Name it explicitly: "grey hoodie (BEFORE)" or "mustard top + denim jacket (AFTER)" |
| Gibberish text on screen | Add "no text, no letters, no signs" and keep the chalkboard/phone out of focus |
| Veo adds talking / music | Mute the clip; add "characters do not speak, silent ambience" |
| Too much motion | Add "subtle movement, locked-off camera with a slow push-in" |

Placeholder claims (50,000 girls, 30-day promise, ingredient benefits)
must be replaced with the brand's real, provable figures before publishing.
