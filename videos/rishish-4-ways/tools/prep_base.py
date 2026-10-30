"""Voice-enhance a clip and jump-cut its pauses.

usage: python prep_base.py IN.mp4 OUT.mp4 OUT_cuts.json
Writes the tightened clip and {"segments":[{src_start,src_end,out_start}], "duration"}.
"""
import json, re, subprocess, sys

src, out, cuts_out = sys.argv[1:4]
VOICE = ("highpass=f=80,afftdn=nf=-25:tn=1,"
         "equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=3,"
         "equalizer=f=10000:t=h:w=0.7:g=2,"
         "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=4,"
         "loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000")
GAP, PAD, MIN_KEEP = 0.40, 0.10, 0.25

dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", src]).decode())
log = subprocess.run(["ffmpeg", "-nostdin", "-i", src, "-af", f"highpass=f=80,afftdn=nf=-25,"
                      f"silencedetect=n=-34dB:d={GAP}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
silences = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))

keep, cur = [], 0.0
for s, e in silences:
    a, b = cur, min(dur, s + PAD)
    if b - a >= MIN_KEEP:
        keep.append([a, b])
    cur = max(cur, e - PAD)
if dur - cur >= MIN_KEEP:
    keep.append([cur, dur])
# trim dead air at the very start/end only down to the padding
segments, t = [], 0.0
for a, b in keep:
    segments.append(dict(src_start=round(a, 3), src_end=round(b, 3), out_start=round(t, 3)))
    t += b - a

parts = "".join(f"[0:v]trim={s['src_start']}:{s['src_end']},setpts=PTS-STARTPTS[v{i}];"
                f"[0:a]atrim={s['src_start']}:{s['src_end']},asetpts=PTS-STARTPTS,"
                f"afade=t=in:d=0.01,afade=t=out:st={s['src_end']-s['src_start']-0.012:.3f}:d=0.012[a{i}];"
                for i, s in enumerate(segments))
cat = "".join(f"[v{i}][a{i}]" for i in range(len(segments)))
fc = f"{parts}{cat}concat=n={len(segments)}:v=1:a=1[v][a0];[a0]{VOICE}[a]"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-preset", "fast",
                "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", out], check=True)
json.dump(dict(duration=round(t, 3), source_duration=round(dur, 3), segments=segments),
          open(cuts_out, "w"), indent=1)
print(f"{src}: {dur:.1f}s -> {t:.1f}s, {len(segments)} segments")
