import json, sys, torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
S = {k: (i, dv) for i, (k, dv, ro) in enumerate(json.load(open("script.json")))}
for k, maxdur in [("back", 3.6), ("cta", 3.6)]:
    i, dv = S[k]; best = None
    for seed in [11, 23, 42, 77]:
        torch.manual_seed(seed)
        wav = m.generate(dv, language_id="hi", audio_prompt_path="ref.wav", exaggeration=0.75, cfg_weight=0.35, temperature=0.8)
        d = wav.shape[-1] / m.sr
        print(k, seed, round(d, 2), flush=True)
        if best is None or abs(d - 2.8) < abs(best[0] - 2.8): best = (d, wav)
        if d <= maxdur: break
    torchaudio.save(f"{i}_{k}.wav", best[1], m.sr)
    print("kept", k, round(best[0], 2), flush=True)
