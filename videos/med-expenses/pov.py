"""POV: first year at a govt medical college. Music-free edit; add the song in Instagram.

python pov.py <assets_dir "money spent"> <work_dir> <out.mp4>
The beat drop is at DROP seconds: line the song's drop up with it in the Instagram editor.
"""
import os, sys, math, subprocess, json
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
import pillow_heif; pillow_heif.register_heif_opener()
import soundfile as sf

A, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(HERE, "..", "..", "audio-lab", "sfx")
FW, FH, FPS = 1080, 1920, 30
B, C, F = "B.RoLLs", "CollegeNMCH", "Food"
DROP = 9.0

def find(stem):
    for fo in (B, C, F):
        for f in sorted(os.listdir(os.path.join(A, fo))):
            if f.startswith(stem): return os.path.join(A, fo, f)
    raise FileNotFoundError(stem)

# (start, source, source_in, text, extra)   kind is inferred: photo -> still with push-in
SHOTS = [
    # part 1: calm build
    (0.0,  "F1D19DE4", 4.5,  "pov: you cleared NEET…", {}),
    (1.8,  "IMG_6261", 0.2,  "…and got a govt medical college", {}),
    (3.6,  "IMG_6262", 0.3,  "the campus", {}),
    (5.2,  "IMG_6263", 0.2,  "the first lecture", {}),
    (6.8,  "IMG_8307", 15.0, "the coat finally fits", {}),
    # part 2: the drop, fast
    (DROP, "IMG_0396", 0,    "real bones in week 1 🦴", {"zoom_speed": 0.25}),
    (9.9,  "67168F2A", 2.6,  "labs", {}),
    (10.7, "IMG_4318", 1.5,  "lab partners", {}),
    (11.5, "IMG_1366", 1.0,  "3D anatomy at 2 AM", {}),
    (12.3, "IMG_0959", 6.0,  "late nights", {}),
    (13.1, "IMG_9200", 1.0,  "auto rides", {"transpose": 1, "cx": 0.62}),
    (13.9, "IMG_6393", 2.45, "your people", {}),
    (14.7, "FFC484C5", 0.2,  "momo breaks", {}),
    # part 3: slow ending
    (15.5, "E56BD187", 0.0,  "and fees of ₹1500/month", {}),
    (17.9, "IMG_9328", 1.0,  "worth every sleepless night.", {}),
]
END = 21.0
TITLE_ON_FIRST = True

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]
def run(c): subprocess.run(c, check=True)
def dur_of(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                           capture_output=True, text=True).stdout or 0)

def cover(cx=0.5, transpose=None):
    f = [f"transpose={transpose}"] if transpose is not None else []
    f += [f"scale={FW}:{FH}:force_original_aspect_ratio=increase", f"crop={FW}:{FH}:(iw-{FW})*{cx}:(ih-{FH})/2",
          f"fps={FPS}", "setsar=1"]
    return ",".join(f)

def still(path, dur, out, speed=0.08):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB"); im.thumbnail((2400, 2400))
    s = max(FW / im.width, FH / im.height); im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)))
    n = int(round(dur * FPS))
    pr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}",
                           "-r", str(FPS), "-i", "-"] + ENC + [out], stdin=subprocess.PIPE)
    for i in range(n):
        z = 1.0 + speed * i / max(1, n - 1); w, h = FW / z, FH / z
        x0, y0 = (im.width - w) / 2, (im.height - h) / 2
        pr.stdin.write(im.resize((FW, FH), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).tobytes())
    pr.stdin.close(); pr.wait()

segdir = os.path.join(W, "pov_segs"); os.makedirs(segdir, exist_ok=True)
segs = []
for i, (st, stem, sin, txt, ex) in enumerate(SHOTS):
    en = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END
    d = round(en - st, 3); src = find(stem); out = os.path.join(segdir, f"{i:02d}.mp4"); segs.append(out)
    if src.lower().endswith((".jpg", ".jpeg", ".heic", ".png")):
        still(src, d, out, ex.get("zoom_speed", 0.08))
    else:
        vf = cover(ex.get("cx", 0.5), ex.get("transpose"))
        if dur_of(src) - sin < d: vf += f",tpad=stop_mode=clone:stop_duration={d}"
        run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(sin), "-i", src, "-t", str(d), "-vf", vf] + ENC + ["-t", str(d), out])
    print(f"{st:5.1f}-{en:5.1f} {stem} | {txt}")

