"""Generates index.html for the Chill Breeze highlight v3 (doctor-led, witty). Run: python3 src/build.py"""
import json, html, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SHOTS = json.load(open(os.path.join(HERE, "shots.json")))
FOOT = round(sum(s["frames"] for s in SHOTS) / 30, 3); END = round(FOOT + 3.0, 3)
Y, R = "y", "r"
# speech captions: (start, end, [(word, t, colour, big)])
CAP = [
 (0.00, 2.10, [("WE'LL CREATE A",0.0,None,0),("MINI",1.27,Y,1),("BANGKOK",1.51,Y,1)]),
 (2.13, 3.30, [("TREATMENT",2.13,None,0),("HERE",2.40,Y,1)]),
 (3.34, 4.66, [("LET'S HOPE",3.76,None,0),("FOR THE BEST",4.14,Y,1)]),
 (4.71, 6.55, [("WHEN YOU SEE THIS…",4.71,None,0),("MASSAGE",6.01,Y,1),("FOR THE LEGS",6.27,None,0)]),
 (7.40, 9.70, [("WHAT",7.40,None,0),("TREATMENTS",8.52,Y,1)]),
 (9.97, 11.10,[("DO YOU",9.97,None,0),("SPECIALIZE IN?",10.22,Y,1)]),
 (11.25,12.62,[("THANK YOU SO MUCH",11.28,None,0),("FOR THE QUESTION",12.28,Y,1)]),
 (12.67,13.70,[("I'M GOING TO HAVE",12.81,None,0),("MY COFFEE",13.25,Y,1)]),
 (14.08,15.18,[("THANK YOU FOR",14.11,None,0),("THE QUESTION",14.55,None,0)]),
 (15.25,16.60,[("AND",15.25,None,0),("GREETINGS",15.29,Y,1),("TO EVERYONE",16.01,None,0)]),
 (16.80,20.05,[("ANU MADAM WAS",17.34,None,0),("EQUALLY",18.00,Y,1),("PASSIONATE",18.40,Y,1)]),
 (20.12,23.85,[("ABOUT OPENING A",21.29,None,0),("COSMETIC",22.65,Y,1),("CLINIC",22.97,Y,1)]),
 (23.95,25.72,[("EQUAL PASSION, MAYBE",23.97,None,0),("MORE",24.91,R,1),("PASSION",25.15,Y,1)]),
 (25.80,27.80,[("NO MATTER WHAT",25.81,None,0),("THE RELATIONSHIP",26.43,Y,1)]),
 (27.85,30.70,[("IF ONE",27.79,None,0),("LOVES MORE",28.16,Y,1),("& THE OTHER",29.00,None,0),("LESS",29.66,R,1)]),
 (30.73,32.20,[("THE RELATIONSHIP IS",30.73,None,0),("USELESS",31.40,R,1)]),
 (32.27,33.45,[("WHAT",32.27,None,0),("ELSE?",32.72,Y,1)]),
 (33.60,34.80,[("EVERYTHING",33.67,Y,1),("IS THERE",34.15,None,0)]),
 (34.85,35.98,[("STARTING WITH",35.00,None,0),("SKIN",35.80,Y,1)]),
 (36.40,39.25,[("MEDICATED",37.54,Y,1),("FACIALS",38.22,Y,1)]),
 (39.35,42.55,[("ANTI-AGEING:",39.35,None,0),("BOTOX",40.79,Y,1),("FILLERS",41.30,Y,1),("THREADS",41.62,Y,1)]),
 (42.65,46.00,[("ALL TYPES OF",42.65,None,0),("ACNE",42.87,Y,1),("TREATMENTS",43.55,None,0)]),
 (46.04,47.70,[("NOW,",46.04,None,0),("HAIR",46.62,Y,1)]),
 (47.75,51.50,[("PRP",49.54,Y,1),("GFC",50.12,Y,1),("EXOSOMES",50.74,Y,1)]),
 (51.55,53.30,[("NEW:",51.69,R,1),("FOLLICULAR",51.97,Y,1),("GRAFTING",52.81,Y,1)]),
 (53.40,55.35,[("LASER",54.17,Y,1),("HAIR REMOVAL",54.49,None,0)]),
 (55.45,59.05,[("SOON:",55.78,None,0),("SLIMMING",57.78,Y,1),("TOO",58.62,None,0)]),
 (59.13,60.70,[("I CAN SEE THE",59.13,None,0),("DIFFERENCE",59.85,Y,1)]),
 (60.78,61.90,[("FEELING",60.98,None,0),("GOOD",61.14,Y,1),("ABOUT IT",61.36,None,0)]),
 (62.20,FOOT,[("DEFINITELY",62.26,None,0),("COME",62.80,Y,1),("CHECK IT",63.74,None,0),("OUT",64.54,Y,1)]),
]
for _i in range(len(CAP)-1):
    _s,_e,_w=CAP[_i]; CAP[_i]=(_s,round(min(CAP[_i+1][0]-0.04,_e+0.6),2),_w)
