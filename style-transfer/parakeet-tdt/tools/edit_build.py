import json, subprocess
cuts=[(10.3333,10.4333),(15.7333,15.8),(27.7667,27.8333)]   # removed ranges (frame-aligned, inside silences)
dur=29.9087
keep=[];a=0
for s,e in cuts: keep.append((a,s)); a=e
keep.append((a,dur))
vf=[];af=[]
for i,(s,e) in enumerate(keep):
    vf.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}]")
    af.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={e-s-0.005}:d=0.005[a{i}]")
n=len(keep); fc=';'.join(vf+af)+';'+''.join(f'[v{i}][a{i}]' for i in range(n))+f'concat=n={n}:v=1:a=1[v][a]'
subprocess.run(['ffmpeg','-v','error','-y','-i','src/client.mp4','-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-crf','12','-preset','fast','-r','30','-c:a','pcm_s16le','aroll/rough_edit.mov'],check=True)
def o2e(t):
    off=0
    for s,e in cuts:
        if t>=e: off+=e-s
        elif t>s: return s-off
    return t-off
W=json.load(open('aroll/words_raw.json'))
for w in W: w['s']=round(o2e(w['s']),3); w['e']=round(o2e(w['e']),3)
json.dump({'cuts':cuts,'keep':keep,'edit_dur':round(dur-sum(e-s for s,e in cuts),3),'words':W},open('aroll/edl.json','w'))
F=json.load(open('aroll/faces.json'))
# faces in edit time: drop the removed frames
idx=[i for i in range(len(F['chin'])) if not any(s<=i/30<e for s,e in cuts)]
json.dump({'chin':[F['chin'][i] for i in idx],'top':[F['faces'][i][0] for i in idx]},open('aroll/faces_edit.json','w'))
print('edit dur',dur-sum(e-s for s,e in cuts))
