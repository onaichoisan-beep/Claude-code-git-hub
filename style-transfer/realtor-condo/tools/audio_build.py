import json,subprocess,numpy as np,soundfile as sf
SR=48000
subprocess.run(['ffmpeg','-v','error','-y','-i','aroll/voice.wav','-af','highpass=f=70,afftdn=nf=-30,acompressor=threshold=-22dB:ratio=3:attack=5:release=80,equalizer=f=3000:t=q:w=1:g=2.5,loudnorm=I=-15:TP=-2,aresample=48000','-ac','2','audio/voice_proc.wav'],check=True)
v,_=sf.read('audio/voice_proc.wav'); N=len(v)
GAIN={'whoosh':.55,'punch':.5,'swish':.45,'leak':.6,'riser':.35,'click':.6,'drop':.55,'icons':.5,'uicard':.5,'card':.5,'paper':.55,'count':.55,'type':.28,'coin':.5,'chart':.35,'letters':.45}
ev=json.load(open('render/ev.json')); sfx=np.zeros((N,2)); rng=np.random.default_rng(3); cache={}
for e in ev:
    n=e['name']
    if n not in cache:
        subprocess.run(['ffmpeg','-v','error','-y','-i',f'web/media/sfx/{n}.mp3','-ar',str(SR),'-ac','2',f'audio/sfx_{n}.wav'],check=True)
        cache[n]=sf.read(f'audio/sfx_{n}.wav')[0]
    s=cache[n]; st=int(rng.uniform(-.7,.7)*0) # fixed pitch in the master
    i=int(e['f']/30*SR); seg=s[:max(0,N-i)]; sfx[i:i+len(seg)]+=seg*GAIN.get(n,.5)*0.6
sf.write('audio/sfx_bus.wav',sfx,SR)
mix=v+sfx; sf.write('audio/mix_pre.wav',mix,SR)
subprocess.run(['ffmpeg','-v','error','-y','-i','audio/mix_pre.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000','audio/mix.wav'],check=True)
print(len(ev),'sfx events')
