# Podcast Edit Style: the "Gut Feeling" Cold-Open Breakdown

What I learned from the first 5 minutes of
*Dating, Gen Z Slang, Food, & Jokes. This Podcast is a Vibe! | Dr. Pal | Abhishek Kumar*
(Gut Feeling with Dr. Pal: a 64-minute Tamil podcast, 1280×720, 25 fps).

Reference frames are in `reference/podcast/`.

How this was measured: scene-cut detection (ffmpeg `scene>0.25`), contact sheets at 2–5 fps,
full-res stills, Demucs voice/background separation, onset and tempo detection, and EBU R128
loudness. The speech is Tamil, so the story notes below come from the burned-in English captions.
I can't hear the audio, so sound effects are named from their spectrogram shape and timing,
and the names are best guesses ("riser", "slap") rather than identified sample files.

---

## 1. The big idea: two different edits in one video

The first 5 minutes are two edits with opposite rules:

| | **Cold open (0:00–1:12)** | **Main body (1:17 onward)** |
|---|---|---|
| Purpose | Trailer/hook: sell the episode in 70 s | The actual conversation |
| Hard cuts | **59 in 72 s**, a cut every **1.3 s** (median) | 44 in 223 s, median 3.4 s, mean 5.1 s |
| Captions | Word-by-word kinetic captions on **every line** | **None** |
| B-roll / memes | Constantly (about 40% of screen time) | Almost none (one thumbnail pop-up) |
| Music | Continuous bed, 117.5 BPM, with drops and track switches | **No music at all** (background stem is −65 LUFS, which is room tone) |
| SFX | Many: risers, tones, impacts | Just a whoosh on the lower-third |
| Loudness | −18.7 LUFS integrated | −23.6 LUFS (voice only) |

**Lesson:** spend all the editing effort on the first minute. Once viewers are in, a plain
two-camera conversation holds them. The heavy edit is only needed to win the first 60 seconds.

Order of the opening:
```
0:00  Cold open: ~25 best moments from the whole episode, recut as a fast montage
1:12  "THIS IS WHY I'M NOT INTERVIEWING WITH THESE GENZ KIDS": host laughs, ends on a laugh
1:12  CONTENT DISCLAIMER card, black, ~4 s, SILENT (a palate cleanser and legal cover)
1:16  Episode proper. Guest name lower-third (1:18) → host lower-third (1:27)
1:58  "SWITCH TO 1.5X" nudge (about 40 s into the body)
2:40  First wide 2-shot (shows the set and the neon "Gut feeling with DR PAL" sign)
```

---

## 2. Storytelling in the cold open

The cold open is a recut of moments, not a summary. Each moment is a **setup → punch** pair,
usually a question from one person and a reaction or punchline from the other, separated by a
hard cut. The order is chosen for emotional variety, not chronology:

| Time | Beat | Device |
|---|---|---|
| 0:00 | "What is your journey on stage sir?" → "What is a doctor doing in a stand-up comedy show?" | Open on a question. The doctor is the unexpected thing |
| 0:03 | "That is actually very unique" | Validation |
| 0:04 | "I had a GIRL, 26 year old…" → "You know SHE…" → "As in YOU" | Story tease, cut off mid-story (open loop) |
| 0:07 | **B&W + film grain, music drops out → TV colour bars + beep** | A "censored / we can't show this" gag. It hides the payoff, so the loop stays open |
| 0:10 | "Who has more ANXIETY? Single people? or Married people?" → "Both sir" | Relatable question → comic answer |
| 0:13 | "HEADACHE is a UNIVERSAL problem" (Tamil movie meme) | Meme as reaction shot |
| 0:15 | "That's why I'M SINGLE I think" | Self-deprecating button |
| 0:18 | "In JANUARY there was COVID VACCINATION… I did like a VLOG… LOOK AT ME, nothing is HAPPENING to me" | The doctor's personal story, with real footage as B-roll |
| 0:23 | "Everybody is asking about THE NURSE" → guest laughs | Twist punchline |
| 0:26 | "Concerned about the GEN Z population here" (Tamil comedy meme) | Theme statement |
| 0:30 | "I found out in AWARD SHOW… I've not told this to ANYONE" (Oscars-slap meme) | Confession tease |
| 0:32 | "This biryani has 1000 CALORIES… so you SPLIT IT… and EAT HALF… then the next half TOMORROW" | Health topic disguised as comedy |
| 0:38 | "One guy is writing the comment: for this I CAN DIE" | Audience in-joke |
| 0:44 | "That DIET COKE is better than WATER" → "Convince me" | Controversial claim (hook for health viewers) |
| 0:46 | "Have you ever seen TWO STATES fight over a DIET COKE?" → "Diet Coke brings PEACE" | Absurd escalation, with animated map graphic |
| 0:51 | "How much FIBER do you think this meal has? 2 GRAMS vs 4 GRAMS… YAYYYY!" | Quiz moment the viewer plays along with, then a celebration |
| 1:00 | "THAPPU" (wrong!), guest's head flashes red | Comic "wrong answer" buzzer |
| 1:02 | "We have some weird GEN Z TERMS… the amount of SPIRITUALITY… IT'S A SPIRITUAL PODCAST" | Title-card-sized joke |
| 1:07 | "Dr. Pal to the power of INFINITY" | Hype |
| 1:09 | "This is WHY I'M NOT INTERVIEWING with these GENZ KIDS", host doubled over laughing | **End on the biggest laugh.** Doubles as the episode's thesis |

