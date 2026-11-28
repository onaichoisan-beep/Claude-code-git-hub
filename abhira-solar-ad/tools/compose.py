# Builds index.html from the shot list + template. Times are voiceover times (seconds).
import json, pathlib
P = pathlib.Path(__file__).resolve().parent.parent
OFFSET = 1.2   # cold open (AC shot + rising music) before the voiceover starts
TOTAL = round(83.4 + OFFSET, 2)
SYNC = {k: v for k, v in json.load(open(P / "tools/sync_report.json")).items()}
SRC = {
    "S1": "assets/ai/S1_a3_synced.mp4", "S2": "assets/ai/S2_a4_synced.mp4", "S3": "assets/ai/S3_a2_synced.mp4",
    "S4": "assets/ai/S4_a1_synced.mp4", "S5": "assets/ai/S5_a8_synced.mp4", "S9": "assets/ai/S9_a9_synced.mp4",
    "S10": "assets/ai/S10_a11_synced.mp4", "a3": "assets/ai/a3.mp4", "OPEN": "assets/ai/a12_open.mp4",
    "a5": "assets/ai/a5.mp4", "a6": "assets/ai/a6.mp4", "a7": "assets/ai/a7.mp4", "a10": "assets/ai/a10.mp4", "a11": "assets/ai/a11.mp4",
    "r26": "assets/real/r26.mp4", "r27": "assets/real/r27.mp4", "r29": "assets/baked/r29_fill.mp4", "r32": "assets/baked/r32_inv.mp4",
    "p20": "assets/baked/p20_fill.mp4", "p23": "assets/baked/p23_fill.mp4", "INV": "assets/img/inverter.jpg",
}
# (start, end, src, media_in, move)
#   Sx sources are anchor clips already warped to the VO: media_in = start - line VO start (lips stay in sync).
#   move: zin | zout | none | fill (letterboxed/landscape -> blurred fill behind) | punch
SHOTS = [
    (2.62, 3.30, "a3", 2.95, "punch"),   # AI: man shocked at the bill                    - अब बिजली बिल की
    (3.30, 4.48, "S2", None, "none"),    # ANCHORS (lip-sync)                            - टेंशन छोड़िए
    (4.48, 5.60, "r27", 3.40, "none"),   # REAL: rooftop panel rows                      - और अपने घर की छत पर
    (5.60, 6.48, "S2", None, "punch"),   # ANCHORS (lip-sync)                            - लगवाइए
    (6.48, 7.60, "r27", 0.20, "zin"),    # REAL: rooftop panels                          - Solar Panel!
    (7.60, 9.10, "r27", 6.60, "zout"),   # REAL: panels + big logo reveal  [BURN 1]      - ABHIRA GREEN ENERGY
    (9.10, 10.99, "p23", 0, "fill"),     # REAL photo: team installing                   - लेकर आया है आपके लिए
    (10.99, 12.19, "S3", None, "none"),  # ANCHORS (lip-sync)                            - PM सूर्य घर योजना के तहत
    (12.19, 13.79, "r29", 1.00, "fill"), # REAL: installation under panels               - ₹78,000 तक की
    (13.79, 15.40, "S3", None, "punch"), # ANCHORS (lip-sync)                            - केंद्रीय सब्सिडी
    (15.40, 16.60, "S4", None, "none"),  # ANCHOR close-up (lip-sync)                     - और बिहार सरकार की
    (16.60, 18.60, "r27", 10.20, "none"),# REAL: under the panels                        - ₹20,000 तक की अतिरिक्त सब्सिडी
    (18.60, 20.20, "r27", 3.00, "zin"),  # REAL: panel close sweep                       - का लाभ, यानी कुल
    (20.20, 22.20, "GFX", 0, "none"),    # full-screen ₹98,000 slam                      - ₹98,000 तक की सब्सिडी
    (22.20, 24.75, "a10", 0.00, "zin"),  # AI: sunset over solar rooftops                - पाने का शानदार मौका
    (24.75, 28.51, "GFX2", 0, "none"),   # full-screen deadline card   [BURN 2]          - ध्यान दीजिए… 31 मार्च तक
    (28.51, 32.48, "S5", None, "none"),  # ANCHORS (lip-sync)                            - इसलिए देर न करें, आज ही booking
    (32.48, 35.00, "r29", 4.00, "fill"), # REAL: installation team                       - और इस शानदार मौके का लाभ उठाइए
    (35.00, 36.90, "r32", 0.20, "none"), # REAL: on-grid inverter on wall  [BURN 3]      - यहाँ उपलब्ध हैं On-Grid
    (36.90, 38.00, "a7", 6.10, "zin"),   # AI: battery unit                              - Off-Grid और Hybrid
    (38.00, 39.60, "INV", 0, "zin"),     # REAL photo: Microtek inverter                 - Solar Systems, 1 KW
    (39.60, 42.00, "a7", 0.10, "none"),  # AI: aerial of homes with solar                - से 10 KW+ तक के विकल्प
    (42.00, 44.10, "r29", 6.00, "fill"), # REAL: installers at work                      - Adani, Tata, Waaree
    (44.10, 45.60, "p20", 0, "fill"),    # REAL photo: mounting structure               - Luminous, Microtek
    (45.60, 47.40, "a6", 1.00, "none"),  # AI: installer tightening clamps               - जैसे Top Brands के साथ
    (47.40, 48.50, "r27", 21.50, "none"),# REAL: panel underside / wiring                - बेहतर Quality
    (48.50, 49.75, "a6", 7.00, "none"),  # AI: installer thumbs-up                       - भरोसेमंद Service
    (49.75, 51.00, "r27", 1.50, "zin"),  # REAL: panels                                  - Solar लगवाइए
    (51.00, 52.80, "a5", 0.40, "none"),  # AI: happy family                              - बिजली बिल में बचत
    (52.80, 54.00, "r27", 22.70, "none"),# REAL: clean structure                         - कम Maintenance
    (54.00, 56.13, "a5", 3.10, "zin"),   # AI: panels in sunlight                        - लंबे समय तक फायदा
    (56.13, 59.73, "S9", None, "none"),  # ANCHORS (lip-sync)  [BURN 4]                   - तो देर किस बात की! 31 मार्च से पहले Solar अपनाइए
    (59.73, 61.20, "r27", 7.00, "none"), # REAL: home rooftop with panels                - और अपने घर को बनाइए
    (61.20, 62.84, "a10", 3.20, "none"), # AI: sunset rooftops                           - Energy Independent
    (62.84, 64.44, "S10", None, "none"), # ANCHOR pointing (lip-sync)                    - अभी कॉल करें ABHIRA
    (64.44, 67.40, "a11", 5.10, "none"), # anchors smiling behind phone card             - Green Energy पर / 8809…
    (67.40, 69.77, "r27", 13.40, "zin"), # REAL: panels behind phone card                - …215769
    (69.77, 72.04, "p20", 0, "fill"),    # REAL photo (Patna rooftop)                    - 101, Karai Bhawan
    (72.04, 74.50, "r29", 70.20, "fill"),# REAL: inverters on wall                       - Gali No. 01, Chandmani Road
    (74.50, 76.50, "r27", 18.30, "none"),# REAL: city view                               - Kankarbagh, Patna
    (76.50, 78.70, "a10", 5.30, "none"), # AI: sunset                                    - 800020
    (78.70, 83.40, "OUTRO", 0, "none"),  # logo + tagline                                - ABHIRA GREEN ENERGY, Powering a Sustainable Tomorrow
]
BURNS = [7.6, 24.75, 35.0, 56.0]
LINE_V0 = {k: v["vo"][0] for k, v in SYNC.items()}

