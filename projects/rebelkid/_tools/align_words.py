# word timing: whisper large-v3 (language=hi) over the whole voice gives speech intervals;
# each burned-caption cue's Roman words are placed along the speech inside that cue by character share.
import os,json;os.environ['HF_HOME']='/home/user/.hfcache'
import soundfile as sf
from faster_whisper import WhisperModel
a,_=sf.read('aroll/voice16.wav',dtype='float32')
m=WhisperModel('large-v3',device='cpu',compute_type='int8',cpu_threads=4)
segs,_=m.transcribe(a,language='hi',word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
W=[]
for s in segs:
    for w in s.words: W.append((w.start,w.end,w.word))
json.dump(W,open('aroll/whisper_hi_words.json','w'),ensure_ascii=False)
print('whisper words',len(W))
