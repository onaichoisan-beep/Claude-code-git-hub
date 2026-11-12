"""compositions/captions.html: one word at a time (reference style), timed from tools/words.json."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "tools", "words.json")))
words = []
i = 0
while i < len(W):
    w, a, b = W[i]
    if w.lower() == "hour" and i + 1 < len(W) and W[i + 1][0].lower().startswith("glass"):
        w, b = "hour" + W[i + 1][0], W[i + 1][2]
        i += 1
    words.append([re.sub(r"[^\w'%-]", "", w), a, b])
    i += 1
EMPH = set("die leo one day never wrong mia two three week strange rang mayor 900 thousands empty giant suddenly slammed shadows up beeping ten nine eight gears lever everything stop flipped golden jumped 75 screamed backwards cracked sand back blank nothing born".split())
END = 121.9
divs, tw = [], []
for n, (w, a, b) in enumerate(words):
    nxt = words[n + 1][1] if n + 1 < len(words) else END
    end = min(nxt, max(b + 0.35, a + 0.25)) if nxt - b > 0.6 else nxt
    if n == len(words) - 1:
        end = min(END, b + 1.0)
    big = w.lower() in EMPH
    divs.append(f'    <div id="cap-{n}" class="cap clip" data-start="{a:.3f}" data-duration="{end - a:.3f}"><span id="cap-{n}-t" class="{"big" if big else ""}">{w}</span></div>')
    tw.append(f'      tl.fromTo("#cap-{n}-t", {{ scale: 0.45 }}, {{ scale: 1, duration: 0.12, ease: "back.out(2.5)" }}, {a:.3f});')
html = f'''<template>
  <style>
    @font-face {{ font-family: "Fredoka"; src: url("assets/fonts/fredoka-700.woff2") format("woff2"); font-weight: 700; }}
    #captions-root {{ position: absolute; inset: 0; pointer-events: none; font-family: "Fredoka", sans-serif; }}
    .cap {{ position: absolute; left: 0; width: 100%; top: 1010px; height: 110px; display: flex; align-items: center; justify-content: center; }}
    .cap span {{ display: inline-block; color: #e8ff1a; font-weight: 700; font-size: 62px; line-height: 1; white-space: nowrap; -webkit-text-stroke: 11px #000; paint-order: stroke fill; text-shadow: 0 5px 0 rgba(0, 0, 0, 0.55), 0 8px 18px rgba(0, 0, 0, 0.5); }}
    .cap span.big {{ font-size: 74px; }}
  </style>
  <div id="captions-root" data-composition-id="captions" data-width="720" data-height="1280">
{chr(10).join(divs)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tw)}
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
'''
open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(html)
print(len(words), "caption words")
