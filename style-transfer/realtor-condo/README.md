# Realtor condo reel: style transfer (Edita method)

- Reference: brandbuddiestudio reel (25.2 s, Hinglish). A-roll: client realtor, 29.5 s, English.
- `spec/`: measurements of the reference (CUTS, S01-S10, STYLE, AUDIO) + the measuring scripts.
- `web/builder.tpl.html`: the Reel Style Builder engine (11 beats x 3 designs); `tools/build_page.py` injects words + face boxes into `web/index.html`.
- Media (A-roll stack video with matte, SFX) is not committed. Rebuild it with `tools/matte.py` (rembg u2net_human_seg) and the ffmpeg vstack command in the session notes.
- Published builder: https://claude.ai/artifact/N1ubywaEwtV1mAVSBPtrbe
