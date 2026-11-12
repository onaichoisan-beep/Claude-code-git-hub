"""Builds assets/audio/mix.wav: dialogue + Mixkit music bed + timed Mixkit SFX, mastered to -14 LUFS."""
import subprocess, json, os, sys
A = os.path.join(os.path.dirname(__file__), "..", "assets", "audio")
S = os.path.join(A, "src")
DUR = 23.0
# (file, at_seconds, gain_db, extra_filter)
ev = [
    ("pop", 1.46, -6, ""),
    ("woosh", 2.90, -14, ""),
    ("bubble", 4.58, -8, ""),
    ("woosh", 4.97, -16, ""),
    ("woosh", 8.25, -12, ""),
    ("ui", 9.41, -14, "atrim=0:0.5,"),
    ("riser", 9.55, -14, "atrim=8.4:9.3,asetpts=PTS-STARTPTS,afade=t=in:d=0.3,"),
    ("pop", 10.75, -5, ""),
    ("swoosh", 11.62, -12, ""),
    ("chime", 15.79, -12, "asetrate=48000*1.0,aresample=48000,"),
    ("chime", 16.69, -12, "asetrate=48000*1.122,aresample=48000,"),
    ("swoosh", 18.20, -16, ""),
]
for i, t in enumerate([10.95, 11.05, 11.15, 11.25, 11.35, 11.45]):
    ev.append(("bubble", t, -15, ""))
t = 8.27
while t < 11.62:
    ev.append(("tick", t, -17, "")); t += 0.25
for semi, t in zip([0, 2, 4, 7, 9], [18.30, 19.04, 19.84, 20.48, 21.16]):
    ev.append(("chime", t, -11, f"asetrate=48000*{2**(semi/12):.5f},aresample=48000,"))
ev.append(("crystal", 21.42, -14, ""))

inputs = ["-i", os.path.join(A, "dialogue.wav"),
          "-i", os.path.join(S, "music_serene.mp3"),
          "-i", os.path.join(S, "waves.mp3")]
fl = [f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={DUR}[dlg]",
      f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{DUR},afade=t=in:d=0.4,volume=-23dB[mus]",
      f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{DUR-11.69},afade=t=in:d=0.6,volume=-30dB,adelay=11690|11690[wav]"]
labels = ["[dlg]", "[mus]", "[wav]"]
for i, (f, at, g, x) in enumerate(ev):
    inputs += ["-i", os.path.join(S, f + ".mp3")]
    k = i + 3
    ms = int(at * 1000)
    fl.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{x}volume={g}dB,adelay={ms}|{ms}[e{i}]")
    labels.append(f"[e{i}]")
fl.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DUR},afade=t=out:st={DUR-0.33}:d=0.33[pre]")

def run(extra, out):
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-y"] + inputs + ["-filter_complex", ";".join(fl) + ";" + extra] + out
    return subprocess.run(cmd, capture_output=True, text=True)

r = run("[pre]loudnorm=I=-14:TP=-1:LRA=7:print_format=json[o]", ["-map", "[o]", "-f", "null", "-"])
js = r.stderr[r.stderr.rfind("{"):]
m = json.loads(js)
ln = (f"loudnorm=I=-14:TP=-1:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
r = run(f"[pre]{ln},aresample=48000[o]", ["-map", "[o]", "-ar", "48000", os.path.join(A, "mix.wav")])
print("rc", r.returncode, r.stderr[-300:] if r.returncode else "mix.wav written")
