import sys, json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3] if len(sys.argv)>3 else 'small.en', device='cpu', compute_type='int8')
import soundfile as sf; a,_sr=sf.read(sys.argv[1], dtype="float32"); segs,_=m.transcribe(a, word_timestamps=True, language='en')
W=[]
for s in segs:
    for w in s.words: W.append(dict(w=w.word.strip(), s=round(w.start,3), e=round(w.end,3), p=round(w.probability,3)))
json.dump(W, open(sys.argv[2],'w'), indent=0); print(' '.join(x['w'] for x in W))
