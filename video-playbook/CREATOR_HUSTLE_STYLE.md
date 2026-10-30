# Talking-Head Motion Style ("Creator Hustle" look)

Learned from one reference: an 8:25 English (Indian creator) YouTube video,
"6 lazy ways to make money in 2026". The format is a talking head in a home
studio, edited jump-cut tight, with a red/black motion-graphics layer on top.
Reference frames are in `reference/creator-hustle/`.

This is a **different format** from the other two playbooks: landscape,
long-form, and built on a person on camera rather than narrated stills or 3D.

---

## 1. Measured numbers

| Spec | Value | How measured |
|---|---|---|
| Aspect / size | 2:1 landscape, 1280×640 (shoot 4K 16:9, crop) | ffprobe |
| Frame rate | 25 fps | ffprobe |
| Length | 8:25 | ffprobe |
| Speech pace | **~221 words/min**, very fast | whisper word timings |
| Silences | only 4 gaps > 1 s in 8 min | word gaps |
| Visual changes | **218 cuts, one every ~2.3 s** | ffmpeg scene detect |
| Loudness | **-10.3 LUFS integrated** (loud; YouTube turns it down to -14) | ebur128 |
| Voice vs music | voice ~**21 dB above** the music bed while talking | demucs stems |
| SFX | ~20 audible hits/min on the music+SFX stem | onset detection |

**Golden rule: the face is the base layer, and something changes every 2–3 s.**
That might be a zoom, a cut, a word, an icon, or a B-roll insert.

---

## 2. The edit (the base layer)

1. **Jump cuts on every breath and filler.** Remove all "umm" sounds and pauses so
   sentences butt up against each other. That's where the 221 wpm comes from.
2. **Alternate the framing on every cut:** wide (≈100%, desk and Batman
   wall art visible) → punch-in (≈120–135%, chest-up) → wide. Each
   punch-in hides a jump cut and adds energy.
3. **The set does the branding:** warm practical light, dark room, the same
   props every video. The background is graded slightly warm/teal, and skin is kept natural.
4. **Hand gestures are cues.** When he raises 5 fingers, "5" appears, and icons
   appear where his hands point.

## 3. The motion-graphics toolkit (what to learn, in order of frequency)

| # | Effect | Where | How it's built |
|---|---|---|---|
| 1 | **Word-by-word captions** | Most lines | White heavy sans (Inter/SF Pro Display Bold-Black, tight tracking), **1–2 words at a time**, lower centre, soft shadow, no box. Pops in at 90→100% scale. |
| 2 | **Text behind the head** | Hook and key claims (`5 YEARS AGO`, `2026`, `WHAT SKILLS`, `JUST TYPING`, `1 LAKH`) | Huge condensed font (Anton/Bebas) across the frame, **layered behind the person** using a person matte (rotobrush / "remove background" / segmentation). Variants: **chrome/iridescent** fill, **solid white with motion blur**, **blurred white**. Letters slide or blur in. |
| 3 | **Two-size caption** | Questions | Small lowercase sans top-left (`how are they`), then a huge condensed word fills the line (`DOING IT`). |
| 4 | **Icon pops beside the head** | Lists, tools, comparisons | Glassy rounded-square app icons (Framer, Webflow, WhatsApp, briefcase, megaphone) or **glowing white orbs** that turn red for "selected". Labels are in a **handwritten marker font** (Permanent Marker style) with a little hand-drawn curved arrow. Scale pops 0→110→100%. |
| 5 | **Recurring master table** | Opens each of the 6 items | One red-glow HUD table (`OPPORTUNITY / SKILLS REQUIRED / TIPS TO GET CLIENTS / HOW MUCH MONEY`) on black. Rows that haven't been covered yet are **blurred**. Each time it returns, a highlight bar **sweeps down to the next row**, the camera **pushes into that cell**, and the bullets type in. That gives the video one progress map the viewer comes back to. |
| 6 | **Chapter card: old book** | Before each item | An aged book on a red table with a candle and scattered cards. The page turns to reveal the item number + title (`3 / VIDEO EDITING / Short Form`), with a music swell + boom. |
| 7 | **Cinematic B-roll + big numbers** | Money and time claims | Stock/AI B-roll graded **deep red / crushed blacks** (city rooftop at night, a silhouette at a desk). Huge chrome or translucent numbers **count up** (`20% → 40%`) or slide across (`₹200,000 /month`), with a small marker-font annotation. |
| 8 | **Dark-grey diagram scenes** | Explaining a system | Vignetted charcoal background, **white glowing line icons** (people grids, pyramid, flowcharts, folder with app icon dropping in), with red as the only accent. Elements build one at a time. |
| 9 | **Red grid charts** | Comparisons | Red background + faint grid, white bars with avatar circles on top (typing speed: 40 vs 80 vs 140 wpm). |
| 10 | **Screen / UI inserts** | Proof, sponsor | Real screenshots (YouTube page, DMs on a phone on a red desk, app UI) in **CRT/scanline treatment** or as floating white cards. |
| 11 | **Borrowed clips** | Authority | Short clips of other creators with a name lower-third (`Iman Gadzhi`, `ALEX / LEILA`). |

