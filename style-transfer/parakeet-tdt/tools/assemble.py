import json, subprocess, os, sys
P='/home/user/work/proj/'; F='/home/user/work/fonts/'
SFXF={k:P+'builder/sfx/'+k+'.mp3' for k in ['glitch','whoosh','open','click','pop','pill','card','count','zig','text']}
META=json.load(open(P+'builder/sfx_meta.json'))
LVL={'whoosh':.55,'glitch':.5,'open':.55,'click':.5,'pop':.5,'pill':.45,'card':.5,'count':.35,'zig':.4,'text':.45}
NAMES=json.load(open(P+'an/design_names.json'))
os.makedirs(P+'out/clips',exist_ok=True)
def run(a): subprocess.run(a,check=True)
def clip(bi,k):
    d=P+f'vid/b{bi+1:02d}_{k}/'; e=json.load(open(d+'events.json')); f0,f1=e['f0'],e['f1']; dur=(f1-f0)/30
    out=P+f'out/clips/b{bi+1:02d}_{k}.mp4'
    ins=['-framerate','30','-i',d+'f_%04d.jpg','-ss',f'{f0/30:.4f}','-t',f'{dur:.4f}','-i',P+'aroll/voice_edit.wav']
    fl=['[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v0]']; mix=['[v0]']; n=2
    for ev in e['ev']:
        m=META[ev['k']]; t=ev['f']/30-(m['peak'] if ev.get('peak') else m['onset'])-f0/30
        ins+=['-i',SFXF[ev['k']]]
        cut=max(0,-t); dl=int(max(0,t)*1000)
        fl.append(f"[{n}:a]atrim=start={cut:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume={LVL[ev['k']]*0.6:.3f},adelay={dl}|{dl}[s{n}]"); mix.append(f'[s{n}]'); n+=1
    fl.append(''.join(mix)+f'amix=inputs={len(mix)}:normalize=0:duration=first,atrim=end={dur:.4f}[a]')
    fl.append('[0:v]crop=1080:1920:0:0,format=yuv420p[v]')
    run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fl),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','medium','-r','30','-c:a','aac','-b:a','192k','-ar','48000',out])
    return out
def card(bi,k):
    nm=NAMES[f'{bi}'][k]; out=P+f'out/clips/c{bi+1:02d}_{k}.mp4'
    for i,t in enumerate([f'BEAT {bi+1:02d} · {k}',nm['design'],nm['beat']]): open(P+f'out/t{i}.txt','w').write(t)
    vf=(f"drawtext=fontfile={F}SairaExpandedBlackItalic.ttf:textfile={P}out/t0.txt:fontsize=96:fontcolor=0xff2e63:x=(w-tw)/2:y=760,"
        f"drawtext=fontfile={F}SairaExpandedRegular.ttf:textfile={P}out/t1.txt:fontsize=50:fontcolor=white:x=(w-tw)/2:y=900,"
        f"drawtext=fontfile={F}SairaExpandedRegular.ttf:textfile={P}out/t2.txt:fontsize=26:fontcolor=0x9d9196:x=(w-tw)/2:y=990")
    run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x141113:s=1080x1920:r=30:d=1.2','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','1.2','-vf',vf+',format=yuv420p','-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k',out])
    return out
part=int(sys.argv[1]); beats=[3*(part-1)+i for i in range(3)]
lst=[]
for bi in beats:
    for k in 'ABC': lst+= [card(bi,k), clip(bi,k)]
open(P+'out/list.txt','w').write(''.join(f"file '{x}'\n" for x in lst))
raw=P+f'out/raw{part}.mp4'
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',P+'out/list.txt','-c','copy',raw])
final=P+f"out/Part {part} - beats {beats[0]+1}-{beats[-1]+1} - designs A B C.mp4"
run(['ffmpeg','-v','error','-y','-i',raw,'-c:v','copy','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',final])
print(final)
