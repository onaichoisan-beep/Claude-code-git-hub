"""Intro trailer: snippets from the clips, stitched with chapter flashes. Writes plans/intro.json.
No proof photos/logos here — those stay inside clips 01/02 as requested."""
import json

V = lambda n: f"assets/video/clip{n}.mp4"
W = lambda n: f"../work/base/clip{n}.words.json"
M = lambda n, m: f"assets/mattes/clip{n}_{m}.webm"

segs = [
    dict(name="hook", n="06", a=0.0, b=3.05),     # I made around 80000 rupees in my first year mbbs
    dict(name="ways", n="08", a=9.15, b=10.5),    # you 4 easy ways
    dict(name="w1", n="01", a=2.2, b=5.35),       # this alone has generated me over 60k of revenue
    dict(name="w2", n="02", a=11.1, b=16.0),      # at just 800 subs i locked my first paid collaboration
    dict(name="w3", n="03", a=13.3, b=16.6),      # you are selling your knowledge jo ki already tumhare pass h
    dict(name="w4", n="04", a=5.9, b=9.1),        # roughly charges around 3-4k per videos
    dict(name="end", n="10", a=15.5, b=18.75),    # more skill, more money, better skill, more money
]
at, t = {}, 0.0
for s in segs:
    at[s["name"]] = t
    t += s["b"] - s["a"]
TAIL = 2.0
dur = t + TAIL

def bh(seg, n, m, src_t, d, text, style):
    """Behind-head text whose matte was cut at src_t in clip n."""
    s = next(x for x in segs if x["name"] == seg)
    return dict(type="bh", t=round(at[seg] + src_t - s["a"], 3), d=d, text=text, style=style, matteFile=M(n, m))

cues = [
    dict(type="flash", t=0.0),
    bh("hook", "06", "a", 0.85, 1.55, "80,000", "money"),
    dict(type="pop", t=2.45, d=0.6, x=380, y=400, icon="steth", label="1ST YEAR MBBS", tile="red"),
    dict(type="title", t=at["ways"], d=1.35, kicker="as a student", line1="4 WAYS", line2="to earn money", line3="all trusted · all easy"),

    dict(type="chapter", t=at["w1"], d=0.8, num="01", title="UGC Content Creation"),
    bh("w1", "01", "a", 3.8, 1.35, "₹60K+", "money"),

    dict(type="chapter", t=at["w2"], d=0.8, num="02", title="Content Creation"),
    dict(type="bh", t=round(at["w2"] + 0.85, 3), d=1.15, mediaStart=0.45, text="800 SUBS", style="white", matteFile=M("02", "a")),
    dict(type="note", t=at["w2"] + 3.2, d=1.6, x=1180, y=250, text="first paid collab!", color="money", arrow="left"),

    dict(type="chapter", t=at["w3"], d=0.8, num="03", title="Online Tutoring"),
    bh("w3", "03", "a", 14.15, 1.6, "KNOWLEDGE", "chrome"),

    dict(type="chapter", t=at["w4"], d=0.8, num="04", title="Freelancing"),
    dict(type="timeline", t=at["w4"] + 1.0, d=2.2, big="₹3–4K", small="per video"),

    dict(type="glitch", t=at["end"] - 0.05),
    bh("end", "10", "a", 15.55, 0.95, "MORE SKILL", "white"),
    bh("end", "10", "b", 16.5, 0.95, "MORE MONEY", "money"),
    bh("end", "10", "c", 17.45, 0.85, "BETTER SKILL", "chrome"),
    dict(type="sfx", t=dur - TAIL - 1.2, name="riser", vol=0.3, dur=1.2),
    dict(type="title", t=dur - TAIL, d=TAIL, kicker="watch till the end", line1="4 WAYS", line2="to earn as a student", line3="from a 1st-year MBBS student", out=False),
]
zoom = [[at[s["name"]], z] for s, z in zip(segs, [1.0, 1.0, 1.16, 1.0, 1.2, 1.0, 1.12])]
zoom += [[1.6, 1.18], [at["w2"] + 3.2, 1.22], [at["end"] + 1.0, 1.2], [at["end"] + 1.95, 1.3]]

plan = dict(id="intro", duration=round(dur, 3), zoom=sorted(zoom),
            keys={"80000": "money", "4": "red", "800": "money", "knowledge": "red", "-4k": "money"},
            fix={"80000": "₹80,000", "-4k": "₹3–4K", "3": ""},
            segments=[dict(video=V(s["n"]), words=W(s["n"]), **{"from": s["a"], "to": s["b"]}) for s in segs],
            cues=cues)
json.dump(plan, open("plans/intro.json", "w"), indent=1, ensure_ascii=False)
print("intro", round(dur, 2), "s;", {k: round(v, 2) for k, v in at.items()})
