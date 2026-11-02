---
name: make-myth-video
description: >
  Make a vertical Hindi mythology / folk-tale short in the "Myth Puppet Theatre" style defined in
  video-playbook/MYTH_PUPPET_STYLE.md (animated leather shadow-puppet characters, red theatre curtain,
  romanised Cinzel karaoke captions, calm storyteller voice with pauses, drone bed, binary comment-bait
  ending). Use when the user runs /make-myth-video with a story, or asks for a mythology/Puranic/lokkatha
  video "in the puppet style" / "like the Shani or Barbarik videos".
argument-hint: "<story> [notes: my script / my voice / length]"
---

# /make-myth-video: Myth Puppet Theatre short

Request: **$ARGUMENTS**

`video-playbook/MYTH_PUPPET_STYLE.md` is the source of truth. Read all of it, including the two
reference scripts in section 9, and look at `video-playbook/reference/puppet-*.jpg` before starting.
When this file and the playbook disagree, the playbook wins. Load the `hyperframes` skill before building.

## Defaults (don't ask about these)
| Item | Default |
|------|---------|
| Story | required; if it's missing, ask and stop |
| Length | 1:55–2:05, 200–280 Hindi words |
| Script | Claude writes it in romanised Hindi, following the 4.0 blueprint beat by beat |
| Voice | the user records it after approving the script; TTS (`hi-IN-MadhurNeural`) only if asked |
| Captions | romanised, Cinzel, mint karaoke word |
| Music | Indian drone bed + low booms |

Work in `videos/<story-slug>/`.

## Steps
1. **Research the versions** of the story. Pick one, note the source (which Purana or which region's
   lokkatha), and note what is *not* in the original texts. That becomes the HONESTY line.
2. **Write the script** as a table: t · beat · line · visual · SFX. It must include, in order: a paradox
   hook with a number ending in "Kaise?/Kyon?", "Jawab ___ mein chhipa hai", a FRAME line that names the
   source, story beats with quoted dialogue, a one-line TWIST plus a one-word punch, a TODAY link, the
   HONESTY line, a one-image MORAL, and a binary CTA. **Show the script to the user and wait for approval.**
3. **Voice**: keep 0.5–0.9 s pauses between lines. Get word timings with faster-whisper (pass a numpy
   array, because the PyAV `metadata_errors` bug breaks file input).
4. **Build**: jointed SVG puppet rigs (profile head, rivets, dotted trim, rod lines, amber glow), layered
   gradient sets, the curtain component (opens on FRAME, closes on CTA), dissolves between all scenes, and
   karaoke captions placed clear of faces.
5. **Audio**: drone bed ducked under the voice, booms on scene changes and the curtain, master -14 LUFS.
6. **Check** against playbook section 8, render 1080×1920 @ 30 fps, and send the user the MP4.
