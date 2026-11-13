import sys,json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3],device='cpu',compute_type='int8')
import soundfile as sf
a,_sr=sf.read(sys.argv[1],dtype="float32")
segs,_=m.transcribe(a,word_timestamps=True,language=sys.argv[4] if len(sys.argv)>4 else None)
W=[]
for s in segs:
    for w in s.words: W.append(dict(w=w.word.strip(),s=round(w.start,3),e=round(w.end,3),p=round(w.probability,2)))
json.dump(W,open(sys.argv[2],'w'),indent=0)
print(' '.join(x['w'] for x in W))
