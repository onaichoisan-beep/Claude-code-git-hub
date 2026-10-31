"""Generates index.html for the Chill Breeze highlight v2 (run: python3 src/build.py)."""
import json, html, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SHOTS = json.load(open(os.path.join(HERE, "shots.json")))   # exact frame-based piece starts
FOOT = round(sum(s["frames"] for s in SHOTS) / 30, 3); END = 67.0
Y, R = "y", "r"
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
 (61.73,63.30,[("CHECK THIS",62.00,None,0),("PLACE",62.40,None,0),("OUT",62.85,Y,1)]),
]
for _i in range(len(CAP)-1):
    _s,_e,_w=CAP[_i]; _n=CAP[_i+1][0]; CAP[_i]=(_s,round(min(_n-0.04,_e+0.6),2),_w)
# B-roll: (id, kind, src, start, end)
BROLL = [("b-facial","img","assets/img/B6.jpg",3.05,4.40),
         ("b-bkk","vid","assets/broll/bangkok.mp4",4.40,6.75),
         ("b-chn","vid","assets/broll/chennai.mp4",8.80,9.60),
         ("b-phone","vid","assets/broll/phone.mp4",9.60,10.77),
         ("b-massage","vid","assets/broll/massage.mp4",13.05,14.80),
         ("b-clap","vid","assets/broll/clapper.mp4",17.86,19.36),
         ("b-mirror","vid","assets/broll/mirror.mp4",19.95,21.13),
         ("b-salon","vid","assets/broll/salon.mp4",29.10,31.10),
         ("b-botox","vid","assets/broll/botox.mp4",33.45,35.28),
         ("b-skin","vid","assets/broll/skincare.mp4",35.32,37.22),
         ("b-hair","img","assets/img/I2.jpg",44.22,45.96),
         ("b-laser","vid","assets/broll/laser.mp4",46.62,48.14),
         ("b-slim","vid","assets/broll/waist.mp4",50.25,51.76)]
ICON = {
 "skin":'<path d="M12 3c3 4 6 7.5 6 11a6 6 0 0 1-12 0c0-3.5 3-7 6-11z"/>',
 "age":'<path d="M17.5 3.5l3 3-2 2-1-1-6.8 6.8 1 1-2.2 2.2-1-1L5 20l-1-1 3.5-3.5-1-1L8.7 12.3l1 1L16.5 6.5l-1-1z"/>',
 "acne":'<path d="M12 2l1.8 6.2L20 10l-6.2 1.8L12 18l-1.8-6.2L4 10l6.2-1.8z"/><circle cx="19" cy="19" r="2.2"/>',
 "hair":'<path d="M7 21c0-6 2-9 5-12s4-5 3-7c3 2 4 5 2 9s-4 6-4 10h-2c0-4 2-7 3-9-2 2-5 4-5 9z"/>',
 "laser":'<path d="M13 2L4 14h6l-1 8 9-12h-6z"/>',
 "slim":'<path d="M3 9h18v6H3z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M7 9v3M11 9v3M15 9v3M19 9v2"/>'}
MENU = [("skin","Medicated facials","SKIN",30.16,""),("age","Botox","ANTI-AGEING",33.51,""),("age","Fillers","ANTI-AGEING",34.13,""),
        ("age","Threads","ANTI-AGEING",34.55,""),("acne","Acne treatments","SKIN",35.56,""),("hair","PRP","HAIR",42.26,""),
        ("hair","GFC","HAIR",42.84,""),("hair","Exosomes","HAIR",43.46,""),("hair","Follicular grafting","HAIR",44.60,"NEW"),
        ("laser","Laser hair removal","BODY",46.92,""),("slim","Slimming","BODY",50.41,"SOON")]
SFX = [("impact-bass-1",0.00,0.5),("pop",0.72,0.3),("whoosh-short",0.25,0.3),("whoosh",3.02,0.45),("whoosh-short",4.38,0.4),
       ("ping",5.08,0.25),("whoosh-cinematic",7.30,0.35),("ping",8.62,0.25),("whoosh-short",8.78,0.35),("typing",9.62,0.45),
       ("key-press",10.30,0.35),("impact-bass-2",10.77,0.6),("error",10.80,0.25),("whoosh-short",13.03,0.4),
       ("click",18.36,0.9),("impact-bass-1",18.38,0.3),("sparkle",19.98,0.4),("whoosh-short",21.18,0.3),("ping",21.30,0.2),
       ("whoosh",24.96,0.4),("whoosh",26.10,0.4),("whoosh",27.50,0.4),("whoosh-short",29.08,0.35),("whoosh-short",33.43,0.35),
       ("whoosh-short",35.30,0.35),("whoosh-short",44.20,0.35),("sparkle",44.60,0.4),("whoosh-short",46.60,0.35),
       ("glitch-1",46.92,0.12),("whoosh-short",50.23,0.35),("chime",50.41,0.25),("whoosh",51.45,0.4),
       ("impact-bass-1",56.46,0.35),("ping",58.29,0.2),("whoosh-cinematic",63.20,0.4),("impact-bass-1",63.75,0.45)]
