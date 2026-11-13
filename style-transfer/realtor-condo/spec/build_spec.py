# Single source of truth for the reference measurements -> markdown specs + web/style.json
import json
META=dict(file='Video_by_brandbuddiestudio_DWIu4iwk81P.mp4',res='720x1280 (measured, reported in 1080x1920 space = x1.5)',fps=30,frames=756,dur=25.2,
          lang='Hindi/Hinglish',lufs_mix=-14.1,lufs_voice=-14.2,lufs_rest=-31.8)
CUTS=[ # first,last,type,content,transition-in,graphics
 (1,118,'speaker','walking MCU, street A','hard (start)','hook page f1-49, blur-swap f49-54, Social media page f55-118'),
 (119,257,'speaker','street A, wider walking','blue light-leak f108-126 (cut under white at f119-120)','Aaj kal sirf / IG post cards / Post / Right ads+content cards'),
 (258,328,'speaker','new location (grey wall)','HARD cut f258','Yahi per / logo disc / Studio'),
 (329,474,'speaker','street B (white bldg)','blue light-leak f319-335','UI profile card / Hum apka complete Social media / Performance marketing pill + chart'),
 (475,604,'speaker','street A pillars','blue light-leak f465-478','Aur best part / humari services / Start hoti hai / counter 0->30000 Rs / Per month se'),
 (605,733,'speaker','street A pillars wide','warm (pink/orange) light-leak f599-610, white-out f601-604','So if you / want to boost / coin / Your business / online / DM US RIGHT NOW / get started'),
 (734,756,'black','end card black','hard','none'),
]
COMP={
 'slideX':dict(what='big accent word, gradient fill, BEHIND the subject (head occludes it)',from_px=-745,axis='x',ease='expo.out',dur_f=20.9,t0='word spoken -0..2f',blur='motion blur while moving (~18px at peak)',src='S01 Dehradun right edge 250->990, rms 7.6px'),
 'riseWord':dict(what='word-by-word rise, used for big behind-head words',from_px=64,axis='y',ease='circ.out',dur_f=21.4,opacity='0->1 in ~4f',stagger='per spoken word',src='S03 Aaj top 760->696, rms 0.4px'),
 'snapRise':dict(what='very fast snap-up of a big word + per-letter random reveal',from_px=218,axis='y',ease='power2.out',dur_f=3,letters='random-order fade over ~5f',src='S02 Social media top 669->452'),
 'springRise':dict(what='coloured accent word springs up',from_px=127,axis='y',ease='back.out(1.7)',dur_f=5.7,overshoot_px=-12,src='S09 Your business 1066->939, settles f657'),
 'sideSlide':dict(what='small coloured side word slides in from the right',from_px=309,axis='x',ease='expo.out',dur_f=9.5,src='S01 Business x0 1014->705'),
 'typeOn':dict(what='light captions / labels / CAPS CTA typed letter by letter',rate='~1.2 chars per frame',cursor=False,src='S01 chala rahe ho f37-47, S04 labels, S10 DM US'),
 'letterRTL':dict(what='giant word revealed letter by letter from the right',dur_f=11,src='S05 Studio x0 493->55 f284-295'),
 'cameraPunchOut':dict(what='whole frame (footage+graphics) zooms out',scale_from=1.15,scale_to=1.0,ease='circ.out',dur_f=4.7,at='~0.9s into hook (f27)',src='S01 Dehradun width 896->779, rms 1.3'),
 'pageExit':dict(what='caption page leaves: scale 1->0.92, blur 0->10px, opacity 1->0',dur_f=5,src='S01->S02 f49-54'),
 'iconRow':dict(what='3 app-icon tiles slide in L->R staggered, settle',stagger_f=1,dur_f=5,src='S02 f55-60'),
 'cardDrop':dict(what='post cards drop in from above one by one on a dark panel',stagger_f=4,dur_f=6,ease='back.out(1.7)',src='S03 f150-160'),
 'mediaCard':dict(what='rounded media card slides in from the side with a green tint flash; green label types on above; thin white arc links cards',dur_f=8,src='S04 f196-240'),
 'logoDrop':dict(what='white disc badge drops from above with one bounce',dur_f=8,ease='back.out(1.7)',src='S05 f282-290'),
 'uiCardPop':dict(what='glassy UI card scales 0.6->1 with overshoot',dur_f=6,ease='back.out(1.7)',src='S06 f336-346'),
 'pillChart':dict(what='white pill (r=full) with gradient text + white line chart drawn behind the subject',chart_draw_f=40,pill_pop_f=5,src='S07 f379-460'),
 'counter':dict(what='big number counts 0->N with a circular progress ring and small suffix',dur_f=27,ease='power2.out',ring='green->purple stroke 0->100%',src='S08 f540-573'),
 'coinRoll':dict(what='3D coin rolls in from the left',dur_f=8,src='S09 f640-650'),
 'lightLeak':dict(what='screen-blended light leak sweeps in from right to white-out, cut underneath, decays',build_f=12,white_f=2,decay_f=8,colors={'blue':['#1a6cff','#7fd3ff','#ffffff'],'warm':['#ff2d6a','#ff9a3c','#ffffff']},src='f108-126, f319-335, f465-478, f599-610'),
}
PAL={'cyan':['#5fd8ff','#1dc3f2','#139fdc'],'blue':['#4aa8ff','#2687e6','#1f5fd6'],'green':'#7cf13e','studio':['#e8a26e','#da996f','#d1466f'],
     'violet':['#3f6bff','#6a3cff'],'pillText':['#c2189b','#2d5be3'],'white':'#ffffff','ring':['#7cf13e','#7a3cff'],'labelGreen':'#58e04a'}
