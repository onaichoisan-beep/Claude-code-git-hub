# Song-Narrated Story Ad Style ("Barbershop Hip-Hop" look)

Learned from one reference: a 96 s vertical ad for a hair-growth gummy
("Lumin"). The whole video is a **rap/R&B song**: the lyrics tell the story and
also deliver the product pitch. No spoken voice-over.
Frames: `reference/song-ad/`.

## 1. Technical format

| Spec | Value |
|------|-------|
| Aspect / resolution | 9:16, 720×1280, 30 fps, H.264 + AAC 44.1 kHz stereo |
| Length | 1:37 (96.8 s) |
| Loudness | −17.4 LUFS integrated, LRA 2.8 LU (very compressed, flat) |
| Silence | None until the last 0.75 s. Music starts on frame 1. |
| Tempo / key | ~92 BPM, D♯/E♭ minor (laid-back boom-bap / R&B groove) |
| Shot length | 47 cuts, so a new shot every ~2.0 s (range 0.7–3.6 s) |
| Lyric density | One caption line every ~2.2 s (about one bar at 92 BPM) |

## 2. Story structure (problem → mentor → mechanism → transformation → CTA)

| Time | Section | What happens | Lyric example |
|------|---------|--------------|---------------|
| 0:00–0:20 | **Verse 1: the pain** | Mirror check, thinning crown, women walk past, hides under a hat at the barbershop, alone at a club | "I started checking the mirror every morning / crown getting thin and that ain't the view I knew" |
| 0:20–0:30 | **Hook** | Walks past barbershops, empty barber station, mirror | "Waves back, that's the move" (×2) |
| 0:30–0:48 | **Verse 2: the mentor** | Older barber "Eddie" (trusted elder, calls him "nephew") explains the problem; 3D medical cut-aways; "I tried everything" montage (pill bottles, minoxidil dropper) | "So I went to Eddie my barber, right / and Eddie told me something real" |
| 0:48–1:02 | **Verse 2b: the mechanism** | Barber holds the product; each ingredient gets its own glowing 3D follicle shot | "Biotin-silica, 40 times more absorption / saw palmetto blocking DHT" |
| 1:02–1:12 | **Hook** | Same "waves back" visuals as the first hook | "Waves back, that's the move" |
| 1:12–1:30 | **Verse 3: the results timeline** | Baby hairs in the mirror, barber notices, women look again, partner touches his hair, confident close-up | "Six weeks in, baby hairs at the edge / three months deep, barber see the change" |
| 1:30–1:37 | **Social proof + offer + end card** | Crowd of men outside "The Community Barbershop"; holds the pack; red end card | "50,000 brothers already know / 90-day guarantee, that's the flow" |

Rules it follows:
- **Starts mid-feeling on frame 1** ("I started checking the mirror…"). No logo or intro.
- **Before/after mirrors itself:** each verse-1 scene comes back fixed in verse 3
  (street walk ignored → street walk noticed; hat at the barber → fresh cut at
  the barber; mirror worry → mirror smile). Same locations, same outfit, new
  mood.
- **Trusted messenger, not the brand,** explains the science (barber/uncle
  figure, "Nephew", "Eddie said"). The brand name is sung only once, at 1:25.
- **Hook = the desired outcome** in 4 words ("Waves back, that's the move"),
  repeated 4–5 times so it gets stuck in the viewer's head.
- **Timeline payoff:** concrete milestones (6 weeks → 3 months).
- **Ends with numbers:** social proof (50,000) + risk reversal (90-day
  guarantee) + CTA card.

## 3. Lyrics / script style

- First person, conversational AAVE / hip-hop slang aimed at the audience:
  *crown, waves, fade, shawties, nephew, that's facts, had me shook, that's the
  move, that's the flow*.
- Rhyme on line endings: knew/view, real/need, change/again, win/back/facts,
  know/flow.
- Each line holds **one idea in about 6–10 words**, which fits one 2-second caption.
- Feature claims are squeezed into rhythm: "[ingredient] + [benefit]" per bar.
- Ad-libs and asides ("You know what I'm saying", "So, yeah", "right") make it
  feel like a real song, not a jingle.

Full transcript (auto-transcribed; the brand and ingredient spellings are
corrected from the captions):

```
I started checking the mirror every morning
You know what I'm saying, crown getting thin
And that ain't the view I knew
Used to walk down the street, shawties grabbing on my fade
Now they walkin' past me like I'm yesterday's fade
Can't even take my hat off at the barbershop
Nephew, lost my crown, that's too much
Used to turn 'em down all day
Now I can't get a touch, that's the pain, that's real
Waves back, that's the move
Waves back, that's the move
So, yeah
So I went to Eddie, my barber, right
And Eddie told me something real
He said biotin dissolving in your stomach
That's the problem, 82% deficient
In what your follicles need
Your melanin blocking the sun
Nephew, I tried everything
Two years of nothing, minoxidil had me shook
Side effects all crazy
But Eddie said Lumin different though
Biotin-silica, 40 times more absorption
Saw palmetto blocking DHT
Where it counts, vitamin D dosed for us
Rosemary matching minoxidil results
No prescription, no side effects
Two gummies a day, nephew
That's it
Waves back, that's the move
Waves back, that's the move
Six weeks in, baby hairs at the edge
Three months deep, barber see the change
That's when the shawties started looking again
Hand in my waves, yeah, that's the win
Crown restored, confidence back
Lumin brought it, nephew, that's facts
50,000 brothers already know
90-day guarantee, that's the flow
```

