import os;os.environ['HF_HOME']='/home/user/.hfcache'
import soundfile as sf
from faster_whisper import WhisperModel
a,sr=sf.read('aroll/voice16.wav',dtype='float32');a=a[int(54.5*sr):int(59.2*sr)]
m=WhisperModel('large-v3',device='cpu',compute_type='int8',cpu_threads=4)
s,_=m.transcribe(a,language='hi',word_timestamps=True)
for x in s:
  for w in x.words: print(round(w.start+54.5,2),round(w.end+54.5,2),w.word)
