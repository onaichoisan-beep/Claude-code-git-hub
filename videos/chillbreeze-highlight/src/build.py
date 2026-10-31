"""Generates index.html for the Chill Breeze highlight (run: python3 src/build.py)."""
import json, html, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FOOT = 63.367; END = 67.0
Y, R = "y", "r"   # keyword colours: yellow / red
# Captions: (start, end, [(word, t, colour|None, big?)])
CAP = [
 (0.00, 1.50, [("I CAN SEE",0.0,None,0),("THE",0.36,None,0),("DIFFERENCE",0.72,Y,1)]),
 (1.54, 2.70, [("I'M FEELING",1.6,None,0),("GOOD",1.89,Y,1),("ABOUT IT",2.11,None,0)]),
 (2.76, 4.30, [("THIS",2.76,None,0),("LYMPHATIC",3.26,Y,1),("DRAINAGE",3.76,Y,1)]),
 (4.36, 6.42, [("I DID IT IN",4.36,None,0),("BANGKOK",5.08,Y,1),("ONCE",5.40,None,0)]),
 (6.48, 7.30, [("TWO YEARS",6.48,None,0),("AGO",6.96,None,0)]),
 (7.40, 8.76, [("HERE",7.93,None,0),("LOCALLY",8.25,Y,1)]),
 (8.81, 9.95, [("I ASKED",8.81,None,0),("MANY PEOPLE",9.17,Y,1)]),
 (9.99, 10.74,[("PUT IT",9.99,None,0),("ONLINE",10.28,Y,1)]),
 (10.77,12.68,[("NOBODY",10.77,R,1),("OFFERED IT",11.20,R,1)]),
 (12.75,14.78,[("THEY DID",12.75,None,0),("BODY MASSAGE",13.48,Y,1)]),
 (15.40,16.72,[("FIRST TIME",15.59,Y,1),("I ASKED",15.99,None,0)]),
 (16.77,17.82,[("CAN YOU",16.77,None,0),("DO THAT?",17.39,Y,1)]),
 (17.86,19.36,[("A",18.10,None,0),("SHOOT",18.39,Y,1),("IS STARTING",18.79,None,0)]),
 (19.39,21.10,[("I NEED TO LOOK",19.39,None,0),("VERY",20.12,Y,1),("YOUNG",20.42,Y,1)]),
 (21.16,23.62,[("SHE DID A",21.16,None,0),("VERY NICE",22.26,Y,1)]),
 (23.70,24.92,[("LYMPHATIC",23.70,Y,1),("DRAINAGE",24.18,Y,1)]),
 (24.98,26.05,[("WHAT",24.98,None,0),("ELSE?",25.25,Y,1)]),
 (26.25,27.45,[("EVERYTHING",26.25,Y,1),("IS THERE",26.73,None,0)]),
 (27.55,28.64,[("STARTING WITH",27.55,None,0),("SKIN",28.30,Y,1)]),
 (29.08,31.86,[("MEDICATED",30.16,Y,1),("FACIALS",30.84,Y,1)]),
 (31.92,33.46,[("ANTI-AGEING",31.92,Y,1),("PROCEDURES",32.45,None,0)]),
 (33.51,35.26,[("BOTOX",33.51,Y,1),("FILLERS",34.13,Y,1),("THREADS",34.55,Y,1)]),
 (35.30,37.22,[("ACNE",35.56,Y,1),("TREATMENTS",36.24,None,0)]),
 (37.26,38.94,[("ALL TYPES OF",37.30,None,0),("ACNE",37.90,Y,1)]),
 (38.99,40.54,[("NOW,",38.99,None,0),("HAIR",39.56,Y,1)]),
 (40.60,44.16,[("PRP",42.26,Y,1),("GFC",42.84,Y,1),("EXOSOMES",43.46,Y,1)]),
 (44.22,45.94,[("NEW:",44.30,R,1),("FOLLICULAR",44.60,Y,1),("GRAFTING",45.30,Y,1)]),
 (45.99,48.12,[("LASER",46.92,Y,1),("HAIR REMOVAL",47.24,None,0)]),
 (48.18,51.74,[("SOON:",48.51,None,0),("SLIMMING",50.41,Y,1),("TOO",51.20,None,0)]),
 (51.80,53.26,[("IT'S ACTUALLY",51.80,None,0),("VERY",52.61,None,0),("SIMPLE",53.05,Y,1)]),
 (53.80,55.55,[("WHEN YOU HEAR",53.80,None,0),("THE TERMS",54.90,None,0)]),
 (55.62,57.40,[("IT SOUNDS LIKE A",55.62,None,0),("BIG PROCEDURE",56.46,R,1)]),
 (57.62,58.84,[("YOU HAVE A",57.62,None,0),("PROFESSIONAL",58.29,Y,1)]),
 (58.88,60.24,[("DOCTOR",58.88,Y,1),("AROUND",59.52,None,0)]),
 (60.32,61.68,[("DEFINITELY",60.57,None,0),("COME",61.11,Y,1)]),
 (61.73,63.40,[("CHECK THIS",62.00,None,0),("PLACE",62.40,None,0),("OUT",62.85,Y,1)]),
]
# Full-frame stock cutaways: (id, img, start, end, credit)
BROLL = [("b-facial","B6",3.05,4.40),("b-phone","C8",9.60,10.77),("b-massage","D1",13.05,14.80),
         ("b-film","E1",17.86,19.36),("b-botox","G1",33.45,35.28),("b-hair","I2",44.22,45.96),
         ("b-laser","J4",46.62,48.14),("b-slim","K7",50.25,51.76)]
