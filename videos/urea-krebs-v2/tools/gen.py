import json, sys, time, torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
torch.manual_seed(7)
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
S = json.load(open("script.json"))
only = sys.argv[1:]
for i, (k, dv, ro) in enumerate(S):
    if only and k not in only: continue
    t = time.time()
    wav = m.generate(dv, language_id="hi", audio_prompt_path="ref.wav", exaggeration=0.75, cfg_weight=0.35, temperature=0.8)
    torchaudio.save(f"{i}_{k}.wav", wav, m.sr)
    print(k, round(wav.shape[-1] / m.sr, 2), "s, took", round(time.time() - t, 1), flush=True)
