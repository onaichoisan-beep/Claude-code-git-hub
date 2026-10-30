"""Generate a standalone HyperFrames composition per clip from plans/<id>.json.

usage: python kit/build.py plans/clip06.json [...]   (run from the edit/ project dir)
"""
import html, json, math, os, re, sys

KIT = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(KIT, "kit.css")).read()
FONTS = open(os.path.join(KIT, "fonts.css")).read().replace("../assets/", "assets/")
ICONS = json.load(open(os.path.join(KIT, "icons.json")))
WAYS = [("01", "UGC Content Creation", "₹60K+ EARNED"), ("02", "Content Creation", "PAID BRAND DEALS"),
        ("03", "Online Tutoring", "ZERO INVESTMENT"), ("04", "Freelancing", "₹3–4K / VIDEO")]
E = html.escape


def norm(w):
    return re.sub(r"[^a-z0-9₹+]", "", w.lower())


class Comp:
    def __init__(self, plan):
        self.p, self.id = plan, plan["id"]
        self.dur = plan["duration"]
        self.cam, self.over, self.scenes, self.top, self.audio, self.js = [], [], [], [], [], []
        self.n = 0
        self.nocaps = []  # (start, end) windows with captions suppressed

    def uid(self, k):
        self.n += 1
        return f"{k}{self.n}"

    def sfx(self, t, name, vol=0.5, dur=None):
        if t < 0 or t >= self.dur:
            return
        dur = dur or {"riser": 3, "whoosh-cinematic": 2.2, "glitch-1": 0.6, "glitch-2": 0.6, "glitch-3": 0.6,
                      "impact-bass-1": 1.8, "impact-bass-2": 2.2, "chime": 1.8, "notification": 1.5,
                      "sparkle": 1.6, "typing": 1.4}.get(name, 0.7)
        dur = min(dur, self.dur - t)
        lanes = self.__dict__.setdefault("lanes", [])  # end time per SFX lane, so overlaps get their own track
        k = next((j for j, end in enumerate(lanes) if end <= t), None)
        if k is None:
            lanes.append(0); k = len(lanes) - 1
        lanes[k] = t + dur
        self.audio.append(f'<audio id="{self.uid("sfx")}" class="clip" src="assets/sfx/{name}.mp3" '
                          f'data-start="{t:.3f}" data-duration="{dur:.3f}" data-track-index="{10 + k}" data-volume="{vol}"></audio>')

    def tw(self, s):
        self.js.append(s)

    # ---------- cue handlers ----------
    def c_bh(self, c):
        i = self.uid("bh"); t, d = c["t"], c["d"]
        text = c["text"]
        size = c.get("size") or int(min(420, 1780 / (0.47 * max(len(text), 1))))
        words = "".join(f'<span class="w">{E(ch) if ch != " " else "&nbsp;"}</span>' for ch in text)
        self.cam.append(f'<div id="{i}" class="bh {c.get("style", "white")}" style="font-size:{size}px;top:{c.get("top", 75)}px;opacity:0">{words}</div>')
        msrc = c.get("matteFile") or f"assets/mattes/{self.id}_{c['matte']}.webm"
        mstart = f' data-media-start="{c["mediaStart"]:.3f}"' if c.get("mediaStart") else ""
        self.cam.append(f'<video id="{i}m" class="matte clip" src="{msrc}" muted playsinline '
                        f'data-start="{t:.3f}" data-duration="{d:.3f}"{mstart} data-track-index="2"></video>')
        self.tw(f'tl.set("#{i}",{{opacity:1}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .w",{{y:-90,opacity:0,filter:"blur(18px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:.32,ease:"power3.out",stagger:{c.get("stagger", .045)}}},{t:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,scale:1.04,duration:.22,ease:"power2.in"}},{t + d - .24:.3f});')
        self.sfx(t - .12, "whoosh-short", .35)
        self.sfx(t + .05, "impact-bass-1", .5)

    def c_pop(self, c):
        i = self.uid("pop"); t, d = c["t"], c["d"]
        if "logo" in c:
            tile = f'<div class="tile logo"><img src="{c["logo"]}" alt=""></div>'
        else:
            tile = f'<div class="tile {c.get("tile", "")}"><svg viewBox="0 0 24 24">{ICONS[c["icon"]]}</svg></div>'
        lbl = f'<div class="lbl">{E(c["label"])}</div>' if c.get("label") else ""
        self.over.append(f'<div id="{i}" class="pop" style="left:{c["x"] - 130}px;top:{c["y"] - 88}px">{tile}{lbl}</div>')
        self.tw(f'tl.fromTo("#{i}",{{opacity:0,scale:.35,y:40}},{{opacity:1,scale:1,y:0,duration:.34,ease:"back.out(2.4)"}},{t:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,scale:.6,duration:.18,ease:"power2.in"}},{t + d - .18:.3f});')
        self.sfx(t, c.get("sound", "pop"), .45)

    def c_note(self, c):
        i = self.uid("note"); t, d = c["t"], c["d"]
        arrow = ""
        if c.get("arrow") == "left":
            arrow = '<svg viewBox="0 0 150 90" style="left:-170px;top:10px"><path d="M140 20 C 100 0, 40 10, 14 60"/><path d="M14 60 L 10 30 M14 60 L 42 52"/></svg>'
        elif c.get("arrow") == "right":
            arrow = '<svg viewBox="0 0 150 90" style="right:-170px;top:10px"><path d="M10 20 C 50 0, 110 10, 136 60"/><path d="M136 60 L 140 30 M136 60 L 108 52"/></svg>'
        color = {"money": "color:var(--money)", "red": "color:var(--glow)"}.get(c.get("color"), "")
        self.over.append(f'<div id="{i}" class="note" style="left:{c["x"]}px;top:{c["y"]}px;{color}">{E(c["text"])}{arrow}</div>')
        self.tw(f'tl.fromTo("#{i}",{{opacity:0,rotation:-6,scale:.7}},{{opacity:1,rotation:0,scale:1,duration:.3,ease:"back.out(2)"}},{t:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,duration:.18}},{t + d - .18:.3f});')
        self.sfx(t, "click-soft", .4)

    def c_l3(self, c):
        i = self.uid("l3"); t, d = c["t"], c["d"]
        self.over.append(f'<div id="{i}" class="l3"><div class="name">{E(c["name"])}</div><span class="role">{E(c["role"])}</span></div>')
        self.tw(f'tl.fromTo("#{i}",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.35,ease:"expo.out"}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .role",{{opacity:0,y:12}},{{opacity:1,y:0,duration:.3}},{t + .2:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,x:-40,duration:.22,ease:"power2.in"}},{t + d - .22:.3f});')
        self.sfx(t - .05, "whoosh-short", .35)

    def dim(self, t, d, amt=.62):
        i = self.uid("dim")
        self.over.insert(0, f'<div id="{i}" class="layer dim"></div>')
        self.tw(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:{amt},duration:.2}},{t:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,duration:.2}},{t + d - .2:.3f});')

    def c_proof(self, c):
        i = self.uid("proof"); t, d = c["t"], c["d"]
        self.dim(t, d)
        cap = f'<div class="cap2">{E(c["caption"])}</div>' if c.get("caption") else ""
        stamp = f'<div class="stamp">{E(c.get("stamp", "PROOF"))}</div>' if c.get("stamp", "PROOF") else ""
        self.over.append(f'<div id="{i}" class="proof">{cap}<div class="card"><img src="{c["img"]}" alt="">{stamp}</div></div>')
        self.tw(f'tl.set("#{i}",{{opacity:1}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .card",{{x:900,rotation:14,opacity:0}},{{x:0,rotation:-3,opacity:1,duration:.5,ease:"back.out(1.3)"}},{t:.3f});')
        if cap:
            self.tw(f'tl.fromTo("#{i} .cap2",{{y:-40,opacity:0}},{{y:0,opacity:1,duration:.3,ease:"power3.out"}},{t + .15:.3f});')
        if stamp:
            self.tw(f'tl.fromTo("#{i} .stamp",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:.22,ease:"power4.in"}},{t + .55:.3f});')
            self.sfx(t + .74, "impact-bass-2", .45)
        self.tw(f'tl.to("#{i}",{{opacity:0,scale:.92,duration:.22,ease:"power2.in"}},{t + d - .22:.3f});')
        self.sfx(t - .05, "whoosh", .45)
        if c.get("nocaps", True):
            self.nocaps.append((t, t + d))

    def c_chapter(self, c):
        i = self.uid("ch"); t, d = c["t"], c["d"]
        self.scenes.append(
            f'<div id="{i}" class="scene chapter bg-dark"><div class="num">{E(c["num"])}</div>'
            f'<div class="txt"><div class="kicker">WAY {E(c["num"])} / 04</div><div class="title">{E(c["title"])}</div>'
            f'<div class="sub">{E(c.get("sub", ""))}</div></div><div class="bar"></div></div>')
        self.tw(f'tl.set("#{i}",{{opacity:1}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .num",{{x:-420,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"expo.out"}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .kicker",{{opacity:0,x:40}},{{opacity:1,x:0,duration:.3}},{t + .15:.3f});')
        self.tw(f'tl.fromTo("#{i} .title",{{opacity:0,y:60,filter:"blur(14px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.4,ease:"power3.out"}},{t + .22:.3f});')
        self.tw(f'tl.fromTo("#{i} .sub",{{opacity:0}},{{opacity:1,duration:.3}},{t + .45:.3f});')
        self.tw(f'tl.fromTo("#{i} .bar",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"power2.inOut"}},{t + .1:.3f});')
        self.tw(f'tl.fromTo("#{i}",{{scale:1}},{{scale:1.05,duration:{d:.3f},ease:"none"}},{t:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,duration:.16}},{t + d - .16:.3f});')
        self.c_flash(dict(t=t + d - .08))
        self.sfx(t - .25, "whoosh-cinematic", .4)
        self.sfx(t + .05, "impact-bass-2", .55)
        self.nocaps.append((t, t + d))

    def c_table(self, c):
        i = self.uid("tb"); t, d, a = c["t"], c["d"], c["active"]
        rows = []
        for k, (n, title, money) in enumerate(WAYS, 1):
            cls = "row blur" if k > a else "row"
            rows.append(f'<div class="{cls}" id="{i}r{k}"><div class="n">{n}</div><div class="t">{E(title)}</div>'
                        f'<div class="m">{E(money)}</div><div class="hl"></div></div>')
        self.scenes.append(f'<div id="{i}" class="scene table bg-dark"><div class="wrap"><h2>4 Ways to Earn <b>as a Student</b></h2>'
                           f'{"".join(rows)}</div></div>')
        oy = 250 + (a - 1) * 172 + 75  # active row centre inside .wrap
        self.tw(f'tl.set("#{i}",{{opacity:1}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .wrap",{{scale:.9,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"power3.out"}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .row",{{x:-60,opacity:0}},{{x:0,opacity:1,duration:.3,stagger:.06,ease:"power2.out"}},{t + .1:.3f});')
        self.tw(f'tl.fromTo("#{i}r{a} .hl",{{opacity:0}},{{opacity:1,duration:.2,repeat:1,yoyo:true}},{t + .6:.3f});')
        self.tw(f'tl.set("#{i}r{a} .hl",{{opacity:1}},{t + 1.0:.3f});')
        self.tw(f'tl.to("#{i} .wrap",{{scale:1.28,transformOrigin:"50% {oy}px",duration:{d - 1.1:.3f},ease:"power2.inOut"}},{t + .9:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,duration:.18}},{t + d - .18:.3f});')
        self.sfx(t - .1, "whoosh", .45)
        self.sfx(t + .6, "click", .5)
        self.sfx(t + .85, "ping", .3)
        self.nocaps.append((t, t + d))

    def c_broll(self, c):
        i = self.uid("br"); t, d = c["t"], c["d"]
        if c.get("img") and not os.path.exists(c["img"]):
            print("  (no stock yet for", c["img"], "- using dark background)")
            c = {k: v for k, v in c.items() if k != "img"}
        img = f'<img src="{c["img"]}" alt=""><div class="tint"></div><div class="shade"></div>' if c.get("img") else ""
        bg = "" if c.get("img") else " bg-dark"
        bsize = f' style="font-size:{c["size"]}px"' if c.get("size") else ""
        big = f'<div class="big {c.get("bigStyle", "chrome")}" id="{i}b"{bsize}>{E(c.get("big", ""))}</div>' if ("big" in c or "count" in c) else ""
        small = f'<div class="small" id="{i}s">{E(c["small"])}</div>' if c.get("small") else ""
        self.scenes.append(f'<div id="{i}" class="scene broll{bg}">{img}{big}{small}</div>')
        self.tw(f'tl.set("#{i}",{{opacity:1}},{t:.3f});')
        if c.get("img"):
            self.tw(f'tl.fromTo("#{i} img",{{scale:1.0,x:0}},{{scale:1.12,x:{c.get("pan", -40)},duration:{d:.3f},ease:"none"}},{t:.3f});')
        if big:
            self.tw(f'tl.fromTo("#{i}b",{{scale:1.5,opacity:0,filter:"blur(20px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:.4,ease:"power3.out"}},{t + .1:.3f});')
            self.sfx(t + .12, "impact-bass-1", .45)
        if "count" in c:
            k = c["count"]; cd = k.get("dur", min(1.4, d - .6))
            self.tw(f'(function(){{const o={{v:{k["from"]}}},el=document.getElementById("{i}b");'
                    f'tl.fromTo(o,{{v:{k["from"]}}},{{v:{k["to"]},duration:{cd:.3f},ease:"power2.out",'
                    f'onUpdate:()=>{{el.textContent="{k.get("prefix", "")}"+fmt(o.v)+"{k.get("suffix", "")}";}}}},{t + .15:.3f});}})();')
            self.sfx(t + .15, "typing", .22, cd)
            self.sfx(t + .15 + cd, "chime", .3)
        if small:
            self.tw(f'tl.fromTo("#{i}s",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},{t + .45:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,duration:.18}},{t + d - .18:.3f});')
        self.sfx(t - .1, "whoosh", .4)
        if c.get("nocaps", False):
            self.nocaps.append((t, t + d))

    def c_phone(self, c):
        i = self.uid("ph"); t, d = c["t"], c["d"]
        bars = "".join(f'<i style="height:{h}%"></i>' for h in (45, 70, 55, 90, 100, 80, 65))
        self.scenes.append(f'<div id="{i}" class="scene bg-dark"><div class="phone"><div class="scr">'
                           f'<div class="lbl">SCREEN TIME · DAILY AVG</div><div class="val" id="{i}v">0h 0m</div>'
                           f'<div class="bars">{bars}</div><div class="apps">Instagram · 3h 10m<br>YouTube · 2h 25m<br>Snapchat · 1h 47m</div>'
                           f'</div></div></div>')
        self.scenes[-1] = self.scenes[-1].replace("<br>", "</div><div class=\"apps\" style=\"margin-top:0\">")
        self.tw(f'tl.set("#{i}",{{opacity:1}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .phone",{{y:300,rotation:8,opacity:0}},{{y:0,rotation:0,opacity:1,duration:.5,ease:"back.out(1.4)"}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .bars i",{{scaleY:0}},{{scaleY:1,duration:.4,stagger:.06,ease:"power2.out"}},{t + .4:.3f});')
        self.tw(f'(function(){{const o={{v:0}},el=document.getElementById("{i}v");tl.fromTo(o,{{v:0}},{{v:{c.get("minutes", 462)},duration:1.2,ease:"power2.out",'
                f'onUpdate:()=>{{const m=Math.round(o.v);el.textContent=Math.floor(m/60)+"h "+(m%60)+"m";}}}},{t + .4:.3f});}})();')
        self.tw(f'tl.fromTo("#{i} .phone",{{scale:1}},{{scale:1.08,duration:{d:.3f},ease:"none"}},{t:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,duration:.18}},{t + d - .18:.3f});')
        self.sfx(t - .05, "whoosh", .45)
        self.sfx(t + .4, "typing", .22, 1.2)
        self.sfx(t + 1.6, "notification", .3)
        self.nocaps.append((t, t + d))

    def c_flash(self, c):
        i = self.uid("fl"); t = c["t"]
        self.top.append(f'<div id="{i}" class="layer flash"></div>')
        self.tw(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:.9,duration:.05}},{max(0, t):.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,duration:.18}},{max(0, t) + .05:.3f});')

    def c_glitch(self, c):
        i = self.uid("gl"); t = c["t"]
        self.top.append(f'<div id="{i}" class="layer glitch"></div>')
        for k, (x, o) in enumerate([(-28, .9), (22, .5), (-12, .8), (16, .4), (0, 0)]):
            self.tw(f'tl.set("#{i}",{{opacity:{o},y:{(k * 37) % 60}}},{t + k * .05:.3f});')
            self.tw(f'tl.set("#camx",{{x:{x}}},{t + k * .05:.3f});')
        self.sfx(t, "glitch-1", .35, .5)

    def c_sfx(self, c):
        self.sfx(c["t"], c["name"], c.get("vol", .5), c.get("dur"))

    def c_timeline(self, c):
        """Editing-software mock: tracks fill with clips, playhead sweeps, price lands on top."""
        i = self.uid("tl"); t, d = c["t"], c["d"]
        lanes = [("V2", [(4, 14, "#7b5cff"), (30, 22, "#7b5cff"), (66, 18, "#7b5cff")]),
                 ("V1", [(0, 26, "#e0141e"), (27, 31, "#ff5a36"), (59, 25, "#e0141e"), (85, 15, "#ff5a36")]),
                 ("A1", [(0, 58, "#1fbf75"), (59, 41, "#1fbf75")]),
                 ("SFX", [(12, 6, "#f5c400"), (40, 5, "#f5c400"), (63, 7, "#f5c400"), (88, 5, "#f5c400")])]
        rows = "".join(f'<div class="nle-row"><b>{n}</b><div class="nle-track">' +
                       "".join(f'<i style="left:{x}%;width:{w}%;background:{col}"></i>' for x, w, col in clips) +
                       '</div></div>' for n, clips in lanes)
        big = f'<div class="big {c.get("bigStyle", "money")}" id="{i}b" style="top:30%">{E(c.get("big", ""))}</div>' if c.get("big") else ""
        small = f'<div class="small" id="{i}s" style="top:46%">{E(c["small"])}</div>' if c.get("small") else ""
        self.scenes.append(f'<div id="{i}" class="scene bg-dark"><div class="nle">{rows}<div class="nle-head"></div></div>{big}{small}</div>')
        self.tw(f'tl.set("#{i}",{{opacity:1}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .nle-track i",{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:.25,stagger:.035,ease:"power2.out"}},{t + .05:.3f});')
        self.tw(f'tl.fromTo("#{i} .nle-head",{{x:0}},{{x:1400,duration:{d - .2:.3f},ease:"none"}},{t:.3f});')
        if big:
            self.tw(f'tl.fromTo("#{i}b",{{scale:1.5,opacity:0,filter:"blur(20px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:.4,ease:"power3.out"}},{t + .35:.3f});')
            self.sfx(t + .37, "impact-bass-1", .45)
        if small:
            self.tw(f'tl.fromTo("#{i}s",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},{t + .6:.3f});')
        self.tw(f'tl.to("#{i}",{{opacity:0,duration:.18}},{t + d - .18:.3f});')
        self.sfx(t - .1, "whoosh", .4)
        self.sfx(t + .05, "typing", .2, 1.0)
        if c.get("nocaps", True):
            self.nocaps.append((t, t + d))

    # ---------- captions + zoom ----------
    def captions(self, words):
        keys = {norm(k): v for k, v in self.p.get("keys", {}).items()}
        groups, cur = [], []
        for w in words:
            k = keys.get(norm(w["w"]))
            if k:
                if cur:
                    groups.append((cur, None)); cur = []
                groups.append(([w], k)); continue
            cur.append(w)
            text = " ".join(x["w"] for x in cur)
            if len(cur) >= 2 or len(text) > 11 or re.search(r"[.,?!]$", w["w"]):
                groups.append((cur, None)); cur = []
        if cur:
            groups.append((cur, None))
        fixes = {norm(a): b for a, b in self.p.get("fix", {}).items()}
        html_caps = []
        for gi, (ws, k) in enumerate(groups):
            s = ws[0]["s"]
            nxt = groups[gi + 1][0][0]["s"] if gi + 1 < len(groups) else self.dur
            e = min(nxt, ws[-1]["e"] + .35)
            if any(a - .05 < s < b for a, b in self.nocaps) or e - s < .08:
                continue
            text = " ".join(fixes.get(norm(x["w"]), x["w"]) for x in ws).strip(" ,")
            text = re.sub(r"\.$", "", text)
            i = self.uid("cap")
            cls = f"cap key {k}" if k else "cap"
            html_caps.append(f'<div id="{i}" class="{cls}"><span>{E(text)}</span></div>')
            self.tw(f'tl.fromTo("#{i}",{{opacity:0,scale:{.7 if k else .88},y:{20 if k else 10}}},{{opacity:1,scale:1,y:0,duration:{.16 if k else .1},ease:"back.out(2.5)"}},{s:.3f});')
            self.tw(f'tl.set("#{i}",{{opacity:0}},{e:.3f});')
        return html_caps

    def zooms(self, words):
        z = self.p.get("zoom")
        if z is None:  # punch on every sentence start, alternating
            starts, prev_end = [0.0], True
            for w in words:
                if prev_end and w["s"] - starts[-1] > 2.2:
                    starts.append(w["s"])
                prev_end = bool(re.search(r"[.,?!]$", w["w"]))
            cycle = [1.0, 1.16, 1.0, 1.26]
            z = [[t, cycle[k % 4]] for k, t in enumerate(starts)]
        for t, s, *rest in z:
            ease = rest[0] if rest else None
            if ease:
                self.tw(f'tl.to("#cam",{{scale:{s},duration:.35,ease:"power2.inOut"}},{t:.3f});')
            else:
                self.tw(f'tl.set("#cam",{{scale:{s}}},{t:.3f});')

    def segments(self):
        """Stitch source ranges from several clips; returns (video html, shifted words)."""
        vids, words, t = [], [], 0.0
        for k, sg in enumerate(self.p["segments"]):
            a, b = sg["from"], sg["to"]
            vids.append(f'<video id="seg{k}" class="clip" src="{sg["video"]}" playsinline data-has-audio="true" '
                        f'data-start="{t:.3f}" data-duration="{b - a:.3f}" data-media-start="{a:.3f}" '
                        f'data-track-index="0" data-volume="1"></video>')
            for w in json.load(open(sg["words"])):
                if a - .02 <= w["s"] < b - .05:
                    words.append(dict(s=round(w["s"] - a + t, 3), e=round(min(w["e"], b) - a + t, 3), w=w["w"]))
            sg["at"] = t
            t += b - a
        return "\n    ".join(vids), words

    def c_title(self, c):
        i = self.uid("ti"); t, d = c["t"], c["d"]
        self.scenes.append(f'<div id="{i}" class="scene bg-dark titlecard"><div class="kicker">{E(c.get("kicker", ""))}</div>'
                           f'<div class="tc1">{E(c["line1"])}</div><div class="tc2">{E(c["line2"])}</div>'
                           f'<div class="tc3">{E(c.get("line3", ""))}</div></div>')
        self.tw(f'tl.set("#{i}",{{opacity:1}},{t:.3f});')
        self.tw(f'tl.fromTo("#{i} .kicker",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.3}},{t + .05:.3f});')
        self.tw(f'tl.fromTo("#{i} .tc1",{{opacity:0,scale:1.6,filter:"blur(20px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.35,ease:"power3.out"}},{t + .1:.3f});')
        self.tw(f'tl.fromTo("#{i} .tc2",{{opacity:0,y:80}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},{t + .3:.3f});')
        self.tw(f'tl.fromTo("#{i} .tc3",{{opacity:0}},{{opacity:1,duration:.3}},{t + .7:.3f});')
        self.tw(f'tl.fromTo("#{i}",{{scale:1}},{{scale:1.06,duration:{d:.3f},ease:"none"}},{t:.3f});')
        if c.get("out", True):
            self.tw(f'tl.to("#{i}",{{opacity:0,duration:.18}},{t + d - .18:.3f});')
        self.sfx(t, "impact-bass-2", .55)
        self.sfx(t + .3, "whoosh-short", .35)
        self.nocaps.append((t, t + d))

    def build(self):
        if "segments" in self.p:
            vid, words = self.segments()
        else:
            words = json.load(open(self.p["words"]))
        for c in sorted(self.p.get("cues", []), key=lambda c: c["t"]):
            getattr(self, "c_" + c["type"])(c)
        self.zooms(words)
        caps = self.captions(words)
        if "segments" not in self.p:
            vid = (f'<video id="base" class="clip" src="{self.p["video"]}" playsinline data-has-audio="true" '
                   f'data-start="0" data-duration="{self.dur:.3f}" data-track-index="0" data-volume="1"></video>')
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>{self.id}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
{FONTS}
{CSS}
</style>
</head>
<body>
<div id="root" data-composition-id="{self.id}" data-start="0" data-duration="{self.dur:.3f}" data-width="1920" data-height="1080">
  <div id="camx" class="layer"><div id="cam">
    {vid}
    {chr(10).join("    " + h for h in self.cam).strip()}
  </div></div>
  <div class="layer vignette"></div>
  <div id="over" class="layer">
{chr(10).join("    " + h for h in self.over)}
  </div>
  <div id="scenes" class="layer">
{chr(10).join("    " + h for h in self.scenes)}
  </div>
  <div id="caps">
{chr(10).join("    " + h for h in caps)}
  </div>
{chr(10).join("  " + h for h in self.top)}
{chr(10).join("  " + h for h in self.audio)}
</div>
<script>
function fmt(v){{return Math.round(v).toLocaleString("en-IN");}}
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(self.js)}
window.__timelines["{self.id}"] = tl;
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for path in sys.argv[1:]:
        plan = json.load(open(path))
        out = plan.get("out", plan["id"] + ".html")
        open(out, "w").write(Comp(plan).build())
        print("wrote", out)
