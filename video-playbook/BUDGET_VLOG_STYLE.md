# Style Breakdown: the "How much do I spend" Talking-Over-B-roll Vlog

Reference: *HOW MUCH DO I SPEND AS A MED STUDENT 💸* (Instagram/YouTube Short, 55 s).
Everything below was measured from the file (scene detection, caption-pixel
tracking at 30 fps, Whisper word timings, Demucs voice/background split,
EBU R128 loudness). Raw numbers are in `reference/budget-vlog-timeline.json`;
contact sheets (one frame every 0.5 s) are `reference/budget-vlog-sheet-0..3.jpg`.

This is the opposite of the Field Notebook style (`PLAYBOOK.md`). There, the
graphics do the work. Here, **the voice does all the work and the footage just
has to feel real**. No motion graphics, no transitions, no music, no SFX.

---

## 1. Technical format

| Spec | Measured value |
|---|---|
| Aspect / resolution | 9:16, 720×1280 (shoot 1080×1920) |
| Frame rate | 60 fps (phone footage, left at native rate) |
| Length | 55.5 s |
| Shots | 22 hard cuts, **average shot 2.5 s** |
| Transitions | **None.** Every edit is a straight cut. No zooms, no speed ramps, no whooshes. |
| Mix loudness | −15.4 LUFS integrated, LRA 4.3 LU (heavily compressed, very even) |
| True peak | +0.2 dBFS (it clips slightly: **don't copy this**, limit to −1 dBTP) |
| Voice | Starts at **0.00 s**, ends at 55.40 s, video ends at 55.48 s |
| Music / background | Background stem is **−51.7 LUFS**: effectively silent. Raw clip audio is muted. |
| Narration speed | **187 words/min**, Hinglish (English frame sentences, Hindi details) |
| Pauses | Only one pause over 0.4 s in the whole video (0.78 s at 32.6 s) |

---

## 2. Structure (the timeline)

| Time | Shot (what we see) | Voice-over | Lower caption |
|---|---|---|---|
| 0.00–3.43 | **Selfie, face to camera**, in scrubs + surgical cap, tired after duty | "Hello, so today let me show you how much do I spend in a month as a med student in India." | — |
| 3.43–6.82 | POV: hand holding an Amul milk carton in the hostel room | "सबसे पहले, I live in a single seater room…" | (6.03) `hostel fee: ₹50/month` |
| 6.82–10.28 | Selfie at a railway platform, squinting in the sun | "…सर्कारी hostel में, जिसकी फीस…" | ″ |
| 10.28–12.35 | Close-up: chillies in hand over a bowl | "…50 रुपये. उसके बाद," | (10.97) `groceries: ₹500-₹1000` |
| 12.35–14.03 | Chopped tomatoes in a mug | "talking about my groceries," | ″ |
| 14.03–16.65 | Bhel bowl, squeezing lemon (laptop in frame) | "सब्जियां, जो भी मैं चुटर-पुटर खाती हूं," | ″ |
| 16.65–18.92 | Packet of sev, then the finished bowl | "वो सब कुछ 500 to 1000 चला जाता है." | ″ (off at 18.93) |
| 18.92–20.57 | Cold coffee on a café counter | "जो मेरा मेन खाना है…" | **none** (gap between topics) |
| 20.57–27.18 | Tiffin (paratha + sabzi), two angles | "…मेरी meals… 2,000 to 3,000 के budget में…" | (20.77) `meals: ₹2-3k` |
| 27.18–33.35 | Bank counter, then campus food stall | "मैं कहां खा रही हूं… college की फीस… ₹390" | (29.00) `college fee: ₹390` |
| 33.35–37.52 | Tablet in hand, lecture app | "एक semester की 2345 होती है." | (35.77) `books not included` |
| 37.52–39.78 | Selfie eating street food in a market | "…एक बड़ा investment कर रही हूं already." | ″ |
| 39.78–41.80 | Selfie, taking glasses off, eyes closed | "और WiFi plan ₹500 monthly…" | (40.47) `Wi-Fi: ₹500` |
| 41.80–45.32 | Jewellery stall, two angles | "…जो मेरे room में installed है." | ″ |
| 45.32–47.52 | POV: holding a paperback book on a bus | "And last but not the least, I do not…" | (44.93) `personal experiences no restrictions` |
| 47.52–50.95 | Tripod shot: side-plank workout | "…restrict myself from spending on experiences like" | ″ |
| 50.95–51.97 | Marigold flowers (**1.0 s**) | "books, my fitness," | ″ |
| 51.97–52.92 | Lotus flower at a temple (**0.95 s**) | "taking up new courses," | ″ |
| 52.92–53.72 | Trees and garden (**0.8 s**) | "doing new" | ″ |
| 53.72–55.48 | **Selfie, smiling, walking outside** | "things, and yeah, that's about it." | ″ |

### The shape
1. **Hook (0–3.4 s): face, identity, question.** You see the creator in scrubs
   (that proves "med student" without saying it) while the title asks the
   question. The voice starts on frame 1.
2. **Body: one topic per line item**, in a fixed order: rent → groceries →
   meals → college fee → books → Wi-Fi → lifestyle. Each topic gets **2–4 shots
   over 4–8 s**.
3. **Ending: an accelerating montage.** The last list ("books, fitness,
   courses, new things") gets one shot per item at 1.0 → 0.95 → 0.8 s. **Each new shot arrives as
   the next item is spoken** (the 50.95 and 51.97 s cuts fall exactly in the gaps
   between "books, | my fitness, | taking up").
4. **Bookend: it opens and closes on her face.** Tired selfie at the start,
   smiling selfie at the end. That's the whole emotional arc in two shots.
5. **No CTA, no outro, no end card.** "That's about it" and the video stops
   80 ms later.

---

## 3. Clipping rules (how the cuts are placed)

- **The voice-over is one continuous track; the footage is cut underneath it.**
  18 of the 21 cuts I could align land in the middle of a word. Cuts don't wait for sentences,
  and they're **not** on a music beat (there's no music). Don't cut on sentence
  ends; that makes it feel like a slideshow.
- **Shot length 1.5–4 s, average 2.5 s.** The first three shots are almost
  identical length (3.43, 3.39, 3.46 s), which sets a steady rhythm before the
  body speeds up to roughly 2 s.
- **Match the topic, not the word.** B-roll is loosely relevant day-in-the-life
  footage: food for groceries, a tiffin for meals, a bank counter for fees. The
  Wi-Fi line plays over a jewellery stall. Honest, varied footage beats literal footage.
- **Mix three camera types and rotate them:**
  - **Selfie / face** (5 shots: start, platform, market, glasses, end). These
    are the "human" anchors, and one appears roughly every 10–15 s.
  - **POV hands** (milk, chillies, lemon, coffee, tiffin, tablet, book, lotus).
    Hands doing something keeps a still object alive.
  - **Static / tripod or pure place** (bank counter, food stall, workout,
    jewellery, flowers, trees).
- **Every shot has movement**: a handheld drift, a hand entering the frame, a
  squeeze, a pour, or walking. There are no locked-off empty frames.
- **Within a topic, show process to result.** Groceries go raw chillies →
  chopped tomato → mixing bhel → sev packet → finished bowl.
- **Speed up into the end.** The last 5 s average 0.9 s per shot.

## 4. Captioning rules

There are **two text layers and nothing else.**

### 4.1 The title (permanent)
`HOW MUCH DO I SPEND IN A MONTH?!`
- On screen **from frame 0 to the last frame**, never animated.
- ALL CAPS, white, humanist sans **italic**, with a thin black outline and a
  soft drop shadow down and to the right.
- Spans almost the full width (x ≈ 25–695 of 720), **centre y ≈ 270 / 1280
  (21% from the top)**: above the face, below the platform UI.
- It ends in `?!`: the question is the hook, repeated for anyone who scrolls in late.

### 4.2 The lower label (one per topic)
`hostel fee: ₹50/month` · `groceries: ₹500-₹1000` · `meals: ₹2-3k` ·
`college fee: ₹390` · `books not included` · `Wi-Fi: ₹500` ·
`personal experiences no restrictions`
- **Format: `lowercase category: ₹amount`.** These are short, not subtitles,
  with no full sentences.
- **Bright yellow `#F0F92F`** with a thick black outline and no box. It's the
  same italic humanist sans as the title, in sentence case.
- **Centre y ≈ 830 / 1280 (65% from the top)**, horizontally centred, about
  370 px wide. It wraps to 2 lines when long and stays inside x ≈ 160–560.
  This keeps it clear of the right-side like/comment buttons and the bottom caption area.
- **Hard on, hard off.** No pop, no typewriter, no word-by-word reveal.
- **Timing: it appears 0.1–0.5 s *before* the voice starts that topic**
  (college fee: caption 29.00 s, voice 29.24 s; books: 35.77 vs 36.06; Wi-Fi:
  40.47 vs 40.62; lifestyle: 44.93 vs 45.04). The reader sees the number
  just before hearing it.
- **It stays across cuts.** One label covers 2–4 shots. It is **not** tied to
  cuts: only 1 of 7 caption changes falls near a cut.
- **There's a deliberate blank between topics** (18.93–20.77 s, the coffee shot).
  The old label goes off when its sentence ends, and the new one comes on with
  the next topic.
- The amount is always written as a symbol and number (`₹2-3k`), even when the voice
  says it in full words. Captions are for skimmers.

## 5. Audio rules

- **The voice is the soundtrack.** It's dry and close-mic'd, with no reverb and
  no music bed. Every clip's own audio is muted. (Demucs found the
  background at about 38 dB under the voice.)
