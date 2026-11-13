import json, subprocess
P='/home/user/work/proj/'
META=json.load(open(P+'builder/sfx_meta.json'))
LVL={'whoosh':.55,'glitch':.5,'open':.55,'click':.5,'pop':.5,'pill':.45,'card':.5,'count':.35,'zig':.4,'text':.45}
ev=json.load(open(P+'vid/full/events.json'))
def run(a): subprocess.run(a,check=True)
# voice chain (skill ch.9)
run(['ffmpeg','-v','error','-y','-i',P+'aroll/voice_edit.wav','-af','highpass=f=70,afftdn=nr=10,acompressor=threshold=-22dB:ratio=3:attack=5:release=80,equalizer=f=3000:t=q:w=1:g=2.5,loudnorm=I=-15:TP=-2','-ar','48000','-ac','2',P+'audio/voice_proc.wav'])
ins=['-i',P+'audio/voice_proc.wav'];fl=[];mix=['[0:a]'];n=1
for e in ev:
    m=META[e['k']]; t=e['f']/30-(m['peak'] if e.get('peak') else m['onset'])
    ins+=['-i',P+'builder/sfx/'+e['k']+'.mp3']; cut=max(0,-t); dl=int(max(0,t)*1000)
    fl.append(f"[{n}:a]atrim=start={cut:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume={LVL[e['k']]*0.6:.3f},adelay={dl}|{dl}[s{n}]"); mix.append(f'[s{n}]'); n+=1
fl.append(''.join(mix)+f'amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]')
run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fl),'-map','[a]','-ar','48000',P+'audio/mix.wav'])
out=P+'out/Parakeet TDT reel v1.mp4'
run(['ffmpeg','-v','error','-y','-framerate','30','-i',P+'vid/full/f_%04d.jpg','-i',P+'audio/mix.wav','-vf','crop=1080:1920:0:0,format=yuv420p','-c:v','libx264','-crf','15','-preset','slow','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','320k','-shortest','-movflags','+faststart',out])
print(out, len(ev),'sfx')
