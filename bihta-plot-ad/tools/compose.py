# Regenerates the video track + timeline script of index.html from timeline.json
import json, re
P="/home/user/Claude-code-git-hub/bihta-plot-ad/"
d=json.load(open(P+"timeline.json")); T=d['cues']; T['aaj']=T['L9']
html=open(P+"index.html").read()
vids=[]; cam=[]; n=0; face_k=0
for x in d['shots']:
    if x['type']!="video": continue
    n+=1; w=f"w{n}"
    rate=f' data-playback-rate="{x["rate"]}"' if x['rate']!=1 else ''
    vids.append(f'      <div class="vw" id="{w}"><video id="v{n}" src="assets/clips/{x["clip"]}.mp4" muted playsinline data-start="{x["start"]}" data-duration="{x["dur"]}" data-media-start="{x["mi"]}"{rate} data-track-index="{1 if x.get("fadein") else 0}"></video></div>')
    mir=-1 if x['mirror'] else 1
    if x['face']:
        z=1.0 if face_k%2==0 else 1.12; face_k+=1
        cam.append(f'      tl.set("#{w}", {{ scale: {z}, scaleX: {z*mir} }}, {x["start"]});')
    else:
        a,b=(x['zoom'],1.0) if x['zoom']>1.12 else (1.0,max(x['zoom'],1.1))
        cam.append(f'      tl.fromTo("#{w}", {{ scaleY: {a}, scaleX: {a*mir} }}, {{ scaleY: {b}, scaleX: {b*mir}, duration: {x["dur"]}, ease: "none" }}, {x["start"]});')
    if x.get('fadein'): cam.append(f'      tl.fromTo("#{w}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.45, ease: "none" }}, {x["start"]});')
html=re.sub(r'(<!-- ===== VIDEO TRACK[^\n]*\n)(.*?)(\n\s*<div class="shadeTop">)', lambda m: m.group(1)+"\n".join(vids)+m.group(3), html, flags=re.S)
html=re.sub(r'(\n\s*root\.dataset\.x = 0;)?', '', html)
html=re.sub(r'data-duration="[0-9.]+"( data-track-index="5")', f'data-duration="{d["total"]}"\\1', html)
html=re.sub(r'data-duration="[0-9.]+"( data-track-index="6")', f'data-duration="{d["total"]}"\\1', html)
html=re.sub(r'(data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration=")[0-9.]+', f'\\g<1>{d["total"]}', html)
html=re.sub(r'const T = \{.*?\};', 'const T = '+json.dumps(T)+';', html, flags=re.S)
html=re.sub(r'(// ---- camera \(generated\) ----\n)(.*?)(\n\s*// ---- end camera ----)', lambda m: m.group(1)+"\n".join(cam)+m.group(3), html, flags=re.S)
open(P+"index.html","w").write(html)
print(len(vids),"video shots")