# comedy "thought" captions + emoji stickers: (id, start, end, text, emoji, x, y, rot)
JOKES = [("j1",6.10,7.40,"client mode: ON","🦵",1300,190,-4),
         ("j2",13.85,15.20,"*sips coffee dramatically*","☕",1180,190,3),
         ("j3",15.95,16.62,"very formal","😂",160,190,-3),
         ("j4",30.75,32.25,"relationship advice??","💔",1240,190,3),
         ("j5",51.60,53.30,"she's still going","😳",130,190,-3)]
STICK = [("s1",1.50,3.25,"🇹🇭",860,110,10),("s2",24.90,25.75,"🔥",880,430,-8),
         ("s4",59.85,61.95,"✨",1000,140,8),("s5",62.80,FOOT,"👉",1540,520,0)]
# b-roll after 10 s only
BROLL = [("b-botox","vid","assets/broll/botox.mp4",39.40,41.70),
         ("b-hair","img","assets/img/I2.jpg",51.55,53.30),
         ("b-laser","vid","assets/broll/laser.mp4",53.65,55.40),("b-slim","vid","assets/broll/waist.mp4",57.30,59.05)]
ICON = {
 "skin":'<path d="M12 3c3 4 6 7.5 6 11a6 6 0 0 1-12 0c0-3.5 3-7 6-11z"/>',
 "age":'<path d="M17.5 3.5l3 3-2 2-1-1-6.8 6.8 1 1-2.2 2.2-1-1L5 20l-1-1 3.5-3.5-1-1L8.7 12.3l1 1L16.5 6.5l-1-1z"/>',
 "acne":'<path d="M12 2l1.8 6.2L20 10l-6.2 1.8L12 18l-1.8-6.2L4 10l6.2-1.8z"/>',
 "hair":'<path d="M7 21c0-6 2-9 5-12s4-5 3-7c3 2 4 5 2 9s-4 6-4 10h-2c0-4 2-7 3-9-2 2-5 4-5 9z"/>',
 "laser":'<path d="M13 2L4 14h6l-1 8 9-12h-6z"/>',
 "slim":'<path d="M3 9h18v6H3z"/>'}
MENU = [("skin","Medicated facials","SKIN",37.54,""),("age","Botox","ANTI-AGEING",40.79,""),("age","Fillers","ANTI-AGEING",41.30,""),
        ("age","Threads","ANTI-AGEING",41.62,""),("acne","Acne treatments","SKIN",42.87,""),("hair","PRP","HAIR",49.54,""),
        ("hair","GFC","HAIR",50.12,""),("hair","Exosomes","HAIR",50.74,""),("hair","Follicular grafting","HAIR",51.97,"NEW"),
        ("laser","Laser hair removal","BODY",54.17,""),("slim","Slimming","BODY",57.78,"SOON")]
SFX = [("impact-bass-1",1.51,0.55),("whoosh-short",2.10,0.3),("rimshot",4.42,0.45),("record_scratch",6.58,0.55),("boing",7.40,0.3),
       ("whoosh",7.38,0.35),("pop",7.55,0.3),("whoosh-short",9.95,0.35),("ping",10.10,0.25),("slurp",13.90,0.7),("whoosh-short",13.80,0.3),
       ("ping",15.95,0.35),("rimshot",16.05,0.35),("whoosh",20.08,0.4),("whoosh-cinematic",20.10,0.25),("impact-bass-1",24.91,0.4),
       ("whoosh-short",25.75,0.3),("sad_trombone",31.05,0.45),("whoosh",32.25,0.4),("whoosh",33.45,0.35),("sparkle",51.97,0.35),
       ("boing",51.95,0.25),("cash_register",58.70,0.45),("sparkle",59.85,0.4),("whoosh-cinematic",FOOT-0.3,0.35),("impact-bass-1",FOOT+0.2,0.45)]
SFX += [("whoosh-short",s0-0.02,0.3) for _,_,_,s0,_ in BROLL]
SFX += [("pop",t,0.25) for *_,t,_ in MENU]
DUR = {"impact-bass-1":2.12,"pop":0.72,"whoosh":0.57,"whoosh-short":0.57,"whoosh-cinematic":5.54,"ping":1.32,"sparkle":1.80,
       "record_scratch":1.13,"sad_trombone":3.24,"slurp":1.82,"cash_register":1.63,"boing":1.22,"rimshot":1.10}