- **No gaps.** The voice runs from 0.00 to 55.40 s with one pause over 0.4 s.
  Remove breaths and dead air and tighten word gaps.
- **Heavy, even compression**: LRA 4.3 LU, and the per-3-second voice level
  stays within about 5 dB the whole way through. Aim for −14 to −15 LUFS with a −1 dBTP limit.
- **Delivery is conversational Hinglish.** English carries the structure
  ("talking about my groceries", "and last but not the least") and Hindi
  carries the details. Use signposts: *सबसे पहले → उसके बाद → और → and last*.
- **Say the amount once, at the end of each topic's sentence**, so the sentence
  builds up to the number, and the caption has already shown it.
- No SFX: no cash-register ding, no whooshes on cuts. The plainness reads as authentic.

## 6. Recipe for a new one

1. **Script**: write a hook line plus 5–7 line items, each `<signpost> + what it is
   + context + amount`, and finish with a values/lifestyle item and "that's about it."
   Aim for 170–190 wpm, so about 160–180 words for 55 s.
2. **Record the VO first** in one take, then cut out breaths and pauses over 0.3 s.
3. **Shoot B-roll to the list**: for each item, get 2–4 clips of 2–4 s each, mixing
   selfie, POV-hands, and place shots. Get a tired or "real" selfie for the open
   and a happy selfie for the close.
