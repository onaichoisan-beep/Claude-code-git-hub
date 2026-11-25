import sys, numpy as np, subprocess, json
from faster_whisper import WhisperModel
m=WhisperModel("small",compute_type="int8")
res={}
for f in sys.argv[2:]:
    a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout,np.int16).astype(np.float32)/32768
    segs,_=m.transcribe(a,language="hi",word_timestamps=True,vad_filter=False,initial_prompt="IIT Bihta, NSMCH, AIIMS, NIT, Kampa Golambar, NH-139, SH-78, Patna, Aurangabad, ₹6 लाख, plot")
    res[f.split('/')[-1]]=[(w.word.strip(),round(w.start,2),round(w.end,2)) for s in segs for w in s.words]
json.dump(res,open(sys.argv[1],"w"),ensure_ascii=False)
for k,v in res.items(): print(k, ' '.join(f"{w}@{s}" for w,s,e in v))