# Treatment menu rows: (section, label, t, badge)
MENU = [("SKIN","Medicated facials",30.16,""),("ANTI-AGEING","Botox",33.51,""),("ANTI-AGEING","Fillers",34.13,""),
        ("ANTI-AGEING","Threads",34.55,""),("SKIN","Acne treatments",35.56,""),("HAIR","PRP",42.26,""),("HAIR","GFC",42.84,""),
        ("HAIR","Exosomes",43.46,""),("HAIR","Follicular grafting",44.60,"NEW"),("BODY","Laser hair removal",46.92,""),
        ("BODY","Slimming",50.41,"SOON")]
SFX = [("impact-bass-1",0.00,0.55),("pop",0.72,0.30),("whoosh",2.98,0.45),("pop",4.92,0.35),("whoosh-short",7.40,0.40),
       ("whoosh-short",9.58,0.40),("error",10.77,0.30),("whoosh-short",13.02,0.40),("click-soft",17.86,0.6),("whoosh",19.98,0.35),
       ("whoosh-short",21.20,0.35),("whoosh",24.96,0.40),("whoosh",26.10,0.35),("whoosh",27.50,0.40),
       ("sparkle",44.60,0.35),("chime",50.41,0.25),("whoosh",51.78,0.40),("impact-bass-1",56.46,0.35),
       ("whoosh",63.45,0.50),("impact-bass-1",63.80,0.45)]
SFX += [("pop",t,0.22) for _,_,t,_ in MENU]
DUR = {"impact-bass-1":2.12,"pop":0.72,"whoosh":0.57,"whoosh-short":0.57,"error":1.62,"click-soft":0.37,"sparkle":1.80,"chime":2.54}

for _i in range(len(CAP)-1):
    _s,_e,_w=CAP[_i]; _n=CAP[_i+1][0]
    CAP[_i]=(_s,round(min(_n-0.04,_e+0.6),2),_w)
def cap_html(i,s,e,words):
    sp="".join(f'<span class="w{(" k"+c) if c else ""}{" big" if b else ""}" id="cw{i}_{j}">{html.escape(w)}</span>' for j,(w,t,c,b) in enumerate(words))
    return f'<div class="cap" id="cap{i}">{sp}</div>'
caps="\n".join(cap_html(i,*c) for i,c in enumerate(CAP))
brolls="\n".join(f'<div id="{b}" class="clip broll" data-layout-allow-overflow data-start="{s}" data-duration="{round(e-s,3)}" data-track-index="2"><div class="bimg" style="background-image:url(assets/img/{img}.jpg)"></div></div>' for b,img,s,e in BROLL)
secs=[]; rows=""
for k,(sec,lab,t,badge) in enumerate(MENU):
    if sec not in secs: secs.append(sec)
