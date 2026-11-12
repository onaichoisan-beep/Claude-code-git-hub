# Clock Town (blocky story Short)

A 2:02 vertical story in the style of `video-playbook/BLOCKY_STORY_STYLE.md`.

## How it is built
| Step | File / command |
|---|---|
| Script (speaker, line) | `SCRIPT.json` (plain text in `SCRIPT.txt`) |
| Voice, one TTS voice per character | `python tools/make_vo.py SCRIPT.json <outdir>`, then copy `vo.wav` to `assets/audio/` |
| Word timings | `python tools/words.py assets/audio/vo.wav > tools/words.json` (faster-whisper) |
| Captions | `python tools/make_captions.py` writes `compositions/captions.html` |
| Music bed + SFX (synthesized) | `python tools/make_audio.py` writes `assets/audio/music.wav`, `assets/sfx/`, `tools/sfx.json` |
| Scenes | edit `tools/scenes/sN.js`, then `python tools/mkscene.py sN <start> <end>` |
| Timeline | `python tools/build_index.py` writes `index.html` |
| Check / look / render | `npm run check`, `npx hyperframes snapshot --at 1,5,9`, `npm run render` |

`assets/js/blocky.js` is the reusable kit. It has:
- rounded-box characters with swappable 2D face textures (smile, happy, shock, worried, cry, angry, sly, grin, scream, eerie and more)
- a cast of presets
- floating number holograms
- the town, clock tower, bedroom and tower interior
- hourglasses, gears and glowing particle streams
- bloom and tone mapping

Python steps need `faster-whisper`, `edge-tts`, `numpy`, `scipy` and `soundfile`.
