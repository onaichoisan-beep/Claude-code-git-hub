# Claude-code-git-hub

This repo makes short vertical education videos with HyperFrames (HTML → MP4).

## Scroll 2 Score (main project — read this first)
The user runs **Scroll 2 Score**, a NEET/MBBS Biology reels channel with the mascot **Pixy "Dr. Dragon"**
(a tiny doctor in a blue dragon hood, Blue/Butter/Chocopie palette).

- Brand bible (style, character, palette, fonts, reel format, rules): **`video-playbook/SCROLL2SCORE.md`**
- Workflow skill: **`/scroll2score`** (`.claude/skills/scroll2score/SKILL.md`)
- Character generator + final assets: `videos/pixy-dragon/` (`tools/dragon_pixy.cjs`, `final/`)
- Reference reel to copy for new ones: `videos/acetyl-coa/` (reel #2, NEET 2013 Acetyl CoA)
- Earlier reels: `videos/urea-krebs-v3/` (reel #1, Krebs bicycle)

Non-negotiables: Pixy design and palette are final; the PYQ format (hook → elimination → late reveal → new question;
no countdown, no previous-answer segment — that goes in a pinned comment); **"Scroll 2 Score" only on the last frame**; keep content in the Reels safe zone;
animated + suitable free stock images inside the safe zone; SFX on every render; the user supplies the voice; label pre-2013 PYQs as AIPMT and verify every answer.

## Other
- `video-playbook/PLAYBOOK.md` + `/make-video`: a different "Field Notebook" style (not Scroll 2 Score).
- `audio-lab/`: TTS / audio analysis tools.