SFX += [("pop",t,0.25) for *_,t,_ in MENU]
DUR = {"impact-bass-1":2.12,"impact-bass-2":2.59,"pop":0.72,"whoosh":0.57,"whoosh-short":0.57,"whoosh-cinematic":5.54,"error":1.62,
       "click":0.37,"sparkle":1.80,"chime":2.54,"typing":1.54,"key-press":0.43,"ping":1.32,"glitch-1":0.6}

def cap_html(i,s,e,words):
    out=[]; last=max([j for j,w in enumerate(words) if w[3]] or [-1])
    for j,(w,t,c,b) in enumerate(words):
        cls="w"+(" k"+c if c else "")+(" big" if b else "")
        if j==last and c: out.append(f'<span class="{cls} hlw" id="cw{i}_{j}"><span class="hl" id="hl{i}_{j}"></span><span class="tx">{html.escape(w)}</span></span>')
        else: out.append(f'<span class="{cls}" id="cw{i}_{j}">{html.escape(w)}</span>')
    return f'<div class="cap" id="cap{i}">{"".join(out)}</div>'
caps="\n".join(cap_html(i,*c) for i,c in enumerate(CAP))
br=[]
for b,kind,src,s,e in BROLL:
    d=round(e-s,3)
    if kind=="vid": br.append(f'<div class="bwrap" id="w-{b}"><video id="{b}" class="clip bvid" src="{src}" muted playsinline data-start="{s}" data-duration="{d}" data-track-index="2"></video></div>')
    else: br.append(f'<div class="bwrap" id="w-{b}"><div id="{b}" class="clip bimg" data-start="{s}" data-duration="{d}" data-track-index="2" style="background-image:url({src})"></div></div>')
brolls="\n".join(br)
cards="".join(f'<div class="card" id="mc{k}"><span class="ic"><svg viewBox="0 0 24 24">{ICON[ic]}</svg></span><span class="cl"><span class="ct">{html.escape(lab)}</span><span class="cs">{sec}</span></span>{f"<span class=\"badge {bd.lower()}\">{bd}</span>" if bd else ""}</div>' for k,(ic,lab,sec,t,bd) in enumerate(MENU))
audios="\n".join(f'<audio id="sfx{i:02d}" src="assets/sfx/{n}.mp3" data-start="{t}" data-duration="{min(DUR[n],END-t):.2f}" data-track-index="{11+i%3}" data-volume="{v}"></audio>' for i,(n,t,v) in enumerate(sorted(SFX,key=lambda x:x[1])))
music_auto=json.dumps({"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":1},{"t":10.6,"v":1},{"t":10.75,"v":0.4},{"t":11.6,"v":0.4},{"t":12.2,"v":1},{"t":51.6,"v":1},{"t":51.9,"v":0.35},{"t":53.1,"v":0.35},{"t":53.5,"v":1},{"t":63.3,"v":1},{"t":63.8,"v":1.4},{"t":66.4,"v":1.4},{"t":67,"v":0}]}]})
# camera drift per piece (reset at cuts), skip pieces covered by punch
starts=[]; t=0
for s in SHOTS: starts.append((round(t,4),round(s["frames"]/30,4),s["shot"])); t+=s["frames"]/30
js=dict(caps=json.dumps([[s,e,[[t,int(b),int(j==max([q for q,w in enumerate(ws) if w[3]] or [-1]) and bool(c))] for j,(w,t,c,b) in enumerate(ws)]] for (s,e,ws) in CAP]),
        menu=json.dumps([t for *_,t,_ in MENU]), broll=json.dumps([[b,s,e,kind] for b,kind,_,s,e in BROLL]), shots=json.dumps(starts))
PIN='<svg viewBox="0 0 24 24" class="pin"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'
DOTS="".join(f'<circle cx="{x}" cy="{y}" r="2.2"/>' for x in range(40,1920,40) for y in range(40,1080,40) if ((x*7+y*13)%97)<38)
page=open(os.path.join(HERE,"template.html")).read()
for k,v in dict(END=END,FOOT=FOOT,ENDD=round(END-FOOT,3),BROLLS=brolls,CAPS=caps,CARDS=cards,AUDIOS=audios,MUSIC=music_auto,PIN=PIN,DOTS=DOTS,
                JS_CAPS=js["caps"],JS_MENU=js["menu"],JS_BROLL=js["broll"],JS_SHOTS=js["shots"]).items():
    page=page.replace("%%"+k+"%%",str(v))
open(os.path.join(ROOT,"index.html"),"w").write(page)
print("wrote index.html", len(CAP),"captions",len(BROLL),"broll",len(SFX),"sfx","FOOT",FOOT)
