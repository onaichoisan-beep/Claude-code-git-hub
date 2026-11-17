# Magadh Panthor Cricket Club – Chhath special offer reel (50.6s, 1080x1920)

- `build.py`: the edit decision list (EDL, with every clip's source, in-point and why it was picked), then segment render → FX pass (white flash, soft film burn, logo top-right, address card) → audio mix (VO + ducked BGM + whooshes) → mux.
- `bgm_sports.py`: v2 sports-anthem BGM (stadium stomp-clap, drums, power chords, brass, crowd). `bgm.py`: v1 dhol BGM, still used for the whoosh SFX.
- v2 changes: transitions only on 5 section changes, Hindi captions (Mukta font), red "आज ही कॉल करें | 97982 70035" banner for the whole video, shirtless hostel shot replaced.
- `logo.png`: the club badge cut out of the client's PNG, which had the checkerboard baked in.
- Sources (not committed): real footage comes from the client Drive folder (renamed R01–R13 in download order), the AI clips are A1–A4, and the voiceover is the ElevenLabs "Bunty" mp3.
- To rebuild, put `real/`, `ai/`, `vo.mp3`, the fonts and the BGM wavs next to the scripts, then run `python3 bgm.py 50.6 && python3 build.py`.
