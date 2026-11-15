import json,os
os.environ['HF_HOME']='/home/user/.hfcache'
import soundfile as sf
from faster_whisper import WhisperModel
a,_=sf.read('aroll/voice16.wav',dtype='float32')
m=WhisperModel('large-v3',device='cpu',compute_type='int8',cpu_threads=4)
segs,info=m.transcribe(a,language='en',word_timestamps=True,vad_filter=False,condition_on_previous_text=False,
  initial_prompt="So I recently turned 25, and I really thought ki koi mere liye surprise plan karega. Mai Pinterest pagal hu na, mujhe realistic hona aata hi nahi hai.")
out=[]
for s in segs:
    print('%.2f-%.2f %s'%(s.start,s.end,s.text),flush=True)
    for w in s.words: out.append(dict(w=w.word.strip(),s=round(w.start,3),e=round(w.end,3),p=round(w.probability,3)))
json.dump(out,open('aroll/words_en.json','w'),ensure_ascii=False)
