# Builds index.html: shot list -> video/img clips, plus the hand-written graphics template.
import json, pathlib
P = pathlib.Path(__file__).resolve().parent.parent
TOTAL = 72.0
SRC = {"a1": "assets/ai/a1.mp4", "a2": "assets/ai/a2.mp4", "a3": "assets/ai/a3.mp4", "a4": "assets/ai/a4.mp4",
       "a5": "assets/ai/a5.mp4", "a6": "assets/ai/a6.mp4", "RB": "assets/real/blazer.mp4", "RS": "assets/real/store.mp4",
       "RJ": "assets/real/jacket.mp4", "RF": "assets/real/fleece.mp4", "W": "assets/real/reel.mp4",
       "I19": "assets/img/blazer.jpg", "I17": "assets/img/fleece.jpg", "PNG": "assets/img/storefront.png"}
# (start, end, src, media_in, move)   move: zin | zout | pan | none | crop (reel: hide its burned-in sticker)
SHOTS = [
    (0.00, 2.00, "a6", 0.05, "zin"),     # kids in winter uniform walking  - सर्दियाँ आ गई हैं
    (2.00, 4.15, "a2", 0.15, "zin"),     # mother puts cap on son          - school shopping की तैयारी
    (4.15, 5.30, "a6", 3.13, "zout"),    # kids walking                     - लेकिन इस बार winter uniform
    (5.30, 6.53, "a6", 5.17, "zin"),     # kids walking                     - इधर-उधर जाने की
    (6.53, 8.15, "a6", 6.42, "zin"),     # girl smiling in winter uniform   - ज़रूरत नहीं
    (8.15, 8.58, "RS", 5.60, "none"),    # REAL: shop front (under the burn)
    (8.58, 10.25, "RS", 6.00, "none"),   # REAL: shop sign + entrance        - क्योंकि NS Brothers   [BURN 1]
    (10.25, 12.75, "a4", 1.60, "zin"),   # presenter presents the shop       - लेकर आया है ... collection
    (12.75, 15.15, "GFX", 0, "none"),    # product photo collage            - यहाँ मिलेगा गर्म और stylish
    (15.15, 16.35, "RB", 1.20, "none"),  # REAL: DAV blazer                  - Blazers
    (16.35, 17.62, "RF", 2.60, "none"),  # REAL: fleece track top            - Fleece Tracksuits
    (17.62, 18.50, "RJ", 0.00, "none"),  # REAL: winter jacket               - Sweaters
    (18.50, 19.45, "a6", 2.13, "zin"),   # girl in pink winter cap           - Winter Caps
    (19.45, 20.55, "W", 20.40, "crop"),  # REAL: long uniform counter        - बेहतरीन कलेक्शन
    (20.55, 22.85, "RJ", 5.30, "none"),  # REAL: DAV on jacket back          - DAV School हो या अन्य स्कूल
    (22.85, 24.35, "RB", 3.00, "none"),  # REAL: blazer orbit                - winter uniform का शानदार कलेक्शन
    (24.35, 26.20, "W", 29.72, "crop"),  # REAL: customer at counter         - मिलेगा एक ही जगह
    (26.20, 27.50, "I19", 0, "zin"),     # REAL photo: blazer                - बेहतरीन Quality
    (27.50, 28.75, "I17", 0, "zout"),    # REAL photo: fleece                - Comfortable Fabric
    (28.75, 30.20, "RB", 5.00, "none"),  # REAL: blazer front                - Smart Look
    (30.20, 33.95, "a3", 4.00, "none"),  # presenter talking at the shop     - सबसे खास बात, location आसान [BURN 2]
    (33.95, 36.40, "PNG", 0, "zout"),    # REAL photo: storefront            - Chandauti More
    (36.40, 38.60, "a3", 0.00, "zin"),   # presenters outside the shop       - Military Hospital gate
    (38.60, 39.75, "W", 14.20, "crop"),  # REAL: shop exterior               - Medical College Road
    (39.75, 40.95, "W", 15.35, "crop"),  # REAL: the road outside            - Sikaria More के पास
    (40.95, 47.10, "a1", 0.00, "none"),  # family leaving with bags (+map)   - Bodh Gaya, Cherki ...
    (47.10, 50.40, "W", 39.30, "crop"),  # REAL: billing at counter          - shopping को बनाइए आसान [BURN 3]
    (50.40, 51.50, "W", 25.27, "crop"),  # REAL: shop interior               - आज ही विजिट करें
    (51.50, 52.60, "W", 21.56, "crop"),  # REAL: shop interior               - NS Brothers
    (52.60, 55.00, "RS", 7.65, "none"),  # REAL: entrance close              - Chandauti More, Gaya / Near PNB
    (55.00, 57.75, "PNG", 0, "zin"),     # REAL photo: storefront            - Chandauti More, Gaya
    (57.75, 61.70, "RF", 0.00, "dim"),   # REAL behind phone card            - phone 1
    (61.70, 65.60, "RJ", 1.40, "dim"),   # REAL behind phone card            - phone 2
    (65.60, 69.20, "a5", 0.00, "none"),  # presenters thumbs up              - Quality, Style, Trust [BURN 4]
    (69.20, 72.00, "OUTRO", 0, "none"),  # logo outro                        - Fashion for Every Generation
]
BURNS = [8.58, 30.2, 47.1, 65.6]

clips, cam = [], []
for k, (s, e, src, mi, mv) in enumerate(SHOTS, 1):
    d = round(e - s, 3); w = f"w{k}"
    if src in ("GFX", "OUTRO"):
        continue
    if src.startswith("I") or src == "PNG":
        el = f'<img id="m{k}" src="{SRC[src]}" alt="" data-start="{s}" data-duration="{d}" data-track-index="0" />'
    else:
        el = f'<video id="m{k}" src="{SRC[src]}" muted playsinline data-start="{s}" data-duration="{d}" data-media-start="{mi}" data-track-index="0"></video>'
    cls = "vw crop" if mv == "crop" else "vw"
    clips.append(f'      <div class="{cls}" id="{w}">{el}</div>')
    if mv == "zin":
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {d}, ease: "none" }}, {s});')
    elif mv == "zout":
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.14 }}, {{ scale: 1.0, duration: {d}, ease: "none" }}, {s});')
    elif mv == "crop":
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.6 }}, {{ scale: 1.7, duration: {d}, ease: "none" }}, {s});')
    elif mv == "dim":
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.08 }}, {{ scale: 1.16, duration: {d}, ease: "none" }}, {s});')
    else:
        cam.append(f'      tl.fromTo("#{w}", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {d}, ease: "none" }}, {s});')

tpl = (P / "tools" / "template.html").read_text()
html = (tpl.replace("<!--CLIPS-->", "\n".join(clips))
           .replace("//CAMERA", "\n".join(cam))
           .replace("__BURNS__", json.dumps(BURNS))
           .replace("__TOTAL__", str(TOTAL)))
(P / "index.html").write_text(html)
print(len(clips), "clips")