def zone_at(t):
    if any(s0<=t<s1 for _,_,_,s0,s1 in BROLL): return "z-low"
    sh=[x for x in SHOTS if x["out"]<=t+0.001][-1]["shot"]
    if 33.5<=t<59.1: return "z-menu"          # treatment menu occupies the right side
    return {"DOC":"z-right","HOST":"z-left","WIDE":"z-low"}[sh]
def cap_html(i,s,e,words):
    lines=[]; 
    for j,(w,t,c,b) in enumerate(words):
        if lines and lines[-1][0]==b: lines[-1][1].append((j,w,c,b))
        else: lines.append([b,[(j,w,c,b)]])
    out=[]
    for b,ws in lines:
        sp="".join(f'<span class="w{(" k"+c) if c else ""}{" big" if b else ""}" id="cw{i}_{j}">{html.escape(w)}</span>' for j,w,c,b in ws)
        out.append(f'<div class="ln{" lb" if b else ""}">{sp}</div>')
    return f'<div class="cap {zone_at(s+0.05)}" id="cap{i}">{"".join(out)}</div>'
caps="\n".join(cap_html(i,*c) for i,c in enumerate(CAP))
jokes="\n".join(f'<div id="{j}" class="clip joke" data-start="{s}" data-duration="{round(e-s,3)}" data-track-index="8" style="left:{x}px;top:{y}px"><div class="jin" style="transform:rotate({r}deg)"><span class="jt">{html.escape(t)}</span><span class="je">{em}</span></div></div>' for j,s,e,t,em,x,y,r in JOKES)
stick="\n".join(f'<div id="{j}" class="clip stick" data-start="{s}" data-duration="{round(e-s,3)}" data-track-index="9" style="left:{x}px;top:{y}px"><span class="sin" style="transform:rotate({r}deg)">{em}</span></div>' for j,s,e,em,x,y,r in STICK)
br=[]
for b,kind,src,s,e in BROLL:
    d=round(e-s,3)
    if kind=="vid": br.append(f'<div class="bwrap" id="w-{b}"><video id="{b}" class="clip bvid" src="{src}" muted playsinline data-start="{s}" data-duration="{d}" data-track-index="2"></video></div>')
    else: br.append(f'<div class="bwrap" id="w-{b}"><div id="{b}" class="clip bimg" data-start="{s}" data-duration="{d}" data-track-index="2" style="background-image:url({src})"></div></div>')
cards="".join(f'<div class="card" id="mc{k}"><span class="ic"><svg viewBox="0 0 24 24">{ICON[ic]}</svg></span><span class="cl"><span class="ct">{html.escape(lab)}</span><span class="cs">{sec}</span></span>{f"<span class=\"badge {bd.lower()}\">{bd}</span>" if bd else ""}</div>' for k,(ic,lab,sec,t,bd) in enumerate(MENU))
audios="\n".join(f'<audio id="sfx{i:02d}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(DUR[n],END-t):.2f}" data-track-index="{11+i%3}" data-volume="{v}"></audio>' for i,(n,t,v) in enumerate(sorted(SFX,key=lambda x:x[1])))
music_auto=json.dumps({"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":1},{"t":6.5,"v":1},{"t":6.6,"v":0},{"t":7.35,"v":0},{"t":7.5,"v":1},
  {"t":30.9,"v":1},{"t":31.0,"v":0.15},{"t":32.2,"v":0.15},{"t":32.5,"v":1},{"t":FOOT-0.2,"v":1},{"t":FOOT+0.3,"v":1.8},{"t":END-0.6,"v":1.8},{"t":END,"v":0}]}]})
shots=[[round(s["out"],4),round(s["frames"]/30,4),s["shot"]] for s in SHOTS]
JS=dict(JS_CAPS=json.dumps([[s,e,[[t,int(b),0] for j,(w,t,c,b) in enumerate(ws)]] for (s,e,ws) in CAP]),
        JS_MENU=json.dumps([t for *_,t,_ in MENU]), JS_BROLL=json.dumps([[b,s,e] for b,_,_,s,e in BROLL]), JS_SHOTS=json.dumps(shots),
        JS_JOKES=json.dumps([[j,s,e] for j,s,e,*_ in JOKES]), JS_STICK=json.dumps([[j,s,e] for j,s,e,*_ in STICK]))
page=open(os.path.join(HERE,"template.html")).read()
for k,v in dict(END=END,FOOT=FOOT,ENDD=round(END-FOOT,3),BROLLS="\n".join(br),CAPS=caps,CARDS=cards,AUDIOS=audios,MUSIC=music_auto,
                JOKES=jokes,STICKERS=stick,**JS).items():
    page=page.replace("%%"+k+"%%",str(v))
open(os.path.join(ROOT,"index.html"),"w").write(page)
print("wrote index.html",len(CAP),"captions",len(BROLL),"broll",len(SFX),"sfx","FOOT",FOOT,"END",END)
