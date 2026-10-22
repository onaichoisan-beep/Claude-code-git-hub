---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Lightning can stop your heart — but 9 in 10 people survive, especially with fast CPR."
destination: shorts
aspect: 1080x1920
language: en
length: 30s
angle: narrative
---

## Intent

Bright pixel-art science short in the user's established style (see videos/snake-bite-venom):
one continuous camera journey, only key facts as small text in the middle, sound effects only
(no narration, no text sounds), complete story start to finish, looping ending. Built autonomously.

Story: field in a storm → strike (300 million volts, ~5x hotter than the sun's surface) →
current flashes over the skin → fern-shaped Lichtenberg marks → heart stops (flatline) →
restarts on its own (pacemaker spark) → victims are safe to touch: start CPR → 9 in 10 survive →
"Thunder? Go indoors." → loop.

## Notes

- Facts per US National Weather Service: ~90% of strike victims survive; victims carry no charge and
  are safe to touch; cardiac arrest is the main cause of death and the heart may restart on its own,
  but breathing may not, so CPR matters. Lightning ~30,000 K vs the sun's ~5,800 K surface.
- Engine: pixel-engine.js (shared copy of videos/_engine/pixel-engine.js); audio: scripts/synth_audio.py + sfxlib.py.