for sec in ["SKIN","ANTI-AGEING","HAIR","BODY"]:
    rows+=f'<div class="msec">{sec}</div>'
    for k,(s2,lab,t,badge) in enumerate(MENU):
        if s2==sec:
            bd=f'<span class="badge {badge.lower()}">{badge}</span>' if badge else ""
            rows+=f'<div class="mrow" id="mr{k}"><span class="dot"></span><span class="mlab">{html.escape(lab)}</span>{bd}</div>'
audios="\n".join(f'<audio id="sfx{i:02d}" src="assets/sfx/{n}.mp3" data-start="{t}" data-duration="{DUR[n]}" data-track-index="{11+i%3}" data-volume="{v}"></audio>' for i,(n,t,v) in enumerate(sorted(SFX,key=lambda x:x[1])))
music_auto=json.dumps({"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":1},{"t":51.6,"v":1},{"t":51.9,"v":0.35},{"t":53.1,"v":0.35},{"t":53.5,"v":1},{"t":63.3,"v":1},{"t":63.8,"v":1.4},{"t":66.4,"v":1.4},{"t":67,"v":0}]}]})

js_caps=json.dumps([[s,e,[[t,int(b)] for (w,t,c,b) in ws]] for (s,e,ws) in CAP])
js_menu=json.dumps([t for (_,_,t,_) in MENU])
js_broll=json.dumps([[b,s,e] for b,_,s,e in BROLL])

PIN='<svg viewBox="0 0 24 24" class="pin"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'
page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>Chill Breeze highlight</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family: "Montserrat"; font-weight: 600; src: url(assets/fonts/montserrat-latin-600-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Montserrat"; font-weight: 800; src: url(assets/fonts/montserrat-latin-800-normal.woff2) format("woff2"); }}
@font-face {{ font-family: "Montserrat"; font-weight: 900; src: url(assets/fonts/montserrat-latin-900-normal.woff2) format("woff2"); }}
:root {{ --yel:#FFE14D; --red:#FF3B30; --ink:#fff; --glass:rgba(14,12,20,.72); --pink:#E8326B; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1920px; height:1080px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; font-family:"Montserrat",sans-serif; color:var(--ink); }}
#cam {{ position:absolute; inset:0; overflow:hidden; }}
#cam .inner {{ position:absolute; inset:0; transform-origin:64% 40%; }}
#interview, #gift {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.broll {{ position:absolute; inset:0; overflow:hidden; }}
.broll .bimg {{ position:absolute; inset:-2%; background-size:cover; background-position:center; }}
.broll::after {{ content:""; position:absolute; inset:0; background:linear-gradient(180deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,0) 40%,rgba(0,0,0,.55) 100%); }}
.vignette {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.45) 100%); }}
.capzone {{ position:absolute; left:0; right:0; bottom:70px; height:180px; }}
.cap {{ position:absolute; left:0; right:0; bottom:0; display:flex; justify-content:center; align-items:baseline; gap:0 22px; flex-wrap:wrap; padding:0 160px; opacity:0; text-align:center; }}
.w {{ display:inline-block; font-weight:900; font-size:64px; letter-spacing:-.5px; text-transform:uppercase; line-height:1.05;
      text-shadow:0 5px 0 rgba(0,0,0,.35),0 0 28px rgba(0,0,0,.6); opacity:0; }}
.w.big {{ font-size:90px; }}
.cap {{ white-space:nowrap; flex-wrap:nowrap; }}
#b-hair {{ background:#15131c; }}
#b-hair .bimg {{ inset:0; background-size:auto 113%; background-position:10px 22%; background-repeat:no-repeat; }}
.w.ky {{ color:var(--yel); }} .w.kr {{ color:var(--red); }}
.chip {{ position:absolute; display:flex; align-items:center; gap:14px; padding:16px 26px 16px 20px; border-radius:18px; background:var(--glass);
        backdrop-filter:blur(6px); box-shadow:0 10px 40px rgba(0,0,0,.35); }}
