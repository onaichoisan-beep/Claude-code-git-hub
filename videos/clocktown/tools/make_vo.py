"""Generate the narration line by line with edge-tts, then join with short gaps.
Usage: python make_vo.py SCRIPT.json out_dir   (needs edge-tts; writes vo.wav + lines.json)"""
import json, os, ssl, subprocess, sys, asyncio
import edge_tts, edge_tts.communicate
ca = "/root/.ccr/ca-bundle.crt"
if os.path.exists(ca):
    edge_tts.communicate._SSL_CTX = ssl.create_default_context(cafile=ca)
VOICES = {  # speaker -> (voice, rate, pitch)
    "n": ("en-US-AndrewNeural", "+0%", "+22Hz"),
    "mom": ("en-US-JennyNeural", "+0%", "+0Hz"),
    "mia": ("en-US-AnaNeural", "+6%", "+0Hz"),
    "mayor": ("en-US-ChristopherNeural", "-6%", "-14Hz"),
}
GAP = 0.3
lines = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out + "/lines", exist_ok=True)
async def gen(i, spk, text):
    v, r, p = VOICES[spk]
    mp3 = f"{out}/lines/{i:02d}.mp3"
    for attempt in range(6):  # the service drops requests now and then
        try:
            await edge_tts.Communicate(text, v, rate=r, pitch=p).save(mp3); break
        except edge_tts.exceptions.NoAudioReceived:
            await asyncio.sleep(1.5 * (attempt + 1))
    else:
        raise SystemExit(f"no audio for line {i}")
    wav = mp3[:-4] + ".wav"
    # trim leading/trailing silence so the pacing stays tight
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af",
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
        "-ar", "44100", "-ac", "1", wav], check=True)
    return wav
async def main():
    wavs = [await gen(i, s, t) for i, (s, t) in enumerate(lines)]
    meta, t, parts = [], 0.0, []
    for (s, txt), w in zip(lines, wavs):
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", w]))
        meta.append({"speaker": s, "text": txt, "start": round(t, 3), "end": round(t + d, 3)})
        parts.append(w); t += d + GAP
    lst = f"{out}/lines/list.txt"
    sil = f"{out}/lines/gap.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(GAP), sil], check=True)
    with open(lst, "w") as f:
        for p in parts: f.write(f"file '{os.path.abspath(p)}'\nfile '{os.path.abspath(sil)}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", f"{out}/vo.wav"], check=True)
    json.dump(meta, open(f"{out}/lines.json", "w"), indent=1)
    print("total", round(t, 2), "s")
asyncio.run(main())