Patterns to copy:
- **Alternate topics every 3–6 s** (dating → anxiety → vaccine → Gen Z → food → diet coke → fiber → slang).
  The episode promises variety, and the title literally lists it ("Dating, Gen Z Slang, Food, & Jokes").
- **Alternate speakers on almost every cut.** Question from one, reaction from the other.
- **Open loops:** at least one story is cut off mid-sentence (the "26-year-old girl" story) and
  its payoff is hidden behind a gag. Viewers stay to hear the end.
- **Cut to reaction shots.** A laughing face after a punchline acts as the laugh track.
- **End on laughter + a thesis line, then reset with a silent black card.**

---

## 3. Captions / kinetic text (the core of the style)

See `reference/podcast/captions-and-graphics.jpg`.

### 3.1 Look
- **Font:** heavy, wide, geometric bold sans in ALL CAPS, slightly tight tracking.
  Free matches: **"The Bold Font"**, *Montserrat Black*, *Poppins ExtraBold*.
- **Colour code (the most important rule):**
  - **White** for connector words (`I HAD A`, `WHO HAS MORE`, `AND THEN YOU`), smaller.
  - **Yellow `#FFE600`** for the positive or neutral keyword (`GIRL`, `JOURNEY`, `VLOG`, `ANYONE`, `PEACE`, `WATER`, `SPLIT IT`).
  - **Red `#E8231F`** for shock, negative or "danger" words (`ANXIETY?`, `HAPPENING`, `I CAN DIE`, `1000 CALORIES`, `EAT HALF`, `THAPPU`, `DIET COKE`, `FIBER`, `GEN Z`).
- **Two- or three-tier stacks:** small white setup line, then the BIG coloured keyword, then a small white tail
  (`THE AMOUNT OF` / **SPIRITUALITY,** · `IN` / **JANUARY** / `THERE WAS` · `HEADACHE` / `IS A` / **UNIVERSAL** / `PROBLEMS`).
- **Size jump:** the keyword is about 2–2.5× the height of the connector words.
- No box and no heavy outline. Just a **soft dark drop shadow** so it reads on any background.

### 3.2 Motion
- **Word by word, synced to speech.** Each word appears the moment it is said, and the
  phrase builds up and then clears on the cut. It is never a full sentence at once.
- The keyword **pops in** (quick scale 120%→100%, ~4 frames). Connector words just appear.
- **Placement follows the empty space**, not a fixed subtitle line: left of the head,
  right of the head, or lower third, whichever side is empty in that shot. On B-roll it's usually lower-centre.
- A caption usually **survives the cut** into a B-roll and finishes there
  (e.g. "WHAT IS DOCTOR DOING IN A" starts on the host and completes over the movie clip).

### 3.3 Special text treatments
| Treatment | Where | How |
|---|---|---|
| **VS card** | 0:55 "2 GRAMS **VS** 4 GRAMS" | Italic gaming/sports font, yellow-gold gradient fill, thick black + white outline, big "VS" in the middle. Builds left → VS → right on 3 beats |
| **Text behind subject** | 1:06 "IT'S A SPIRITUAL PODCAST" | Giant yellow letters on black, with the cut-out host (photoshopped as a guru) **in front of** the word. Depth layering via rotoscope/AI subject mask |
| **Screaming caption** | 0:58 "YAYYYYY!" | Repeated letters, centred low, held on the celebration |
| **Header bar** | 0:01–0:04 | Black band at top with the 2-line caption **above** the B-roll, which is letterboxed below. Gives meme-format framing |
| **Thumbnail pop-up** | 2:17 | When the host mentions an old video, its YouTube thumbnail ("Side effect after my second dose", 1 MILLION views badge) pops in top-left for ~4 s |