.chip .pin {{ width:44px; height:44px; fill:var(--pink); flex:none; }}
.chip .t1 {{ font-weight:900; font-size:40px; letter-spacing:.5px; line-height:1; }}
.chip .t2 {{ font-weight:600; font-size:28px; opacity:.85; margin-top:6px; }}
.chip .col {{ display:flex; flex-direction:column; }}
#hook {{ left:70px; top:64px; }}
#hook .tag {{ background:#C4122F; color:#fff; font-weight:900; font-size:28px; letter-spacing:2px; padding:8px 12px; border-radius:8px; }}
#hook .t1 {{ font-size:34px; }}
#title {{ left:70px; top:64px; }}
#title .t1 {{ font-size:54px; color:var(--yel); }}
#bkk {{ left:70px; top:64px; }} #chn {{ left:70px; top:64px; }} #loc {{ left:70px; top:64px; }} #film {{ left:70px; top:64px; }}
#chn .status {{ font-weight:900; font-size:30px; color:var(--red); margin-top:8px; letter-spacing:1px; }}
#chn .ok {{ font-weight:600; font-size:28px; opacity:.85; margin-top:8px; }}
#lt {{ position:absolute; left:70px; bottom:300px; }}
#lt .bar {{ position:absolute; left:0; top:0; bottom:0; width:10px; border-radius:6px; background:var(--pink); }}
#lt .box {{ padding:14px 30px 16px 34px; background:var(--glass); border-radius:14px; overflow:hidden; }}
#lt .n {{ font-weight:900; font-size:52px; line-height:1.05; }}
#lt .r {{ font-weight:600; font-size:28px; opacity:.9; margin-top:6px; }}
#menu {{ position:absolute; right:60px; top:60px; width:640px; padding:30px 34px 26px; border-radius:26px; background:var(--glass);
        backdrop-filter:blur(8px); box-shadow:0 20px 60px rgba(0,0,0,.4); border:1px solid rgba(255,255,255,.12); }}
