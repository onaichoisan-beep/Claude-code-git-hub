# Scroll 2 Score — brand bible

Channel: **Scroll 2 Score** — NEET / MBBS Biology reels (YouTube Shorts first, then Instagram).
Owner: a 2nd-year MBBS student. Audience: NEET aspirants and junior medicos. Language: **Hinglish**.
This file is the source of truth for every reel. When it disagrees with older projects, this file wins.

## 1. Mascot: Pixy "Dr. Dragon" (FINAL — do not redesign)
A tiny doctor in a dragon hood. Personality: explains medicine like gossip, roars when something is NEET-important.

- **Hood:** blue dragon hood whose open jaw frames the face; **small, cute rounded fangs (3 top, 2 bottom)**;
  angry-cute dragon eyes + nostrils on top; **gold horns**; **orange crest spikes**; scale marks on the sides.
- **Face:** **big expressive eyes** (white disc + large black pupil, eyelids for attitude), pink blush, tiny mouths.
- **Body (Chi-style):** small torso, long noodle arms, mitten hands, long legs, big round shoes.
- **Outfit:** cream lab coat, blue shirt, stethoscope, "PIXY" badge with orange stripe, brown trousers, blue shoes.
- **Emotions (9):** friendly, joy, sly, gusto, confusion, watching, upset, angry, shock.
- **Poses (10):** stand, wave, point, think, celebrate, shrug, facepalm, hips, walk, back.

Code + assets:
- Generator: `videos/pixy-dragon/tools/dragon_pixy.cjs` → `hood(expr, mouth)` (head), `pixy({expr, pose, back})` (full body),
  `MOUTH_SVG` (mouth shapes: closed, smile, mid, open, oh, joy, …; `hood(e, 'none')` = head without mouth for lip-sync layers).
- Ready assets: `videos/pixy-dragon/final/` (transparent PNG + SVG for every emotion and pose, sheets, README).
- In reels, use **only the head** (face), centred, lip-synced. Full body only when a pose is really needed.

## 2. Palette (FINAL)
| Use | Name | Hex |
|---|---|---|
| Background, cards | Butter | `#feefb8` (dotted bg: `rgba(159,192,214,.45)` dots, 46px grid) |
| Hood, shirt, shoes, accents | Blue | `#c4dae8` (dark `#9fc0d6`) |
| Outlines, text, dark cards | Chocopie | `#432f2e` |
| Highlight / fumarate-type accent | Orange | `#e8743b` (text-safe orange `#b2461a`) |
| Horns, stars, bulb | Gold | `#f2c94c` / `#F6D365` |
| Coat, light cards | Cream | `#FFFCF2` |
Correct-answer green (only for the ✓ moment): `#2f9e5b` / fill `#bfe8c8`.
(An alternate Midnight/Chartreuse/Powder/Lapis version exists but is NOT used.)

## 3. Fonts (local TTFs in each project `assets/fonts/`)
- **Playfair Display 900** — questions, big serif titles.
- **Bagel Fat One** — keywords, buttons, punchy labels.
- **Inter 800** — options, small labels.
Copy them from `videos/acetyl-coa/assets/fonts/`.

## 4. Reel format (the "PYQ" format — default for every reel)
~30–50 s, vertical 1080×1920.
1. **Hook (0–4 s):** "Ye question **NEET 20XX** mein aaya tha!" + exam stamp + MCQ card with 4 options.
2. **Lock it (≈3 s):** "Comment mein apna answer lock karo… 3… 2… 1!" with a countdown.
3. **Explanation by ELIMINATION:** knock out wrong options one by one with animated mini-scenes. Do NOT reveal the answer early.
4. **Reveal (at the END of the explanation):** "Sahi answer hai — ___!" — tick + green + sparkles + Pixy joy.
5. **Previous reel's answer** (2–3 s): "Pichli reel ka answer — ___ ✅".
6. **CTA:** a NEW related question (mini MCQ) + "Answer agli reel mein — follow karo!".

Rules:
- **Brand name "Scroll 2 Score" appears ONLY on the final follow frame.** No logo/name anywhere else in the reel.
- **Instagram/Shorts safe zone:** keep Pixy and all key content out of the right button column
  (x > ~930, y 1000–1720), the bottom caption zone (y > ~1600) and the top bar (y < ~120).
  Pixy face: ~410 px wide, centred around x 540, top ≈ 1135.
- **Fully animated** — no stock photos. Molecules are cute "buddy" characters (circle + eyes + smile + label).
- **One idea per screen**, minimal text; big keywords only.
- **Pixy behaviour:** pops in, constant gentle sway, lip-sync to the voice loudness (15 fps), expression swap with
  squash-stretch on key words, jolts on big moments, head shake on "Out!", pop-up reactions (❗🔒❓💡✨❤️🚫) beside the head.
- **Shorter is better** — aim ≤ 40 s when the script allows.

## 5. PYQ honesty rules
- Source bank: `neet-biology-previous-year-papers-mcq-bank.pdf` (user upload; 1988–2013).
- **Only 2013 questions are "NEET 2013".** 1988–2012 are **AIPMT** — say "AIPMT 20XX", never "NEET 20XX".
- The bank's answer key has **errors** (e.g. antihistamine → allergy, palindrome GAATTC, DNA separation → electrophoresis).
  **Verify every answer yourself** against NCERT before scripting.
- Shortlist of the first 10 (verified): Acetyl CoA (NEET 2013, done = reel #2), Down's syndrome, menstruation/progesterone,
  trypsinogen, potato eyes = axillary buds, co-dominance, K⁺ intracellular cation (all NEET 2013), sporopollenin (AIPMT 2011),
  HIV & central dogma (AIPMT 2012), Widal → typhoid (AIPMT 2010).
- Open loop: reel #2 asked "1 Acetyl CoA → Krebs cycle → kitne CO₂?" → **answer B (2)** goes at the start of the next reel.

## 6. Voice
The user records/generates the narration (ElevenLabs, voice "Chinku – Casual Cool Course Narrator") and sends the mp3.
**Never generate the voice yourself** unless asked. Give the script as a plain copy-paste block (+ an optional version
with ElevenLabs v3 tags like [excited], [whispers]).

## 7. Thumbnails & YouTube
- Vertical 1080×1920 (Shorts) + 1280×720 (feed). Exam stamp, big question (Playfair), Pixy shocked face on a gold sunburst,
  ❗ bubble, options **blurred** (curiosity), a short hook pill. No channel name on thumbnails.
- YouTube title ≤ 100 characters; description = hook + MCQ + "answer reel mein" + previous answer + next question
  + chapter/exam + 3 hashtags first (#NEET #NEETBiology #NEETPYQ); tags ≤ 500 characters.
