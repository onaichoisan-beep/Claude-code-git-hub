---
workflow: general-video
flow: automation
storyboard: no
message: "In a town where everyone's wrist clock shows when they will die, Leo's says one day left; he finds the mayor stealing everyone's time and gives it back, but his friend Mia's clock is blank."
destination: shorts
aspect: "9:16"
language: en
audience: general social viewers
length: "about 2:00"
angle: first-person spooky/mystery story with a twist ending
voice: "edge-tts: narrator en-US-AndrewNeural +22Hz; Mom JennyNeural; Mia AnaNeural; Mayor ChristopherNeural -14Hz"
---

## Intent
"Can you make a video starting the same but about a town in which every person is born with a clock that exactly tells when he gonna die"
Style reference: video-playbook/BLOCKY_STORY_STYLE.md (blocky toy-world story Shorts).

## Stated
- It opens the same way as the references: "In this town, every person is born with a clock..."
- The premise is a clock that tells exactly when you die.

## Inferred
- It follows the style guide's beat table: an impossible town rule, the hero's own clock in danger, a missing-time mystery, the villain (the mayor), the weakness (gears/lever), the rescue, and a twist sting.
- 720x1280, 30 fps, about 2:00, one yellow word per caption.
- Blocky characters with 2D faces are built in Three.js inside HyperFrames.
- The music bed and every sound effect are synthesized in `tools/make_audio.py` (no third-party audio).