#menu .mh {{ font-weight:900; font-size:30px; letter-spacing:3px; color:var(--yel); margin-bottom:6px; }}
#menu .ms {{ font-weight:600; font-size:28px; opacity:.8; margin-bottom:10px; }}
.msec {{ font-weight:800; font-size:28px; letter-spacing:3px; color:rgba(255,255,255,.62); margin:10px 0 0; }}
.mrow {{ display:flex; align-items:center; gap:14px; height:42px; font-weight:800; font-size:31px; opacity:.22; }}
.mrow .dot {{ width:14px; height:14px; border-radius:50%; background:rgba(255,255,255,.5); flex:none; }}
.mrow.on .dot {{ background:var(--yel); }}
.badge {{ font-weight:900; font-size:28px; letter-spacing:1px; padding:2px 10px; border-radius:7px; margin-left:6px; }}
.badge.new {{ background:#C4122F; }} .badge.soon {{ background:#fff; color:#111; }}
#endcard {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; background:rgba(8,6,14,.55); }}
#endcard .e1 {{ font-weight:900; font-size:120px; letter-spacing:-1px; line-height:1; }}
#endcard .x {{ color:var(--pink); padding:0 24px; }}
#endcard .e2 {{ font-weight:600; font-size:36px; margin-top:22px; opacity:.95; }}
#endcard .e3 {{ font-weight:600; font-size:28px; position:absolute; bottom:34px; opacity:.75; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
  <div id="cam" data-layout-allow-overflow><div class="inner">
    <video id="interview" src="assets/footage/interview.mp4" muted playsinline data-start="0" data-duration="{FOOT}" data-track-index="0"></video>
  </div></div>
  <video id="gift" src="assets/footage/bts-gift.mp4" muted playsinline data-start="{FOOT}" data-duration="{round(END-FOOT,3)}" data-track-index="1"></video>
{brolls}
  <div class="vignette"></div>

  <div id="hook" class="clip chip" data-start="0.1" data-duration="2.55" data-track-index="3"><span class="tag">REAL STORY</span><span class="t1">THE FACIAL NOBODY IN CHENNAI OFFERED</span></div>
  <div id="title" class="clip chip" data-start="2.95" data-duration="2.0" data-track-index="3"><div class="col"><span class="t1">LYMPHATIC DRAINAGE FACIAL</span><span class="t2">A gentle face massage that reduces puffiness</span></div></div>
  <div id="bkk" class="clip chip" data-start="4.95" data-duration="2.35" data-track-index="3">{PIN}<div class="col"><span class="t1">BANGKOK, THAILAND</span><span class="t2">where she first tried it · 2 years ago</span></div></div>
  <div id="chn" class="clip chip" data-start="7.40" data-duration="5.30" data-track-index="3">{PIN}<div class="col"><span class="t1">BACK HOME IN CHENNAI</span><span class="ok" id="chn-ok">searching for a clinic…</span><span class="status" id="chn-no">✕ NOBODY OFFERED IT</span></div></div>
  <div id="film" class="clip chip" data-start="17.90" data-duration="1.45" data-track-index="3"><div class="col"><span class="t1">FOR A FILM ROLE</span><span class="t2">needed to look younger</span></div></div>
  <div id="loc" class="clip chip" data-start="21.20" data-duration="3.70" data-track-index="3">{PIN}<div class="col"><span class="t1">CHILL BREEZE</span><span class="t2">Valluvar Kottam, Chennai · with TMCC</span></div></div>
  <div id="lt" class="clip" data-start="26.10" data-duration="5.40" data-track-index="4"><div class="box"><div class="bar"></div><div class="n">Dr. Suman</div><div class="r">Cosmetologist · The Madras Cosmetic Clinic (TMCC)</div></div></div>
  <div id="menu" class="clip" data-start="27.50" data-duration="24.30" data-track-index="4"><div class="mh">TREATMENT MENU</div><div class="ms">Now at Chill Breeze, Valluvar Kottam</div>{rows}</div>
  <div id="endcard" class="clip" data-start="{FOOT}" data-duration="{round(END-FOOT,3)}" data-track-index="5"><div class="e1">CHILL BREEZE<span class="x">×</span>TMCC</div><div class="e2">Cosmetology is now at Chill Breeze · Valluvar Kottam, Chennai</div><div class="e3">Music: “Upbeat Corporate”, Soundrider/Dope (CC BY 3.0) · Images: Wikimedia Commons</div></div>

  <div id="captions" class="clip capzone" data-start="0" data-duration="{FOOT}" data-track-index="6">
{caps}
  </div>

  <audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="{FOOT}" data-track-index="9" data-volume="1"></audio>
  <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{END}" data-track-index="10" data-volume="1" data-automation='{music_auto}'></audio>
{audios}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const CAPS = {js_caps};
CAPS.forEach(([s, e, ws], i) => {{
  tl.set("#cap" + i, {{ opacity: 1 }}, s);
  ws.forEach(([t, big], j) => {{
    const el = "#cw" + i + "_" + j;
    if (big) tl.fromTo(el, {{ opacity: 0, scale: 1.35, y: 10 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.16, ease: "back.out(2.6)" }}, t);
    else tl.fromTo(el, {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.10, ease: "power2.out" }}, t);
  }});
  tl.set("#cap" + i, {{ opacity: 0 }}, e);
}});
// camera: slow push on hook / outro, punch-ins on key words
tl.fromTo("#cam .inner", {{ scale: 1.0 }}, {{ scale: 1.07, duration: 2.73, ease: "none" }}, 0);
tl.set("#cam .inner", {{ scale: 1.0 }}, 2.73);
tl.set("#cam .inner", {{ transformOrigin: "74% 42%" }}, 19.95);
tl.to("#cam .inner", {{ scale: 1.28, duration: 0.14, ease: "power3.out" }}, 20.10);
tl.set("#cam .inner", {{ scale: 1.0, transformOrigin: "64% 40%" }}, 21.13);
tl.to("#cam .inner", {{ scale: 1.14, duration: 0.14, ease: "power3.out" }}, 56.44);
tl.set("#cam .inner", {{ scale: 1.0 }}, 57.43);
tl.set("#cam .inner", {{ transformOrigin: "60% 42%" }}, 60.29);
tl.fromTo("#cam .inner", {{ scale: 1.0 }}, {{ scale: 1.08, duration: 3.07, ease: "none", immediateRender: false }}, 60.29);
// stock cutaways: pop in + Ken Burns
{js_broll}.forEach(([id, s, e]) => {{
  tl.fromTo("#" + id + " .bimg", {{ scale: 1.18, opacity: 0 }}, {{ scale: 1.06, opacity: 1, duration: 0.22, ease: "power3.out" }}, s);
  tl.to("#" + id + " .bimg", {{ scale: 1.0, xPercent: -1.5, duration: e - s - 0.22, ease: "none" }}, s + 0.22);
}});
// chips
const chipIn = (id, t) => tl.fromTo(id, {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "back.out(1.8)" }}, t);
const chipOut = (id, t) => tl.to(id, {{ x: -40, opacity: 0, duration: 0.2, ease: "power2.in" }}, t);
chipIn("#hook", 0.1); chipOut("#hook", 2.45);
chipIn("#title", 2.95); chipOut("#title", 4.78);
chipIn("#bkk", 4.95); tl.fromTo("#bkk .pin", {{ y: -30 }}, {{ y: 0, duration: 0.4, ease: "bounce.out" }}, 5.0); chipOut("#bkk", 7.1);
chipIn("#chn", 7.40); tl.set("#chn-no", {{ display: "none" }}, 7.40);
tl.set("#chn-ok", {{ display: "none" }}, 10.77); tl.set("#chn-no", {{ display: "block" }}, 10.77);
tl.fromTo("#chn-no", {{ scale: 1.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.18, ease: "back.out(3)", transformOrigin: "0% 50%" }}, 10.77);
tl.fromTo("#chn", {{ x: -8 }}, {{ x: 8, duration: 0.05, repeat: 5, yoyo: true }}, 10.80); tl.set("#chn", {{ x: 0 }}, 11.10);
chipOut("#chn", 12.5);
chipIn("#film", 17.90); chipOut("#film", 19.15);
chipIn("#loc", 21.2); chipOut("#loc", 24.7);
// lower third
tl.fromTo("#lt .box", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.out" }}, 26.12);
tl.fromTo("#lt .n", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, 26.3);
tl.fromTo("#lt .r", {{ y: 14, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, 26.45);
tl.to("#lt .box", {{ clipPath: "inset(0 100% 0 0)", duration: 0.3, ease: "power2.in" }}, 31.15);
// treatment menu
tl.fromTo("#menu", {{ x: 700, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 27.5);
{js_menu}.forEach((t, k) => {{
  tl.to("#mr" + k, {{ opacity: 1, duration: 0.12 }}, t);
  tl.set("#mr" + k, {{ className: "mrow on" }}, t);
  tl.fromTo("#mr" + k + " .mlab", {{ x: -14 }}, {{ x: 0, duration: 0.25, ease: "back.out(2)" }}, t);
}});
tl.to("#menu", {{ x: 700, opacity: 0, duration: 0.35, ease: "power2.in" }}, 51.45);
// end card
tl.fromTo("#gift", {{ scale: 1.08 }}, {{ scale: 1.0, duration: {round(END-FOOT,3)}, ease: "none" }}, {FOOT});
tl.fromTo("#endcard .e1", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.7)" }}, {FOOT}+0.25);
tl.fromTo("#endcard .e2", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4 }}, {FOOT}+0.6);
tl.fromTo("#endcard .e3", {{ opacity: 0 }}, {{ opacity: 0.75, duration: 0.3 }}, {FOOT}+0.35);
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(os.path.join(ROOT,"index.html"),"w").write(page)
print("wrote index.html", len(CAP), "captions", len(BROLL), "cutaways", len(SFX), "sfx")
