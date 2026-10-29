---
name: scroll2score
description: >
  Make a "Scroll 2 Score" NEET/MBBS Biology reel with the Dr. Dragon (Pixy) mascot in the channel's PYQ format
  (exam hook + MCQ, lock-your-answer countdown, elimination, late reveal, previous answer, new question CTA).
  Use when the user asks for a new reel / script / PYQ video, a thumbnail or YouTube title/description/tags for one,
  or anything about Pixy / Dr. Dragon, the Scroll 2 Score style, palette or character.
argument-hint: "<PYQ or topic> | script | <path to voice mp3> | thumbnail | youtube"
---

# /scroll2score

Request: **$ARGUMENTS**

**Read `video-playbook/SCROLL2SCORE.md` first — it is the source of truth** (mascot, palette, fonts, format,
brand rule, safe zone, PYQ honesty rules). The finished reference reel is `videos/acetyl-coa/` — copy it, don't start blank.
Load `/hyperframes` (and `/hyperframes-core`) before writing or editing composition HTML.

## Stage A — script (when given a PYQ/topic)
1. Pick/verify the PYQ: correct exam label (NEET only for 2013; AIPMT before), and **verify the answer yourself** (the PDF key has errors).
2. Write the script in the 4-part format (hook → elimination → reveal → new related question + follow). No countdown,
   no previous-answer segment (give a pinned-comment text instead). Hinglish, punchy, ~25–35 s spoken.
   Mark SFX cues and stock-image cues (source + what to show) in the scene table. Answer revealed only AFTER elimination.
3. Deliver: a scene table (time · narration · on-screen · Pixy expression), then a **plain copy-paste narration block**
   and an optional ElevenLabs-v3-tagged version. Note the next reel's answer.
4. Stop and wait for the user's recorded audio. Don't generate a voice.

## Stage B — animate (when given the voice mp3)
1. `cp -r videos/acetyl-coa videos/<slug>` (drop `renders/`, `.hyperframes/`), update `meta.json` / `package.json` names,
   copy the mp3 to `assets/audio/vo.mp3`.
2. Word timings: `npx hyperframes transcribe assets/audio/vo.mp3 --model small --language en --json`
   → `assets/audio/transcript.json` (whisper writes English words; match cues on those).
3. Lip-sync: 15 fps RMS of the voice → `assets/audio/lips.json` as `[[t, "closed"|"mid"|"open"], …]`
   (thresholds 0.1 / 0.4 of the 95th-percentile RMS) — see the Python snippet used for reel #2.
4. Edit `tools/build.cjs`: `cue('word', after)` table, scene groups, `EXPR_T` (Pixy expressions), `POPS` (pop-ups).
   Keep: Pixy head layers via `hood(expr, 'none')` + mouth layers from `MOUTH_SVG`; brand only on the final frame;
   everything inside the safe zone. Initial hidden states go in markup/CSS (`opacity="0"`), never `tl.set(..., 0)`.
5. `node tools/build.cjs && npx hyperframes lint`, then `npx hyperframes snapshot --at <scene midpoints>` and look at
   the contact sheet (check safe zone, overlaps, text fit) before rendering.
6. Add SFX (`/media-use` resolve --type sfx; see brand bible §4) mixed under the VO, stock images as in-safe-zone cards.
7. `npx hyperframes render -o renders/<slug>.mp4`, check audio with ffmpeg volumedetect, send the file.

## Stage C — publish kit
- Thumbnails: adapt `videos/acetyl-coa/tools/thumbnail.cjs` (vertical with blurred options + clean variant, plus 1280×720).
- YouTube: title options ≤ 100 chars, description (hook, MCQ, previous answer (+ pinned comment), next question, chapter/exam, 3 hashtags first),
  tags ≤ 500 chars. Instagram caption on request (≤ 5 hashtags).

Commit work to the current branch and push when the user is happy.
