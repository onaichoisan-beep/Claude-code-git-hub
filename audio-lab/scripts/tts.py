"""Generate narration with offline (Kokoro, Piper) or online (Edge) voices.

  python tts.py --engine kokoro --voice am_michael --speed 1.15 --text "..." -o out.wav
  python tts.py --engine piper  --voice en_US-ryan-high --text-file script.txt -o out.wav
  python tts.py --engine edge   --voice en-US-AndrewNeural --rate +15% --pitch +10Hz --text "..." -o out.mp3
  python tts.py --list kokoro|piper|edge
"""
import argparse, asyncio, os, subprocess, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = os.path.join(HERE, "..", "voices")
KOKORO_MODEL = os.path.join(VOICES, "kokoro", "kokoro-v1.0.onnx")
KOKORO_VOICES = os.path.join(VOICES, "kokoro", "voices-v1.0.bin")
PIPER_DIR = os.path.join(VOICES, "piper")


def kokoro(text, voice, speed, out):
    import soundfile as sf
    from kokoro_onnx import Kokoro
    samples, sr = Kokoro(KOKORO_MODEL, KOKORO_VOICES).create(text, voice=voice, speed=speed, lang="en-us")
    sf.write(out, samples, sr)


def piper(text, voice, speed, out):
    from piper import PiperVoice, SynthesisConfig
    v = PiperVoice.load(os.path.join(PIPER_DIR, voice + ".onnx"))
    with wave.open(out, "wb") as wf:
        v.synthesize_wav(text, wf, syn_config=SynthesisConfig(length_scale=1 / speed))


def edge(text, voice, rate, out, pitch="+0Hz"):
    import ssl, edge_tts, edge_tts.communicate
    ca = os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt"
    if os.path.exists(ca):  # sandbox TLS proxy: edge-tts otherwise trusts only certifi's store
        edge_tts.communicate._SSL_CTX = ssl.create_default_context(cafile=ca)
    mp3 = out if out.endswith(".mp3") else out + ".mp3"
    asyncio.run(edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(mp3))
    if mp3 != out:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, out], check=True)
        os.remove(mp3)


def list_voices(engine):
    if engine == "kokoro":
        from kokoro_onnx import Kokoro
        print("\n".join(sorted(Kokoro(KOKORO_MODEL, KOKORO_VOICES).get_voices())))
    elif engine == "piper":
        print("\n".join(sorted(f[:-5] for f in os.listdir(PIPER_DIR) if f.endswith(".onnx"))))
    else:
        import edge_tts
        vs = asyncio.run(edge_tts.list_voices())
        print("\n".join(f"{v['ShortName']}\t{v['Gender']}" for v in vs if v["Locale"].startswith("en-")))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--engine", choices=["kokoro", "piper", "edge"], default="kokoro")
    p.add_argument("--voice", default="am_michael")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--rate", default="+0%", help="edge only, e.g. +15%%")
    p.add_argument("--pitch", default="+0Hz", help="edge only, e.g. +20Hz")
    p.add_argument("--text")
    p.add_argument("--text-file")
    p.add_argument("-o", "--out", default="out.wav")
    p.add_argument("--list", choices=["kokoro", "piper", "edge"])
    a = p.parse_args()
    if a.list:
        list_voices(a.list); sys.exit()
    text = a.text or open(a.text_file).read().strip()
    if a.engine == "kokoro":
        kokoro(text, a.voice, a.speed, a.out)
    elif a.engine == "piper":
        piper(text, a.voice, a.speed, a.out)
    else:
        edge(text, a.voice, a.rate, a.out, a.pitch)
    print(a.out)
