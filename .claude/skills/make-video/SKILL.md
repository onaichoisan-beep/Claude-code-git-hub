---
name: make-video
description: >
  Make a vertical Hindi/Hinglish explainer video in the "Field Notebook" style defined in
  video-playbook/PLAYBOOK.md (aged-paper specimen-file look, two-tier red punch headlines,
  flip counters, stamps, fast Hinglish voice-over). Use when the user runs /make-video with a
  topic, or asks for a new video "in the playbook style" / "like the reference videos".
  Takes the topic plus optional notes on script, voice, images, music and length.
argument-hint: "<topic> [notes: my script / my voice / my images / music / length]"
---

# /make-video: Field Notebook explainer

Request: **$ARGUMENTS**

`video-playbook/PLAYBOOK.md` (repo root) is the source of truth for style, voice, structure and
sound. Read all of it before doing anything else, and look at the frames in
`video-playbook/reference/` to calibrate the look. When this file and the playbook disagree, the
playbook wins.

## 0. Read the request

Pull these out of the request. Use the default when something isn't stated, and **don't ask about
anything that has a default**:

| Item | Default |
|------|---------|
| Topic | required; if missing, ask for it and stop |
| Angle / must-include facts | find them in research |
| Script | Claude writes it |
| Voice-over | the user records it after approving the script; AI voice only if they ask for it |
| Subject images | Claude builds them; use the user's own files instead if they attach any |
| Music | a free dark documentary underscore |
| Length | 2:30–3:00 (~450–550 Hindi words) |
| Watermark | none |
| On-screen text | English keywords, two-tier headline |

Work in `videos/<topic-slug>/` at the repo root. Keep every file for this video there.

## 1. Research (playbook section 6)

- Search the web. Find: the one-line paradox hook, the India angle, 5–8 hard numbers, one dated
  proof point (study / experiment / court case), and the twist or ending.
- Verify **every number against 2 independent sources**. Drop anything you can't verify, and
  don't present it as fact.
- Save `research.md`: the facts, each with its source URLs.

## 2. Script + beat sheet, then wait for approval

- Write the narration in conversational Hindi (Devanagari), keeping English technical words in
  English, following the structure in playbook section 4: hook → name reveal → India angle by
  0:45 → 3–5 question-led chapters → "सबसे अजीब हिस्सा" pivot → dated proof → ending (callback
  question / future question / actionable advice). Don't add a "like & subscribe" ending.
  One sentence per line, 2–3 s each.
- Build the beat sheet using the playbook section 8 template, one row per narration line:
  `Chapter · FIG | Narration | small text / RED PUNCH | visual + prop + motion | SFX`.
  Every row must introduce a new visual element.
- Save `script.md` (script + beat sheet). Send it to the user and **stop**. Ask them to approve it
  or request changes, and to say whether they will record the voice-over.
  - Skip this stop only if the request explicitly says not to wait (e.g. "no review", "go straight
    to render").

## 3. Gather media (after approval)

- **Voice-over:** use the user's recording if they send one. If they asked for an AI voice, make
  it with `/media-use`, using a Hindi voice that sounds energetic but calm. Either way: cut breath
  gaps over ~0.2 s, then transcribe for word-level timestamps so every beat lands on its word.
- **Subject cut-outs:** use the user's images if provided. Otherwise source them or generate them
  with `/media-use`. Remove backgrounds and add a soft drop shadow. If nothing photoreal is
  available, draw clean illustrated versions and tell the user which assets are stand-ins.
- **Music + SFX:** resolve them with `/media-use` (SFX needs no account). Follow the SFX table in
  playbook section 5.

## 4. Build

Hand off to `/hyperframes` (route: faceless-explainer) with this brief. Skip its interview: the
answers are already fixed here and in the playbook.

- 9:16, **1080×1920, 30 fps**.
- **Reusable paper canvas:** kraft paper with grain, vignette, fold creases, punch holes and a
  header strip (chapter label left, `FIG. N` right, thin rule). Build it once as a component.
  Dark lightbox / starfield / sepia-photo / lined-notebook variants per chapter as the playbook
  describes.
- **Two-tier headlines:** a condensed heavy caps font (Anton/Bebas Neue/Oswald), small dark setup
  line plus a big brick-red `#C0392B` punch word, appearing word by word in sync with the VO.
  Monospace (IBM Plex Mono/Space Mono) for labels.
- **Prop components:** split-flap counter, torn-paper label, rubber stamp (slams in at 110% and
  settles to 100%), red name bar + Latin name, specimen tag, microscope viewport with scale bar,
  x-ray frame, pictogram grid, hand-drawn bar chart, ✗ checklist, red strike/circle/tick
  annotations.
- **Motion:** a slow push-in on every scene, pop/slide-in with slight overshoot, a match transition
  where the subject carries across a cut, and a paper-tear reveal for the hook's shock beat.
- **Pacing:** something new on screen on every narration line (1.5–3 s); full scene changes about
  every 6–8 s; never let the frame sit static.
- **Audio** (`/hyperframes-audio`): music never drops out, sits −18 to −22 dB under the VO and
  ducks around it, an SFX on every pop/slam/stamp/flip, no silence over 0.3 s, master
  **−14 LUFS**, true peak −1 dBTP.

## 5. Review and deliver

- Render a preview. Pull a contact sheet (1 frame / 3 s) and compare it to `video-playbook/reference/`.
  Fix anything off-style before showing the user.
- Run the playbook section 10 checklist and fix every failing item.
- Send the preview MP4 to the user, iterate on their feedback, then render the final.
- Commit `videos/<topic-slug>/` (project, script, research; not large raw media unless asked) and
  push to the current branch.