4. **Lay out the edit**: VO on one track; B-roll on top, cut every 1.5–4 s
   regardless of words; first 3 shots about 3.4 s; final list item montage at about 1 s
   per shot on the spoken items; open and close on the face.
5. **Text**: the title at y≈21% for the whole runtime, plus one yellow `category:
   ₹amount` label at y≈65% per topic, switched on 0.1–0.5 s before the topic's
   first word, kept across cuts, and blank between topics.
6. **Mix**: mute the clip audio, compress the VO, normalise to −14/−15 LUFS, limit to −1 dBTP.

### Fonts and colours
| Element | Free match | Colour | Stroke |
|---|---|---|---|
| Title | Ubuntu Medium Italic / Open Sans SemiBold Italic, ALL CAPS, ~34 px @720w | `#FFFFFF` | 2 px black, plus drop shadow (2,2) 60% |
| Lower label | same family, sentence case, ~30 px @720w | `#F0F92F` | 4 px black, no shadow |

### ffmpeg sketch (captions and mix only)
```bash
ffmpeg -i edit.mp4 -i vo.wav -filter_complex "
 [0:v]drawtext=fontfile=Ubuntu-MI.ttf:text='HOW MUCH DO I SPEND IN A MONTH?!':
   fontsize=34:fontcolor=white:borderw=2:bordercolor=black:shadowx=2:shadowy=2:
   shadowcolor=black@0.6:x=(w-tw)/2:y=255,
 drawtext=fontfile=Ubuntu-MI.ttf:text='hostel fee\: ₹50/month':fontsize=30:
   fontcolor=0xF0F92F:borderw=4:bordercolor=black:x=(w-tw)/2:y=815:
   enable='between(t,6.03,10.97)'[v];
 [1:a]acompressor=threshold=-20dB:ratio=4,loudnorm=I=-14:TP=-1[a]" \
 -map "[v]" -map "[a]" out.mp4
```
