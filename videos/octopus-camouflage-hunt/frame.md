---
version: alpha
name: Pixel Reef — Frame (bespoke, from pixel-explainer-style.md)
description: >
  Bespoke spec derived from the @BITWONDER-style reference analysis (capture/extracted/style-reference.md).
  No shipped preset fits pixel art. The world is a 180x320 art canvas upscaled 6x to 1080x1920 with
  nearest-neighbour; captions live on a 360x640 overlay canvas upscaled 3x (text strokes half an art pixel).
unit: the frame — 1080x1920 (9:16)
principle: one subject · dark low-contrast ground · one accent · palette-locked + Bayer dither on gradients

canvas: "#04121a"

colors:
  # deep water (dark to light)
  abyss: "#04121a"
  deep: "#06202b"
  water-1: "#0a2f3c"
  water-2: "#0e4250"
  water-3: "#145a66"
  water-4: "#1d7a80"
  shaft: "#3fa6a0"
  glow: "#8fd9c8"
  # sand / rock
  sand-dark: "#3a3a33"
  sand: "#6d6650"
  sand-light: "#a39a74"
  rock-dark: "#2b3436"
  rock: "#4a5654"
  rock-light: "#6f7d76"
  moss: "#3f6a4a"
  # reef
  coral-deep: "#7a2f4c"
  coral: "#d9607a"
  coral-light: "#f29aa6"
  anemone: "#f2c46d"
  kelp: "#2f6b3f"
  # octopus accent
  octo-dark: "#7a1f1a"
  octo: "#d8462b"
  octo-light: "#ff8a4a"
  # crab
  crab: "#e0703a"
  crab-dark: "#8a3a22"
  # ui
  ink: "#06050a"
  paper: "#f1eef4"
  gold: "#ffd23f"

typography:
  font: "built-in 5x7 bitmap pixel font, ALL CAPS, drawn on the overlay canvas (no web font)"
  headline: { scale: 3, overlayPx: 18, lineHeightPx: 26, maxChars: 12 }
  sub: { scale: 2, overlayPx: 12, lineHeightPx: 18, maxChars: 18 }

components:
  caption-card:
    box: "solid {colors.ink} at 92% opacity, 3 overlay-px padding, square corners, no border"
    text: "{colors.paper}; key number in {colors.gold}"
    position: "upper third, centred, top edge at overlay y≈34 (≈5% of height)"
    enter: "pop on in one frame"
    exit: "dither-dissolve — Bayer-ordered dots drop out over 0.4s"
  hero: "subject outlined 1 art-px darker, 3–4 tone shading, white specular pixels"
  atmosphere: "posterized halo rings + light shafts + bokeh + drifting particles; nothing ever still"
