---
version: alpha
name: Pixel Venom — Frame (bespoke, sibling of Pixel Reef)
description: >
  Same pixel system as videos/octopus-camouflage-hunt/frame.md (180x320 art canvas upscaled 6x,
  360x640 caption overlay upscaled 3x, palette lock + 4x4 Bayer dither, pixel caption cards with
  dither-dissolve exit). New palettes: a desert at dusk outside, a blood vessel inside.
unit: the frame — 1080x1920 (9:16)
principle: one subject · dark low-contrast ground · ONE accent (venom green) · palette-locked + dither

canvas: "#120a1c"

colors:
  # desert dusk sky (dark to light)
  night: "#120a1c"
  dusk1: "#24123a"
  dusk2: "#3d1d4f"
  dusk3: "#6b2f5c"
  horizon: "#c4566a"
  sunset: "#f08a5d"
  moon: "#f6e6c4"
  # desert ground
  sandDark: "#4a2c2a"
  sand: "#8a5236"
  sandLight: "#c98a52"
  rock: "#5e3a3a"
  cactus: "#3f6b4a"
  cactusDark: "#24402f"
  # rattlesnake
  snakeDark: "#3a2a22"
  snake: "#8a6a44"
  snakeLight: "#d0b07a"
  fang: "#efe8dc"
  # hiker boot / skin cross-section
  boot: "#5a3b2a"
  bootLight: "#8a5f3f"
  skin: "#e0a080"
  dermis: "#c76a6a"
  fat: "#f0d08a"
  # bloodstream
  plasma: "#4a0d18"
  plasmaLight: "#7a1a26"
  vessel: "#a8344a"
  rbc: "#d8303a"
  rbcLight: "#ff6a60"
  # accents
  venom: "#7dff4a"
  venomDark: "#2f9a2a"
  antibody: "#bff4ff"
  # ui
  ink: "#06050a"
  paper: "#f1eef4"
  gold: "#ffd23f"

typography:
  font: "built-in 5x7 bitmap pixel font (same as Pixel Reef)"
  headline: { scale: 3 }
  sub: { scale: 2 }

components:
  caption-card: "same as Pixel Reef: ink box 92%, paper text, key number/word in gold, dither-dissolve exit"
  accent-rule: "venom green appears ONLY on venom (fang drip, venom particles); antibodies are pale cyan"