TYPO=[('accent big word','Bricolage Grotesque',800,220,'cap 145px, tracking -0.03em, gradient fill'),
      ('headline white','Bricolage Grotesque',800,125,'So if you (xh 66)'),
      ('line bold white','Bricolage Grotesque',800,98,'Aur best part (xh 52), mein apna 81'),
      ('sub bold white','Bricolage Grotesque',700,75,'Start hoti hai (xh 40)'),
      ('light caption','Bricolage Grotesque',300,62,'chala rahe ho 79 / humari services 62 / want to boost 57'),
      ('colour accent mid','Bricolage Grotesque',800,132,'Your business (cap 87)'),
      ('CAPS CTA','Bricolage Grotesque',800,133,'DM US RIGHT NOW (cap 88)'),
      ('counter','Bricolage Grotesque',800,188,'30000 (cap 124) + Rs 70px'),
      ('side word','Bricolage Grotesque',800,72,'Business (green)'),
      ('pill text','Bricolage Grotesque',700,44,'Performance marketing, pill h 64, pad 30')]
SECT=[
 ('S01','Hook',1,54,['zoom-in start? no: starts at rest','slideX big cyan word "Dehradun" behind head (y 468-613)','line bold white "mein apna" above (y 453-516) rise','sideSlide green "Business" right (x 705-1017, y 675-735)','3D emoji (hourglass) pops top-right, rotates in','typeOn light caption "chala rahe ho" at chest (y 924-985)','cameraPunchOut 1.15->1 at f27','pageExit f49-54']),
 ('S02','Icons + big blue word',55,118,['iconRow YT/FB/IG above head (y ~330-420)','snapRise + random letters "Social media" blue, behind head','typeOn light "customer" / "nahi arahe" at chest (y 883-922)','blue lightLeak out f108']),
 ('S03','Word-by-word + post cards',126,192,['riseWord "Aaj kal sirf" blue behind head','cardDrop 3 IG post cards on dark panel above head','light "dal dene se" + blue bold "Post" + white bold "Kam nai chalta !!" stack at chest']),
 ('S04','Two media cards + labels',193,257,['mediaCard right then left (x 1260-? / 30-?)','green labels type on "Right content" / "Right ads"','white arc connecting','light typeOn "bhi jaruri hai" at chest']),
 ('S05','Logo disc + giant gradient word',258,328,['HARD cut','light "Yahi per" at chest','logoDrop disc top centre (d ~ 230px)','letterRTL "Studio" orange->pink giant behind head','light "apki help karta hai"','blue lightLeak out f319']),
 ('S06','UI card + complete social media',329,378,['uiCardPop green glass profile card top (x 45-490, y 105-390)','bold white "Hum apka" at chin','"complete" white right','"Social media" violet gradient at chest']),
 ('S07','Pill + line chart',379,470,['white pill "Performance marketing" gradient text at chest (y ~ 1000)','line chart axis + polyline draws behind subject','blue lightLeak out f465']),
 ('S08','Counter',478,600,['bold "Aur best part" + light "humari services" above-right + bold "Start hoti hai" below-left (stacked, staggered)','counter 0->30000 + "Rs" + ring above head','light "Per month se" at chest','warm lightLeak out f599']),
 ('S09','Headline + spring accent',605,676,['slide-in from right "So if you" white headline','light "want to boost" right-aligned below','coinRoll left','springRise "Your business" blue','light "online"']),
 ('S10','CTA',677,733,['typeOn CAPS "DM US RIGHT NOW" white at chest','light "get started" above-right','end hard to black f734']),
]
AUDIO=dict(mix=-14.1,voice=-14.2,rest=-31.8,music_below_voice_dB=17.6,ducking='none detected',
 hits=[(3,'whoosh','hook slideX'),(27,'whoosh/air','camera punch-out'),(56,'pop','icon row'),(60,'pop','letters'),(77,'tick','typeOn'),(125,'whoosh tail','light-leak'),(150,'pop','card drop'),(164,'pop','card'),(211,'swish','media card'),(217,'swish','media card 2'),(281,'thud/pop','logo drop'),(296,'whoosh','Studio reveal'),(384,'click','pill'),(464,'whoosh','light-leak'),(503,'click','line'),(524,'click','line'),(534,'tick roll','counter start'),(607,'whoosh','warm leak'),(728,'glitch tail','end')],
 lead='text appears 0-12 f before the spoken word (mean ~4 f)')