clips, cam = [], []
for k, (s, e, src, mi, mv) in enumerate(SHOTS, 1):
    d = round(e - s, 3); w = f"w{k}"
    if src in ("GFX", "GFX2", "OUTRO"):
        continue
    if src.startswith("S"):
        mi = round(s - LINE_V0[src], 3)
    path = SRC[src]; img = path.endswith((".jpg", ".png"))
    def el(idx, extra=""):
        if img:
            return f'<img id="m{k}{idx}" src="{path}" alt="" data-start="{round(s+OFFSET,3)}" data-duration="{d}" data-track-index="0"{extra} />'
        return f'<video id="m{k}{idx}" src="{path}" muted playsinline data-start="{round(s+OFFSET,3)}" data-duration="{d}" data-media-start="{mi}" data-track-index="0"{extra}></video>'
    if mv == "fill":  # baked blurred-fill source -> plain clip with a slow push
        mi = 0 if mi is None else mi
        mv = "zin"
    if False:
        clips.append(f'      <div class="vw fill" id="{w}"><div class="bgb">{el("b")}</div><div class="fg">{el("")}</div></div>')
    else:
        clips.append(f'      <div class="vw" id="{w}">{el("")}</div>')
    if mv == "zin":
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {d}, ease: "none" }}, {s});')
    elif mv == "zout":
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.14 }}, {{ scale: 1.0, duration: {d}, ease: "none" }}, {s});')
    elif mv == "punch":
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.16 }}, {{ scale: 1.2, duration: {d}, ease: "none" }}, {s});')
    elif mv == "fill":
        cam.append(f'      tl.fromTo("#{w} .fg", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {d}, ease: "none" }}, {s});')
    else:
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {d}, ease: "none" }}, {s});')

# opener (new first clip): global 0 -> OFFSET+2.62, AC cold open then bill + meter synced to line 1
clips.insert(0, f'      <div class="vw" id="w0"><video id="m0" src="{SRC['OPEN']}" muted playsinline data-start="0" data-duration="{round(OFFSET+2.62,3)}" data-media-start="0" data-track-index="0"></video></div>')
tpl = (P / "tools" / "template.html").read_text()
html = (tpl.replace("<!--CLIPS-->", "\n".join(clips)).replace("//CAMERA", "\n".join(cam))
           .replace("__BURNS__", json.dumps(BURNS)).replace("__TOTAL__", str(TOTAL)).replace("__OFFSET__", str(OFFSET)))
(P / "index.html").write_text(html)
print(len(clips), "clips")
