# Pixel HD

This repo (Pixel HD) makes vertical, sharp HD pixel-art Reels/Shorts (science, Indian mythology, fiction fables) with HyperFrames.

**House style (STYLE_GUIDE.md): SHARP HD pixel art (360×640 render, light dither), a dark outline on every
living character, NO narration (owner's rule, Oct 31 2026: text cards + speech bubbles + sound only), and open-source sound
effects (CC0 packs, Openverse, jsfxr, the repo's synth kits).**

**For any video request, use the `pixel-short` skill** (`.claude/skills/pixel-short/SKILL.md`): it holds
the owner's confirmed style, pacing, voice casting, sound rules, build recipe and Instagram caption format.
Don't ask the owner questions or run review checkpoints — build, self-check, render, deliver, commit and push.

- `STYLE_GUIDE.md` — the owner's rules in one page
- `videos/_engine/new_video.sh <slug>` — start a new video from `videos/_template` in the house style
- `videos/_engine/` — sharp pixel engine (`pixel-engine.js`, `character()` outlines), narration (`make_voices.py`,
  `voicelib.py`, `VOICES.md`), sound (`osfx.py` open-source SFX, `SOUNDS.md`, `sfxlib.py`, `foley.py`)
- `videos/style-sample/` — the reference video for the current style
- `videos/<slug>/` — one finished project per video (`index.html`, `scripts/synth_audio.py`, `BRIEF.md`, `renders/video.mp4`)
- `pixel-explainer-style.md` — the original analysis of the reference videos (@BITWONDER style; the look has since moved to sharp HD)