### Transitions
- **Hard cut** (default, ~85%).
- **White flash** for 2–3 frames into big reveals.
- **Grey VHS static** for 3–6 frames into archival/borrowed clips.
- **RGB glitch** (magenta/cyan split) into screenshots.
- **Blur-zoom** into the table cell or chapter card.

### Colour system
| Role | Colour |
|---|---|
| Accent / brand | Blood red `#D0101A` → glow `#FF2A2A` |
| Backgrounds | Black `#0B0B0B`, charcoal `#2A2A2A` vignette |
| Text | White `#FFFFFF`; chrome gradient for hero words |
| Highlight (rare) | Neon yellow-green `#E6FF6A` for money (`$1,000,000`, `30K /MONTH`) |

## 4. Sound design (from stem separation)

- **The music bed is barely there under speech:** about -33 dB, ~21 dB below the
  voice. It's a low, steady, modern beat (lo-fi/hip-hop/trap, 100–140 BPM),
  and the track changes between sections.
- **Music jumps to full volume only on set pieces:** the intro title sequence
  (0:30–0:40), the chapter-book cards (e.g. 3:30, 5:45), and the outro
  (8:15). These are the only moments the bed rises to near voice level.
- **SFX palette** (heaviest first, from onset classification):

| Hits found | Sound | Put it on |
|---|---|---|
| 67 | **Boom / sub impact** with a tail | Text-behind-head slams, chapter number, big numbers |
| 33 | **Short thud / kick** | Icon pops, table row highlight, punch-in zooms |
| 41 | **Mid swoosh / pop / ding** | Captions entering, cards sliding, UI pops |
| 12 | **Shimmer / riser / glitch** | Into chapter cards, glitch transitions, the money reveal |
| 11 | **Whoosh** that rises into the hit | Slide-ins, whip moves, B-roll entries |

  Only ~12% of cuts get an SFX. Jump cuts stay silent; **SFX mark graphics,
  not edits**.
- **Mix:** a voice that's heavily compressed and bright, finished at roughly -10 LUFS. SFX sit
  just under the voice and never land on top of a key word.

> Caveat: SFX that demucs left in the vocal stem weren't counted, so the
> real SFX density is higher than 20/min.

## 5. Script structure

```
0:00–0:35  HOOK      "5 years ago my parents would never have believed…" +
                     big claim (₹2 lakh/month without a degree) + 3 questions
                     ("How are they doing it? What skills do they have that
                     you don't? How can you get started?")
0:35–0:40  TITLE     Book/title sequence with full music.
0:40–1:03  WHY TRUST "I make these every few months…" + flatter the audience.
1:03       "Let's start."
1:04–8:00  LIST ×6   Each item: chapter book → master table row → what it is
                     → real example → skills needed → how to get clients →
                     money range. The sponsor read sits inside an item.
8:00–8:25  OUTRO     Full table recap → emotional push ("prove them all
                     wrong") → black end card with a 4-line manifesto.
```

Verbal tics worth stealing: direct address ("you guys"), one swear for
emphasis, numbers in rupees/lakhs, and the "not X, but Y" correction
("Not a one-time digital product, but a proper business").

## 6. How to make it

### In HyperFrames (this repo)
| Effect | Skill / tool |
|---|---|
| Person matte for text-behind-head | `/media-use` remove-background (run on the footage) → stack: footage, text, matted person |
| Word-by-word captions | `/media-use` transcription → `hyperframes-core` caption track |
| Punch-ins, cell push-ins, blur-zoom | `/hyperframes-keyframes` |
| Pops, slides, counters, row sweep | `/hyperframes-animation` (GSAP `back.out(1.7)` for pops, `expo.out` for slides) |
| Glitch / VHS / CRT / white flash | `/hyperframes-registry` (search "glitch", "crt", "flash") |
| Booms, whooshes, music ducking | `/media-use resolve --type sfx`, `/hyperframes-audio` for ducking and the -10 LUFS target |

### In a manual editor (Premiere / After Effects / CapCut / DaVinci)
1. Rough cut: remove silences (Premiere *Text-Based Editing* / CapCut *Remove
   pauses* / AutoCut). Alternate 100% and 125% scale on each cut.
2. Captions: auto-transcribe, set the max to 2 words per line, Inter Black, add a pop-in preset.
3. Text behind head: duplicate the clip on top, use **Roto Brush (AE)** / **Magic Mask
   (DaVinci)** / **Remove background (CapCut)** on the top copy, and put the text between the two layers.
4. Chrome text: a gradient map or chrome texture clipped to the text, plus a bevel and drop shadow.
5. Build the master table, chapter book, and icon pops **once** as templates
   (MOGRTs / CapCut templates), then reuse them every video.
6. SFX: one boom per graphic slam, a thud per icon, and a whoosh per slide. Keep the music
   at -30 dB under speech, and ride it up on chapter cards.

### Checklist before export
- [ ] Nothing on screen stays the same for more than 3 s
- [ ] Every number is a graphic (counter, chrome, or table)
- [ ] Every list item opens with the chapter card + master table
- [ ] Hook has at least 2 text-behind-head moments
- [ ] Red/black/white only, with yellow-green for money
- [ ] Music audible only between lines, full only on set pieces
