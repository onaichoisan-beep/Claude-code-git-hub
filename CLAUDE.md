# Pixel explainer shorts

This repo makes 30-second vertical pixel-art Reels/Shorts (science + Indian mythology) with HyperFrames.

**For any video request, use the `pixel-short` skill** (`.claude/skills/pixel-short/SKILL.md`): it holds
the owner's confirmed style, pacing, sound rules, build recipe and Instagram caption format. Don't ask the
owner questions or run review checkpoints — build, self-check, render, deliver, commit and push.

- `videos/_engine/` — shared pixel engine (`pixel-engine.js`) and sound library (`sfxlib.py`)
- `videos/<slug>/` — one finished project per video (`index.html`, `scripts/synth_audio.py`, `BRIEF.md`, `renders/video.mp4`)
- `pixel-explainer-style.md` — the original analysis of the reference videos (@BITWONDER style)
