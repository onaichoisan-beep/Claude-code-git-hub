import os;os.environ['HF_HOME']='/home/user/.hfcache'
import subprocess,soundfile as sf
subprocess.run(['ffmpeg','-v','error','-y','-i','src/ref.mp4','-t','12','-ac','1','-ar','16000','audio/ref12.wav'])
from faster_whisper import WhisperModel
a,_=sf.read('audio/ref12.wav',dtype='float32')
m=WhisperModel('large-v3',device='cpu',compute_type='int8',cpu_threads=4)
s,_=m.transcribe(a,language='en',word_timestamps=True)
for x in s:
  for w in x.words: print('%.2f %.2f f%d %s'%(w.start,w.end,int(w.start*30)+1,w.word))