## 4. Voice & music

- **One male vocalist** who half-raps the verses (melodic flow, relaxed, not
  aggressive) and sings the hook. No separate narrator.
- **Beat:** ~92 BPM, minor key, warm R&B / boom-bap. Soft kick + snare,
  sub bass, mellow keys or guitar. Feels "smooth confidence", not hype trap.
- The vocal sits on top; the beat never drops out. The mix is heavily limited
  (only 2.8 LU of loudness range), so it sounds like a finished radio song.
  Master louder (−14 LUFS) for Reels/Shorts.
- **No SFX:** the song carries everything.
- Getting this sound: AI music generators (Suno, Udio, ElevenLabs Music) with
  your own lyrics. Prompt sketch:
  > "Smooth R&B hip-hop, 92 BPM, E♭ minor, male vocalist, melodic rap verses,
  > catchy sung hook, warm Rhodes keys, boom-bap drums, deep bass, confident
  > feel-good storytelling"
  Put section tags in the lyrics (`[Verse 1]`, `[Hook]`, `[Verse 2]`,
  `[Outro]`) and keep each line short so it fits one caption.

## 5. Visual style

- **Stylised photoreal 3D (Pixar-meets-realistic):** big expressive eyes, soft
  skin, detailed hair. Same lead character in every shot (grey tee / black
  bomber jacket / white sneakers) so the viewer follows one person.
- **Warm golden-hour palette:** amber, brown wood, brick, sunlight flares.
  Night club scene switches to neon purple/teal for the low point.
- **Recurring sets:** bathroom mirror, city sidewalk with brick shops, vintage
  barbershop (bulb-lit mirrors, barber pole, clippers laid out), club, park.
- Shop signage is invented and on-theme (PREMIER CUTS, THE COMMUNITY
  BARBERSHOP, METRO GROOMING, GENTLEMAN'S GROVE).
- **3D medical cut-aways for every claim:** stomach with glowing fluid, skin
  cross-section with follicles, golden particles moving into the root, a green
  shield bubble for "blocking DHT", green glowing follicles for "rosemary".
- **Stat overlays inside the cut-aways:** thin, elegant serif or light-sans
  numerals in cream/gold ("82%", "40x"), a small caps label ("DEFICIENT",
  "More Absorption"), a thin gold progress bar and tiny grey fine print
  underneath. Callout labels with hairline leader lines.
- **Camera:** each shot is an AI image-to-video clip of 2–4 s with a slow
  push-in or gentle drift; the subject moves a little (walks, turns head,
  touches hair). Hard cuts on the lyric beats; no flashy transitions.
- **Product placement:** the pack appears only from 0:44 onward, in the
  barber's hand, then in the hero's hand, then on the end card.

### Captions
- The **full lyric line**, in ALL CAPS, white, heavy sans (Montserrat
  ExtraBold / Open Sans ExtraBold feel) with a dark outline and soft shadow, no
  box.
- Up to 2 lines, centred, lower third (about 72–75% of frame height),
  ~28–32 px at 720 wide.
- The caption changes per lyric line, with no word-by-word karaoke highlight.

### End card (last ~3 s)
- Dark charcoal → coral/red vertical gradient with faint floating particles.
- White bold sans headline: "50,000 BROTHERS / ALREADY GROWING".
- Product pack centred on a glowing white pedestal disc.
- Red pill button "Tap Learn More" that fills in.

## 6. Production recipe

1. **Write the song** (~38 lines, 3 verses + hook): pain → mentor →
   mechanism (one claim per line) → milestones → proof/offer.
2. **Generate the track** with an AI music tool; aim for a 90–100 s cut.
3. **Transcribe the track** with word timings (`audio-lab/scripts/analyze_audio.py`)
   to get each line's start/end; this is your edit list.
4. **Shot list:** one image prompt per lyric line; reuse the same locations
   for before/after pairs; keep the character consistent (reference image or
   character LoRA).
   > "Stylized photoreal 3D animation, Pixar-like, [character description],
   > [action], [location], warm golden-hour light, shallow depth of field,
   > vertical 9:16, cinematic"
   > Cut-aways: "3D medical visualization, cross-section of human scalp skin
   > with hair follicles, glowing golden nutrient particles, warm bokeh,
   > macro, vertical 9:16"
5. **Animate** each still for 2–4 s (image-to-video), slow push-in.
6. **Assemble** in HyperFrames/CapCut: cut on lyric lines, add captions, add
   stat overlays on the claim shots, add the end card, master to −14 LUFS.

## 7. Notes before copying the pitch

- The "82% deficient" overlay's own fine print is about vitamin D levels in the
  general population, not about follicles. Claims like "40× absorption",
  "matching minoxidil" and "no side effects" need real evidence if you use
  them. Health/supplement ads that make unproven claims break platform ad
  policies and FTC rules. Use the *structure*; source your own claims.
- Don't reuse this ad's song, characters or brand. Write new lyrics and make
  your own track.