---

## 4. B-roll and meme usage

Types used in the cold open, in rough order of frequency:

1. **Regional movie/comedy memes** (Tamil films: *Vasool Raja MBBS*, Vadivelu-style comic scenes).
   Used as **reaction shots**, never as decoration. Each matches the line literally
   ("headache is a universal problem", "concerned about the Gen Z population").
   A source tag (`▶ VASOOL RAJA MBBS`) sits top-left.
2. **Face-swap meme:** the host's face is pasted onto a movie character (0:02). Cheap, very funny.
3. **Global memes:** the Oscars slap (Chris Rock) for "I found out in award show".
4. **Literal stock footage:** COVID vials, biryani platter, diet coke glass, idli plate, silhouette
   man (single people) vs couple (married people). Each one **illustrates the exact noun said**.
5. **Personal archival footage:** the host's real vaccination vlog, shown as a **triptych**
   (B&W copies on both sides of a colour centre panel) to fill the 16:9 frame with vertical footage.
6. **Simple 2D graphic:** two black state silhouettes (Karnataka / Tamil Nadu) on white paper, and a diet-coke
   can that slides in between them (0:47). Explains "two states fighting over a Diet Coke" in 1 s.
7. **Prop sticker:** a biryani pot PNG pops onto the host's chest while he talks about it (0:34).

Rules:
- B-roll lasts **1–3 s**. It shows up exactly on the noun and leaves on the next speaker.
- **Slow push-in** (about 100→108% over the clip) on every still/stock shot so nothing is static.
- **Vertical footage → triptych** (blurred or B&W side copies), never black pillar bars.

---

## 5. Motion graphics and visual effects

| Effect | Time | Purpose |
|---|---|---|
| **Split screen 2-up** (host left, guest right) | 0:06, 1:47–2:00 | Shows the question and the reaction at once. Used for back-and-forth banter |
| **B&W + film scratches/grain** | 0:07–0:09 | "Dramatic / flashback / censored" moment. **Music drops out under it** |
| **TV colour bars (SMPTE)** | 0:09.5, ~0.5 s | "Technical difficulties" gag that hides a juicy answer. Paired with a ~1 kHz test-tone beep |
| **Red head flash** (subject mask filled red) | 1:00 | Visual "WRONG!" buzzer on the guest after "THAPPU" |
| **Glowing red magic circle / aura** behind the host | 1:07 | Hype for "Dr. Pal to the power of infinity" |
| **Sparkle/dust particle burst** | 0:15, 1:02, 1:09 | Transition into a new line, like a sparkle wipe |
| **Light-leak/flash transition** | ~1:02 | Bright flare frames between two shots |
| **Punch-in zoom** on reactions | throughout | Reaction shots are often a tighter crop than the talking shot |
| **Lower-thirds** | 1:18, 1:27 | Name in white heavy sans, role underneath in small bold (`Standup Comedian` · `Consultant Gastroenterologist (California) · Co-Founder of NewMe · Podcast Host`). Type-on reveal, no box, sits on a dark gradient at the bottom |
| **"SWITCH TO 1.5X / for a faster viewing experience"** | 1:58–2:04 | White heavy text with a thin orange underline, lower-left. A retention trick for long podcasts |
| **Logo bug** | always | "GUT FEELING" (mic icon inside the U), white, top-right, never removed |
| **Disclaimer card** | 1:12–1:16 | Black, red title "CONTENT DISCLAIMER", fair-use text in white |

See `reference/podcast/bw-tvbars-transition.jpg`, `text-behind-subject.jpg`, `overlays-lowerthirds.jpg`.

---

## 6. Sound design (measured on the Demucs background stem)

See `reference/podcast/cold-open-music-sfx-spectrogram.png`.

### 6.1 Mix levels
| Stem | Cold open | Body |
|---|---|---|
| Voice | −22.5 LUFS | −24.7 LUFS |
| Music + SFX | −30 LUFS (about 7–8 dB under the voice) | −65 LUFS (nothing) |
| Full mix | −18.7 LUFS | −23.6 LUFS |

The music bed sits only **about 8 dB under the voice**. That's much louder than an explainer
bed (20–25 dB under), so it makes the cold open feel like a trailer.