lst = os.path.join(W, "pov_concat.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
pic = os.path.join(W, "pov_picture.mp4")
run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic])

# text: ONE WORD AT A TIME, instant on (no fade), single centred line, monoline sans (Inter SemiBold)
WFONT = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 104)
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
def is_emoji(w): return any(ord(c) > 0x2600 and c not in "…₹" for c in w)
def word_img(w):
    if is_emoji(w):
        e = Image.new("RGBA", (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(e).text((0, 0), w, font=EMOJI, embedded_color=True)
        e = e.crop(e.getbbox()); return e.resize((int(e.width * 110 / e.height), 110))
    l, t, r, b = WFONT.getbbox(w); pad = 24
    img = Image.new("RGBA", (r - l + 2 * pad, 150), (0, 0, 0, 0)); sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((pad - l + 3, 14 + 5), w, font=WFONT, fill=(0, 0, 0, 210))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(img).text((pad - l, 14), w, font=WFONT, fill="white", stroke_width=2, stroke_fill=(0, 0, 0, 90))
    return img

# word timeline: words share the start of each shot (max 0.38 s each), the last word holds to the end of the shot
WORDS = []
for i, (st, stem, sin, txt, ex) in enumerate(SHOTS):
    en = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END
    ws = txt.split(); per = min(0.38, (en - st) / len(ws))
    for k, w in enumerate(ws):
        WORDS.append((round(st + k * per, 3), round(en if k == len(ws) - 1 else st + (k + 1) * per, 3), word_img(w)))
print(len(WORDS), "word captions")

# sound: only a whoosh into the drop and a pop on the bones; music gets added in Instagram
SR = 48000
mix = np.zeros(int(END * SR), np.float32)
cat = {c["name"]: c for c in json.load(open(os.path.join(SFX, "catalog.json")))}
def place(name, at, db):
    c = cat[name]
    y = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(SFX, c["file"]), "-f", "f32le", "-ac", "1",
                                      "-ar", str(SR), "-"], capture_output=True, check=True).stdout, np.float32)
    s = int((at - c["sync_at_s"]) * SR); y = y[max(0, -s):]; s = max(0, s); e = min(len(mix), s + len(y))
    mix[s:e] += 10 ** ((c["gain_db_for_minus14_voice"] + db) / 20) * y[:e - s]
place("My_fav_whoosh", DROP, 4)
n = int(0.09 * SR); t = np.arange(n) / SR
pop = np.sin(2 * np.pi * np.cumsum(950 * np.exp(-t * 28) + 260) / SR) * np.exp(-t * 55) * 10 ** (-12 / 20)
mix[int((DROP + 0.05) * SR):int((DROP + 0.05) * SR) + n] += pop.astype(np.float32)
aud = os.path.join(W, "pov_sfx.wav"); sf.write(aud, mix, SR)

# one pass: grade the picture in ffmpeg, stamp the current word in Python, encode with the sound
grade = ("eq=saturation=1.06:contrast=0.97:brightness=0.01,colorbalance=rs=0.05:gs=0.01:bs=-0.05:rm=0.03:bm=-0.03,"
         f"fade=t=in:st=0:d=0.35,fade=t=out:st={END-0.9}:d=0.9")
dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", pic, "-vf", grade, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}",
                        "-r", str(FPS), "-i", "-", "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
                        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                        "-t", str(END), OUT], stdin=subprocess.PIPE)
fs = FW * FH * 3; f = 0
while True:
    buf = dec.stdout.read(fs)
    if len(buf) < fs: break
    tt = f / FPS; fr = Image.frombuffer("RGB", (FW, FH), buf)
    cur = [w for w in WORDS if w[0] <= tt < w[1]]
    if cur:
        im = cur[-1][2]; fr = fr.convert("RGBA")
        fr.alpha_composite(im, ((FW - im.width) // 2, int(FH * 0.40) - im.height // 2)); fr = fr.convert("RGB")
    enc.stdin.write(fr.tobytes()); f += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("done", OUT)
