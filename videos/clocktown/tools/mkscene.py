"""Wrap tools/scenes/<id>.js into compositions/<id>.html (a templated sub-composition).
The JS body gets CV (canvas), T0 (scene start, global seconds), D (duration) and must define render(t)
taking global time. Usage: python mkscene.py s2 8.93 19.2 [s3 19.2 31.3 ...]"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
for i in range(0, len(args), 3):
    sid, a, b = args[i], float(args[i + 1]), float(args[i + 2])
    body = open(os.path.join(ROOT, "tools", "scenes", sid + ".js")).read()
    body = "\n".join("        " + l if l.strip() else "" for l in body.splitlines())
    html = f'''<template>
  <style>
    #{sid}-root {{ position: absolute; inset: 0; overflow: hidden; background: #000; }}
    #{sid}-root canvas {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; }}
  </style>
  <div id="{sid}-root" data-composition-id="{sid}" data-width="720" data-height="1280">
    <canvas id="{sid}-cv"></canvas>
  </div>
  <script>
    (function () {{
      const B = Blocky, T = THREE, T0 = {a}, D = {round(b - a, 3)};
      const CV = document.getElementById("{sid}-cv");
      document.fonts.load("700 40px Fredoka").then(() => {{
{body}
        const st = {{ t: 0 }};
        const tl = gsap.timeline({{ paused: true }});
        tl.to(st, {{ t: D, duration: D, ease: "none", onUpdate: () => render(T0 + st.t) }}, 0);
        render(T0);
        window.__timelines["{sid}"] = tl;
      }});
    }})();
  </script>
</template>
'''
    open(os.path.join(ROOT, "compositions", sid + ".html"), "w").write(html)
    print("wrote", sid)
