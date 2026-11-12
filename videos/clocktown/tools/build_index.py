"""Write index.html: scene clips, captions, voice, music bed and sound effects.
Scenes and SFX are listed here so timing lives in one place."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENES = [  # id, start, end
    ("s1", 0.0, 8.93), ("s2", 8.93, 19.2), ("s3", 19.2, 31.3), ("s4", 31.3, 41.9),
    ("s5", 41.9, 60.6), ("s6", 60.6, 76.15), ("s7", 76.15, 91.2), ("s8", 91.2, 102.8), ("s9", 102.8, 122.0),
]
TOTAL = 122.0
only = os.environ.get("ONLY")  # e.g. ONLY=s1 for a quick test build
sfx = json.load(open(os.path.join(ROOT, "tools", "sfx.json"))) if os.path.exists(os.path.join(ROOT, "tools", "sfx.json")) else []
out = []
for sid, a, b in SCENES:
    if only and sid not in only.split(","):
        continue
    out.append(f'      <div id="{sid}" class="clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
               f'data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="1" data-width="720" data-height="1280"></div>')
cap = "" if only else ('      <div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" '
       f'data-start="0" data-duration="{TOTAL}" data-track-index="5" data-width="720" data-height="1280" style="z-index: 20"></div>')
aud = ['      <audio id="vo" class="clip" src="assets/audio/vo.wav" data-start="0" data-duration="120.34" data-track-index="10" data-volume="1"></audio>']
if os.path.exists(os.path.join(ROOT, "assets/audio/music.wav")):
    aud.append(f'      <audio id="music" class="clip" src="assets/audio/music.wav" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="1"></audio>')
for i, s in enumerate(sfx):
    aud.append(f'      <audio id="sfx-{i:02d}" class="clip" src="assets/sfx/{s["f"]}.wav" data-start="{s["t"]}" data-duration="{s["d"]}" '
               f'data-track-index="{12 + i % 4}" data-volume="{s.get("v", 0.5)}"></audio>')
total = TOTAL if not only else max(b for sid, a, b in SCENES if sid in only.split(","))
html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=720, height=1280" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script src="assets/js/three.min.js"></script>
    <script src="assets/js/three-bloom.js"></script>
    <script src="assets/js/blocky.js"></script>
    <style>
      @font-face {{ font-family: "Fredoka"; src: url("assets/fonts/fredoka-700.woff2") format("woff2"); font-weight: 700; }}
      @font-face {{ font-family: "Fredoka"; src: url("assets/fonts/fredoka-600.woff2") format("woff2"); font-weight: 600; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 720px; height: 1280px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Fredoka", sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="720" data-height="1280">
{chr(10).join(out)}
{cap}
{chr(10).join(aud)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(html)
print("index.html:", len(out), "scenes,", len(sfx), "sfx, total", total)
