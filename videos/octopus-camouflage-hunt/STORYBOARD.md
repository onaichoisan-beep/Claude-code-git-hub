---
format: 1080x1920
duration: 30s
message: "An octopus can become the reef in an instant — without even seeing colour."
arc: Hook → Stalk → Mechanism (colour) → Mechanism (texture) → Strike → Twist → Loop
audience: curious Shorts/TikTok viewers
mode: collaborative
music: none
build: single continuous-take composition (one shared pixel world + camera); see Notes
---

## Frame 1 — Where is it?

- scene: Wide reef at dusk-teal; sand, coral, kelp, a mossy "rock". Caption WHERE IS THE / OCTOPUS? + 🎧
- duration: 4s
- poster: 2s
- transition_in: cut
- status: outline
- voiceover: ""
- camera: wide, slow drift right
- sfx: underwater ambience bed (whole video)

Hook as a question over an empty-looking reef. The octopus is already on screen, camouflaged as the rock on the right. A sharp-eyed viewer can spot one eye pixel blink at ~3s.

## Frame 2 — Something is watching

- scene: A crab scuttles in from the left along the sand. The rock's slit eye opens. Caption SOMETHING / IS WATCHING
- duration: 4.5s
- poster: 7s
- transition_in: camera push-in (continuous)
- status: outline
- voiceover: ""
- camera: push in and pan toward the rock, keeping the crab and rock in frame
- sfx: crab clicks

Stakes: prey and predator in one frame. The open eye is the first hint that the rock is alive.

## Frame 3 — Colour cells

- scene: Macro dive into the rock's skin. It's a grid of pigment sacs (chromatophores) stretching open and closed, colour waves ripple across. Caption SKIN WITH / ~10,000 / COLOUR CELLS (number in gold)
- duration: 5s
- poster: 11s
- transition_in: camera macro zoom (continuous)
- status: outline
- voiceover: ""
- camera: deep zoom onto the octopus's mantle until cells fill the frame
- sfx: soft bubbly pops as cells flex

Mechanism 1, like the Morpho wing-scale zoom. Each sac is a dot of pigment ringed by muscle; stretching it shows colour.

## Frame 4 — Texture

- scene: Still close, camera tilts to the skin's edge in profile; bumps (papillae) rise into spikes and lumps that match the rock. Caption IT CHANGES / TEXTURE TOO
- duration: 4s
- poster: 15s
- transition_in: camera pull-back to profile (continuous)
- status: outline
- voiceover: ""
- camera: partial pull-back, horizon of skin against water
- sfx: low creak

Mechanism 2. Colour alone isn't enough; the outline breaks up too.

## Frame 5 — Strike

- scene: Pull back to medium. The crab steps beside the rock. FLASH: the rock turns orange-red, eight arms unfurl and wrap the crab. Caption IN UNDER / 0.2 SECONDS (gold)
- duration: 4.5s
- poster: 19.5s
- transition_in: camera pull-back + impact shake (continuous)
- status: outline
- voiceover: ""
- camera: medium two-shot, 3-frame shake on the strike
- sfx: whoosh + snap on the strike

The payoff of the hunt. The reveal colour is the video's accent, used here for the first time at full strength.

## Frame 6 — Twist

- scene: The octopus holds the crab, then fades from red back to rock-grey as we watch. Caption AND IT'S / COLOURBLIND
- duration: 4.5s
- poster: 23.5s
- transition_in: continuous hold
- status: outline
- voiceover: ""
- camera: slow push-in on the octopus eye
- sfx: single low tone

The counter-intuitive fact. It matches colours it can't see, which keeps viewers watching to the end.

## Frame 7 — Loop

- scene: Pull back to the exact opening wide shot. The reef is empty again, the octopus is a rock, the crab is gone. The opening caption pops back on for the loop seam.
- duration: 3.5s
- poster: 28.5s
- transition_in: camera pull-back to the opening framing (continuous)
- status: outline
- voiceover: ""
- camera: return to frame 1 framing
- sfx: bubbles

The last frame matches the first, so the replay is seamless.

## Notes

- Built as ONE composition: a 180x320 pixel world drawn per frame on a canvas from a GSAP proxy (deterministic, seeded), palette-locked with Bayer dither, scaled 6x; captions on a 360x640 overlay canvas. Frames above are camera beats in one take, not separate sub-compositions, so the per-frame worker dispatch and transition injection are replaced by a single build.
- Placeholder creator tag "@YOURHANDLE" is carved small into a foreground rock (visible in frames 1, 2, 7).