### 6.2 Music map of the cold open
| Time | What happens | Why |
|---|---|---|
| 0:00–0:05 | Light, bouncy bed | Energy from frame 1 |
| **0:05–0:09** | **Music cuts out** (bg falls to −67…−76 dB) | Silence = tension for the B&W "dramatic" moment |
| 0:08.5 & 0:09.8 | **Pure tone ~1.1–1.2 kHz** (TV test beep) | Pairs with the colour bars. A comedic "censor" |
| 0:10–0:47 | Main groove, **117.5 BPM**, steady | Carries the rapid montage |
| ~0:25, 1:00, 1:08 | **Rising chirps/sweeps** (1.3→3 kHz) | Riser/"boing" accents on punchlines and reaction cuts |
| **0:47–0:58** | **Track switch** to a heavier, bass-loud beat (~76 BPM) | New "segment" feel for the Two States / fiber quiz |
| 0:58–1:00 | Music drops out again | Breath before the payoff |
| **1:00.5** | **Biggest broadband hit** in the cold open (strongest onset, wide-band burst ~1 s) | The "THAPPU" red-head slap/buzzer impact |
| 1:01–1:11 | Main groove returns | Run to the final laugh |
| **1:12–1:16** | **Total silence** under the disclaimer card | Hard reset between trailer and episode |
| 1:18 | Short bright hit (~3.5 kHz) | Whoosh/swoosh on the guest lower-third |
| 1:16 onward | No music | Pure conversation |

### 6.3 SFX rules to copy
- **Drop the music** for drama and **slam it back** on the punchline. The silences are as important as the hits.
- **One signature SFX per gag**, matched to the visual: colour bars → test beep; "wrong" → buzzer/slap + red flash;
  hype → riser + aura.
- Reaction cuts get a **short riser or chirp**. Big payoffs get **one** heavy impact (don't stack them).
- Switching music tracks marks a new segment inside the montage.
- Graphics (lower-thirds, pop-ups) get a quiet whoosh, not a hit.

---

## 7. Camera / set (the base layer every effect sits on)

- **Two singles**, each framed as a medium close-up from a 3/4 angle, plus a **wide 2-shot** used rarely
  (first at 2:40, then every ~30 s as a reset).
- Each person has a **distinct colour world**: guest = deep red velvet curtain + white chair + plant;
  host = warm bookshelf, gold YouTube play button, neon logo glow. You know who's talking even in a 0.5 s cut.
- Wardrobe contrasts with the background (navy vs red, teal vs warm beige).
- Shallow depth of field, warm grade, and both faces lit softly from the front.
- Body cutting rule: **cut to whoever is speaking**, and cut to the listener for laughs and nods.
  Shots last 3–10 s, sometimes 15–20 s on a long answer.

---

## 8. Recipe: making a cold open in this style

1. **Mine the episode:** pull 25–35 moments of 2–5 s each. Pick for: a question, a laugh, a confession,
   a controversial claim, a quiz, a story cut off mid-way.
2. **Order them for variety:** never two moments on the same topic back to back. Alternate speakers.
   Open on "the unexpected thing about the guest". End on the biggest laugh and a line that states the theme.
3. **Trim hard:** a cut every 1–1.5 s on average. Cut off the breath before and after each line.
4. **Captions on every line:** white connectors, yellow good/neutral keyword, red shocking keyword, word by word,
   placed in the empty space beside the face.
5. **B-roll every 2nd or 3rd line:** a literal stock shot or a regional meme reaction, 1–3 s, slow push-in,
   with the caption continuing over it.
6. **One visual gag every 10–15 s:** censor bars, B&W flashback, red flash, face swap, text-behind-subject, VS card.
7. **Music:** a 115–120 BPM bed about 8 dB under the voice. Drop it out before 2–3 payoffs, switch tracks once mid-way,
   and use total silence for the disclaimer/transition card.
8. **SFX:** a riser on reaction cuts, a themed sound per gag, one big impact for the biggest gag.
9. **Then the episode:** silent card → guest lower-third → host lower-third → "switch to 1.5x" at about 40 s →
   plain two-camera conversation, no music.

## 9. Checklist
- [ ] Cold open is 60–75 s with a cut every ~1.3 s
- [ ] Every cold-open line has word-by-word captions with the white/yellow/red code
- [ ] At least one open loop (a story cut off before its payoff)
- [ ] 6+ distinct visual gags in the cold open
- [ ] Music drops out at least twice, and there is one track switch
- [ ] Cold open ends on a laugh, then a silent card
- [ ] Lower-thirds within 15 s of the episode starting
- [ ] Logo bug top-right throughout
- [ ] Body: no music, cut on the speaker, wide shot every ~30 s