open('spec/CUTS.md','w').write('# CUTS — reference\n\n'+json.dumps(META)+'\n\n| # | first | last | time | len | type | content | transition in | graphics |\n|---|---|---|---|---|---|---|---|---|\n'+''.join(f'| {i+1} | {a} | {b} | {(a-1)/30:.2f}-{b/30:.2f}s | {b-a+1}f | {t} | {c} | {tr} | {g} |\n' for i,(a,b,t,c,tr,g) in enumerate(CUTS))+'\nCadence: true 30 fps (no duplicated frames in speaker shots). No full-screen b-roll, no splits: 100% speaker with overlay graphics.\n')
for sid,name,a,b,items in SECT:
    open(f'spec/{sid}.md','w').write(f'# {sid} — {name} (f{a}-{b}, {(a-1)/30:.2f}-{b/30:.2f}s)\n\n'+''.join('- '+x+'\n' for x in items)+'\n```json\n'+json.dumps(dict(id=sid,f0=a,f1=b,elements=items))+'\n```\n')
open('spec/STYLE.md','w').write('# STYLE — reference summary\n\n## Palette\n'+''.join(f'- {k}: {v}\n' for k,v in PAL.items())+'\n## Typography (Bricolage Grotesque, NCC 0.78 = best of 20 Google candidates; ref is soft 720p)\n| role | family | wt | px@1080 | note |\n|---|---|---|---|---|\n'+''.join(f'| {r} | {f} | {w} | {s} | {n} |\n' for r,f,w,s,n in TYPO)+'\n## Components (canonical motion)\n'+''.join(f'- **{k}**: '+json.dumps(v)+'\n' for k,v in COMP.items())+'\n## Global rules\n- 100% speaker footage; every section = one caption "page"; page swaps by blur-exit (5f) or a light-leak at shot changes.\n- Big accent words sit BEHIND the subject (depth layer), around forehead/hair height; small text sits at chest, never over the face.\n- Words appear word-by-word/letter-by-letter in sync with speech; light captions type on.\n- A new page every 2-3 s; light-leak at each location change (4 of 5 cuts).\n- Grade: untouched footage, slight warm, no vignette.\n')
open('spec/AUDIO.md','w').write('# AUDIO — reference\n\n'+json.dumps({k:v for k,v in AUDIO.items() if k!='hits'})+'\n\n| frame | type | sits on |\n|---|---|---|\n'+''.join(f'| {f} | {t} | {s} |\n' for f,t,s in AUDIO['hits'])+'\n')
json.dump(dict(meta=META,cuts=CUTS,components=COMP,palette=PAL,typo=TYPO,sections=SECT,audio=AUDIO),open('web/style.json','w'))
print('ok')
