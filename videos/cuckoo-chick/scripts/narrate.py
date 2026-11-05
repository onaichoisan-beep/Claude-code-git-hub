"""Shared helper for NARRATED pixel shorts (story mode, STYLE_GUIDE.md sections 7 + 9).

    import narrate as NR
    S = NR.Story(ROOT, gaps={...}, gold={...}, red={...}, start=0.25)   # lays out assets/audio/vo/NN.wav (Kokoro)
    A, W, E, Bn = S.A, S.W, S.E, S.B                                    # line start / word start / word end / line end
    S.finalize(B, tail=1.0)  -> sets DUR, STOP, REWIND, writes nothing yet; returns DUR
    ... from sfxlib import *; build fx/amb buses (time-keyed to A()/W()) ...
    S.mix(fx, amb, master, write_wav, band, reverb, B)                 # voice + ducked SFX -> mix.wav, captions.js, BEATS

Voice: Kokoro-82M af_heart (the most human of the open voices). Light handling only: every line levelled, a gentle
70 Hz-14 kHz band, a touch of small-room reverb, natural pauses kept up to 0.45 s (no robotic squeezing).
Captions: 1-3 words per card, a new card at every comma/full stop, *gold* keywords, red danger words.
"""
import json
import os
import re
import sys
import wave

import numpy as np

import voicelib as V


class Story:
    def __init__(self, root, gaps=None, gold=(), red=(), start=0.25, max_pause=0.45, per_card=3):
        self.root = root
        self.lines = json.load(open(os.path.join(root, "scripts", "lines.json")))
        self.clips = V.layout(os.path.join(root, "assets", "audio", "vo"), self.lines, start=start, gaps=gaps or {},
                              max_pause=max_pause)
        K = V.Words(self.clips)
        self.A, self.W, self.E, self.B = K.A, K.B and K.W, K.E, K.B
        self.A, self.W, self.E, self.B = K.A, K.W, K.E, K.B
        self.gold = {g.lower() for g in gold}
        self.red = {r.lower() for r in red}
        self.per_card = per_card

    def caps(self):
        out = []
        for c in self.clips:
            chunks, cur = [], []
            for w in c["w"]:
                cur.append(w[0])
                if re.search(r"[.,!?]$", w[0]) or len(cur) == self.per_card or sum(len(x) + 1 for x in cur) > 15:
                    chunks.append(cur)
                    cur = []
            if cur:
                chunks.append(cur)
            res = []
            for ch in chunks:
                words = []
                for w in ch:
                    k = re.sub(r"[^a-z0-9']", "", w.lower())
                    words.append(f"*{w.upper()}*" if k in self.gold or k in self.red else w.upper())
                res.append((" ".join(words).replace("* *", " "), re.sub(r"[^A-Za-z0-9']", "", ch[0]).lower() or ch[0]))
            out.append(res)
        return out

    def finalize(self, B, tail=1.0):
        B["STOP"] = round(self.clips[-1]["b"] + tail, 3)
        B["REWIND"] = round(B["STOP"] + 0.7, 3)
        self.DUR = round(float(np.ceil((B["REWIND"] + 0.45) * 10) / 10), 1)
        for i in range(len(self.clips)):
            B.setdefault(f"L{i}", round(self.A(i), 3))
        print(f"voice ends {self.clips[-1]['b']:.2f}s -> DUR {self.DUR}")
        return self.DUR

    def mix(self, fx, amb, master, write_wav, band, reverb, B, SR, N, sfx_gain=0.8, duck_depth=0.5, room=0.08):
        tracks = V.voice_tracks(self.clips, SR, N, band, level_db=-14.0)
        for k in tracks:
            tracks[k] = reverb(tracks[k], length=0.5, wet=room)[:N]
        voice = sum(tracks.values())
        duck = V.duck_env(voice, SR, depth=duck_depth)
        captions = V.make_captions(self.clips, self.caps(), self.DUR, hold=0.25)
        # a soft tick on every caption card (sound on every change)
        import chiptune as CT
        CT.card_blips(fx, [(c["a"], c["b"], "") for c in captions], gain=0.05)
        tmp = os.path.join(self.root, "assets", "audio", "sfx.wav")
        master(amb, fx, tmp, amb_gain=1.0, makeup_db=5.0)
        with wave.open(tmp, "rb") as w:
            sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
        os.remove(tmp)
        V.finish(sfx, voice, duck, os.path.join(self.root, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=sfx_gain, makeup_db=2.0)
        V.write_captions_js(os.path.join(self.root, "captions.js"), self.DUR, captions, self.clips, V.mouths(tracks, SR))
        with open(os.path.join(self.root, "captions.js"), "a") as f:
            f.write("window.BEATS = " + json.dumps({k: (round(v, 3) if not isinstance(v, list) else [round(x, 3) for x in v]) for k, v in B.items()}) + ";\n")
        for i, c in enumerate(self.clips):
            print(f"  {i:02d} {c['a']:6.2f}-{c['b']:6.2f}  {self.lines[i][1]}")
        print("DUR", self.DUR, "captions", len(captions))
