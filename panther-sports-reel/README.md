# Panther Sports India – counselling reel

75 s vertical (1080x1920) promo with a Hindi VO. Renders (`*.mp4`, v2 is current) are gitignored because it is ~105 MB, over GitHub's file limit.

- `scripts/edl.py`: the shot list as (timeline in/out, source clip, source in-point, framing mode). R## = real clips from the client Drive folder, A## = AI clips.
- `scripts/base.py`: cuts and frames every shot, then concatenates them into `base.mp4`.
- `scripts/fx.py`: film-burn and light-leak layer, screen-blended over `base.mp4` to make `base_fx.mp4`. Zoom punches and RGB glitches are applied per shot in `base.py`. Transition times are in `edl.py`.
- `scripts/music.py`: synthesizes the original BGM (`bgm.wav`).
- `scripts/overlay.py`: draws the logo, Hindi captions (Mukta ExtraBold, red box), the title card and the flashes. Pipe its output into ffmpeg over `base_fx.mp4`.
- Final mix: VO loudnorm to -15 LUFS, BGM -4 dB with sidechain ducking, alimiter.
- `logo_badge.png`: the Magadh Panthor badge cut out of its checkered background.
