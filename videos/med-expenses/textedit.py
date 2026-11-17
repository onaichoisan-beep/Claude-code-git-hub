"""Music-free "text + clips" edit engine (the POV style). Music gets added in Instagram.

python textedit.py <spec.py> <assets_dir "money spent"> <work_dir> <out.mp4>

A spec file defines:
  END   total length (s)
  DROP  beat-drop time (s) or None; a whoosh is placed there
  SHOTS list of dicts, in time order:
        {"t": start, "src": "IMG_1234", "in": 1.5,           # video clip
         "speed": 0.8, "cx": .5, "transpose": 1,             # optional: slow-mo, horizontal crop, rotation fix
         "text": "line on screen", "ty": 0.40}               # optional text and its vertical position (0-1)
        {"t": start, "src": "IMG_0396", "zoom": 0.25, ...}   # photo -> still with push-in
        {"t": start, "stack": ["IMG_a", "IMG_b"], "pops": [t1, t2], ...}   # photo pile with pop sounds
  SFX   optional list of (catalog_name, time, extra_db)
"""
import os, sys, math, json, random, runpy, subprocess
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
import pillow_heif; pillow_heif.register_heif_opener()
import soundfile as sf

SPEC, A, W, OUT = sys.argv[1:5]
spec = runpy.run_path(SPEC)
SHOTS, END, DROP = spec["SHOTS"], spec["END"], spec.get("DROP")
XFADE, XD = spec.get("XFADE"), spec.get("XFADE_DUR", 0.4)   # e.g. "dissolve"; per shot override with "xfade"
HERE = os.path.dirname(os.path.abspath(__file__))
SFXDIR = os.path.join(HERE, "..", "..", "audio-lab", "sfx")
FW, FH, FPS = 1080, 1920, 30
NAME = os.path.splitext(os.path.basename(SPEC))[0]
random.seed(11)

def find(stem):
    for f in sorted(os.listdir(A)):                      # top-level clips first (your own picks)
        if f.startswith(stem) and os.path.isfile(os.path.join(A, f)): return os.path.join(A, f)
    for fo in ("B.RoLLs", "CollegeNMCH", "Food"):
        for f in sorted(os.listdir(os.path.join(A, fo))):
            if f.startswith(stem): return os.path.join(A, fo, f)
    raise FileNotFoundError(stem)

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]
def run(c): subprocess.run(c, check=True)
def dur_of(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                           capture_output=True, text=True).stdout or 0)
def is_photo(p): return p.lower().endswith((".jpg", ".jpeg", ".heic", ".png"))

def frames_writer(out):
    return subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}",
                             "-r", str(FPS), "-i", "-"] + ENC + [out], stdin=subprocess.PIPE)

def load(p, m=2400):
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB"); im.thumbnail((m, m)); return im

def cover_img(im):
    s = max(FW / im.width, FH / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)))
    x, y = (im.width - FW) // 2, (im.height - FH) // 2
    return im.crop((x, y, x + FW, y + FH))

def still(path, d, out, speed=0.08):
    im = load(path); s = max(FW / im.width, FH / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)))
    pr = frames_writer(out); n = int(round(d * FPS))
    for i in range(n):
        z = 1 + speed * i / max(1, n - 1); w, h = FW / z, FH / z; x0, y0 = (im.width - w) / 2, (im.height - h) / 2
        pr.stdin.write(im.resize((FW, FH), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).tobytes())
    pr.stdin.close(); pr.wait()

def card(im):
    im = im.copy(); im.thumbnail((700, 900)); bw, pad = 16, 40
    fr = Image.new("RGB", (im.width + 2 * bw, im.height + 2 * bw), "white"); fr.paste(im, (bw, bw))
    out = Image.new("RGBA", (fr.width + 2 * pad, fr.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((pad + 10, pad + 14, pad + 10 + fr.width, pad + 14 + fr.height), fill=(0, 0, 0, 150))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); out.paste(fr, (pad, pad)); return out

def pop_scale(t):
    if t < 0: return None
    if t >= 0.2: return 1.0
    u = t / 0.2
    return 0.55 + 0.53 * math.sin(u * math.pi * 0.62) / math.sin(math.pi * 0.62) if u < 0.7 else 1.08 - 0.08 * (u - 0.7) / 0.3

def stack(paths, pops, t0, d, out):
    ims = [load(p, 1400) for p in paths]
    bg = cover_img(ims[0]).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", bg.size, "black"), 0.45).convert("RGBA")
    placed = []
    for i, im in enumerate(ims):
        c = card(im).rotate(random.uniform(-9, 9) if i else random.uniform(-4, 4), resample=Image.BICUBIC, expand=True)
        placed.append((c, random.randint(-70, 70), random.randint(-40, 50)))
    pr = frames_writer(out)
    for f in range(int(round(d * FPS))):
        t = t0 + f / FPS; fr = bg.copy()
        for (c, dx, dy), pt in zip(placed, pops):
            sc = pop_scale(t - pt)
            if sc is None: continue
            cc = c if sc == 1.0 else c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.BILINEAR)
            x = min(max(FW // 2 + dx - cc.width // 2, 12), FW - cc.width - 12)
            fr.alpha_composite(cc, (x, int(FH * 0.57) + dy - cc.height // 2))
        pr.stdin.write(fr.convert("RGB").tobytes())
    pr.stdin.close(); pr.wait()

# ------------------------------------------------------------------ picture
segdir = os.path.join(W, f"{NAME}_segs"); os.makedirs(segdir, exist_ok=True)
segs = []
for i, s in enumerate(SHOTS):
    t0 = s["t"]; t1 = SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else END
    d = round(t1 - t0 + (XD if XFADE and i + 1 < len(SHOTS) else 0), 3)
    out = os.path.join(segdir, f"{i:02d}.mp4"); segs.append(out)
    if "stack" in s:
        stack([find(x) for x in s["stack"]], s["pops"], t0, d, out); label = "stack"
    else:
        src = find(s["src"]); label = os.path.basename(src)
        if is_photo(src):
            still(src, d, out, s.get("zoom", 0.08))
        else:
            sp = s.get("speed", 1.0); sin = s.get("in", 0.0)
            vf = ([f"transpose={s['transpose']}"] if "transpose" in s else []) + (
                [f"scale=-2:{FH*1.12:.0f}", "deshake=rx=48:ry=48:edge=clamp"] if s.get("stabilize") else []) + [
                f"scale={int(FW*s.get('vzoom',1))}:{int(FH*s.get('vzoom',1))}:force_original_aspect_ratio=increase",
                f"crop={FW}:{FH}:(iw-{FW})*{s.get('cx', .5)}:(ih-{FH})*{s.get('cy', .5)}", f"setpts=PTS/{sp}", f"fps={FPS}", "setsar=1"] + (
                [f"scale=w='trunc({FW}*(1+{s['pushin']}*t/{d})/2)*2':h=-2:eval=frame:flags=bicubic",
                 f"crop={FW}:{FH}:(iw-{FW})/2:(ih-{FH})*{s.get('py', 0.5)}"]
                if s.get("pushin") else [])
            if s.get("fit"):   # whole landscape/rotated frame, centred over a blurred copy: no crop, no zoom
                pre = ([f"transpose={s['transpose']}"] if "transpose" in s else []) + [f"scale={FW}:-2"]
                post = (f"split[fa][fb];[fa]scale={FW}:{FH}:force_original_aspect_ratio=increase,crop={FW}:{FH},"
                        f"boxblur=40:4,eq=brightness=-0.08[fbg];[fbg][fb]overlay=(W-w)/2:(H-h)/2,setpts=PTS/{sp},fps={FPS},setsar=1")
                span = ["-ss", str(sin), "-t", f"{d * sp + 0.2:.3f}", "-i", src]
                if s.get("smooth"):
                    trf = out + ".trf"
                    run(["ffmpeg", "-loglevel", "error", "-y"] + span + ["-vf", ",".join(pre) + f",vidstabdetect=shakiness=6:accuracy=15:result={trf}", "-f", "null", "-"])
                    mid = f",vidstabtransform=input={trf}:smoothing=20:optzoom=2:zoomspeed=0.15:interpol=bicubic"
                else:
                    mid = ""
                run(["ffmpeg", "-loglevel", "error", "-y"] + span + ["-vf", ",".join(pre) + mid + "," + post] + ENC + ["-t", str(d), out])
                print(f"{t0:6.2f}-{t1:6.2f} {label:28.28} | {s.get('text', '')}  [fit]"); continue
            if "freeze_at" in s:   # play up to this source time, then hold that frame
                vf.insert(0, f"trim=end={s['freeze_at'] - sin},setpts=PTS-STARTPTS"); vf.append(f"tpad=stop_mode=clone:stop_duration={d}")
            elif (dur_of(src) - sin) / sp < d: vf.append(f"tpad=stop_mode=clone:stop_duration={d}")
            if s.get("smooth"):   # two-pass gimbal-style stabilisation (vid.stab), minimal adaptive crop
                trf = out + ".trf"; span = ["-ss", str(sin), "-t", f"{d * sp + 0.2:.3f}", "-i", src]
                run(["ffmpeg", "-loglevel", "error", "-y"] + span + ["-vf", ",".join(vf) + f",vidstabdetect=shakiness=6:accuracy=15:result={trf}", "-f", "null", "-"])
                run(["ffmpeg", "-loglevel", "error", "-y"] + span + ["-vf", ",".join(vf) + f",vidstabtransform=input={trf}:smoothing=20:optzoom=2:zoomspeed=0.15:interpol=bicubic,unsharp=5:5:0.5"]
                    + ENC + ["-t", str(d), out])
            else:
                run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(sin), "-i", src, "-vf", ",".join(vf)] + ENC + ["-t", str(d), out])
    print(f"{t0:6.2f}-{t1:6.2f} {label:28.28} | {s.get('text', '')}")

pic = os.path.join(W, f"{NAME}_picture.mp4")
if XFADE:
    # shot i+1 starts dissolving in at its scheduled time; each segment carries an XD-long tail
    ins, fc, cur = [], [], "0:v"
    for x in segs: ins += ["-i", x]
    for i in range(1, len(segs)):
        kind = SHOTS[i].get("xfade", XFADE)
        fc.append(f"[{cur}][{i}:v]xfade=transition={kind}:duration={XD}:offset={SHOTS[i]['t']}[v{i}]"); cur = f"v{i}"
    run(["ffmpeg", "-loglevel", "error", "-y"] + ins + ["-filter_complex", ";".join(fc), "-map", f"[{cur}]"] + ENC + [pic])
else:
    lst = os.path.join(W, f"{NAME}_concat.txt"); open(lst, "w").write("".join(f"file '{x}'\n" for x in segs))
    run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic])

# ------------------------------------------------------------------ text (white, lowercase look, soft shadow; emoji in colour)
FONT = ImageFont.truetype(os.path.join(W, "fonts", "Ubuntu-Medium.ttf"), 64)
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
def is_emoji(ch): return ord(ch) > 0x2600 and ch not in "…₹"
def runs(t):
    out = []
    for ch in t:
        e = is_emoji(ch) or ch in "️‍"
        if out and out[-1][1] == e: out[-1][0] += ch
        else: out.append([ch, e])
    return out
def emoji_img(s, hgt=62):
    s = s.replace("️", "")
    im = Image.new("RGBA", (140 * len(s), 140), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), s, font=EMOJI, embedded_color=True)
    im = im.crop(im.getbbox() or (0, 0, 1, 1)); return im.resize((int(im.width * hgt / max(1, im.height)), hgt))
def wrap(t, maxw=FW - 120):
    lines, cur = [], ""
    for w in t.split(" "):
        c = (cur + " " + w).strip()
        if FONT.getlength(c) > maxw and cur: lines.append(cur); cur = w
        else: cur = c
    return lines + [cur]
def fit_font(t):
    size = 64
    while size > 34:
        f = ImageFont.truetype(os.path.join(W, "fonts", "Ubuntu-Medium.ttf"), size)
        w = sum((size * 1.05) if e else f.getlength(x) for x, e in runs(t))
        if w <= FW - 90: return f, size
        size -= 2
    return f, size
MID = spec.get("MID_CAPTIONS")          # centred, smaller, safe-zone captions (max 2 lines)
SAFE_W = 860                            # ~80% of 1080: clear of screen edges and Instagram's side buttons
def measure(t, f):
    return sum((emoji_img(x, int(f.size * 0.97)).width + 8) if e else f.getlength(x) for x, e in runs(t))
def mid_lines(t):
    for size in range(46, 34, -2):
        f = ImageFont.truetype(os.path.join(W, "fonts", "Ubuntu-Medium.ttf"), size)
        lines, cur = [], ""
        for w_ in t.split(" "):
            c = (cur + " " + w_).strip()
            if measure(c, f) > SAFE_W and cur: lines.append(cur); cur = w_
            else: cur = c
        lines.append(cur)
        if len(lines) <= 2 and all(measure(l, f) <= SAFE_W for l in lines): return f, size, lines
    return f, size, lines
def text_png(t, path):
    global FONT
    if MID:
        FONT, fsz, lines = mid_lines(t); lh = int(fsz * 1.32)
    elif spec.get("SINGLE_LINE"):
        FONT, fsz = fit_font(t); lines = [t]; lh = int(fsz * 1.3)
    else:
        lines = wrap(t); lh = 82
    img = Image.new("RGBA", (FW, 60 + lh * len(lines)), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for k, ln in enumerate(lines):
        parts = [(emoji_img(x, int(FONT.size * 0.97)) if e else x, e) for x, e in runs(ln)]
        width = sum((p.width + 8) if e else FONT.getlength(p) for p, e in parts); x = (FW - width) / 2; y = 30 + k * lh
        for p, e in parts:
            if e: img.alpha_composite(p, (int(x + 4), y + 6)); x += p.width + 8
            else:
                ImageDraw.Draw(sh).text((x + 3, y + 4), p, font=FONT, fill=(0, 0, 0, 200))
                ImageDraw.Draw(img).text((x, y), p, font=FONT, fill="white"); x += FONT.getlength(p)
    base = Image.new("RGBA", img.size, (0, 0, 0, 0)); base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    base.alpha_composite(img); base.save(path); return base.height

ovl = os.path.join(W, f"{NAME}_ovl"); os.makedirs(ovl, exist_ok=True)
inputs, chain = ["-i", pic], []
chain.append("[0:v]eq=saturation=1.06:contrast=0.97:brightness=0.01,colorbalance=rs=0.05:gs=0.01:bs=-0.05:rm=0.03:bm=-0.03,"
             f"fade=t=in:st=0:d=0.2,fade=t=out:st={END-spec.get('FADE_OUT', 0.9)}:d={spec.get('FADE_OUT', 0.9)}[g]"); last = "g"; k = 0
for i, s in enumerate(SHOTS):
    if not s.get("text"): continue
    t0 = s["t"]; t1 = s.get("text_until") or (SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else END)
    p = os.path.join(ovl, f"t{i:02d}.png"); h = text_png(s["text"], p)
    inputs += ["-loop", "1", "-framerate", str(FPS), "-t", str(END), "-i", p]; k += 1
    fi = 0.25 if t1 - t0 > 1.2 else 0.08
    fo = XD if XFADE and i + 1 < len(SHOTS) else 0.06
    t1 = t1 + (XD if XFADE and i + 1 < len(SHOTS) else 0) - (0 if XFADE else 0)
    chain.append(f"[{k}:v]format=rgba,fade=t=in:st={t0 + (XD*0.5 if XFADE and i else 0)}:d={fi}:alpha=1,fade=t=out:st={t1-fo}:d={fo}:alpha=1[x{k}]")
    yy = spec.get("MID_Y", 0.5) if MID else s.get('ty', 0.40)
    chain.append(f"[{last}][x{k}]overlay=0:{int(FH*yy) - h//2}:enable='between(t,{t0},{t1})'[o{k}]"); last = f"o{k}"

# single white flash on a hard cut (FLASH = time), no crossfade
if spec.get("FLASH") is not None:
    fl = spec["FLASH"]
    chain.append(f"color=white:s={FW}x{FH}:r={FPS}:d={END},format=rgba,fade=t=in:st={fl-0.08}:d=0.08:alpha=1,"
                 f"fade=t=out:st={fl}:d=0.35:alpha=1[flash]")
    chain.append(f"[{last}][flash]overlay=0:0:enable='between(t,{fl-0.08},{fl+0.36})'[ofl]"); last = "ofl"

# credibility tag: small line, e.g. ("MBBS student · NMCH Patna", t0, t1, ty)
if spec.get("TAG"):
    tg, a0, a1, tyy = spec["TAG"]
    if MID: tyy = spec.get("MID_Y", 0.5) + 0.075
    tf = ImageFont.truetype(os.path.join(W, "fonts", "Ubuntu-Medium.ttf"), 32 if MID else 40)
    im = Image.new("RGBA", (FW, 90), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); x = (FW - tf.getlength(tg)) / 2
    ImageDraw.Draw(sh).text((x + 2, 27), tg, font=tf, fill=(0, 0, 0, 220)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    ImageDraw.Draw(im).text((x, 24), tg, font=tf, fill=(255, 255, 255, 235))
    tp = os.path.join(ovl, "tag.png"); im.save(tp); inputs += ["-loop", "1", "-framerate", str(FPS), "-t", str(END), "-i", tp]; k += 1
    chain.append(f"[{k}:v]format=rgba,fade=t=in:st={a0}:d=0.25:alpha=1[x{k}]")
    chain.append(f"[{last}][x{k}]overlay=0:{int(FH*tyy) - 45}:enable='between(t,{a0},{a1})'[o{k}]"); last = f"o{k}"

# ------------------------------------------------------------------ sound: whoosh on the drop, pops, extras
SR = 48000; mix = np.zeros(int(END * SR) + SR, np.float32)
cat = {c["name"]: c for c in json.load(open(os.path.join(SFXDIR, "catalog.json")))}
def synth(name, at, db):
    n = int(0.16 * SR); t = np.arange(n) / SR
    if name == "pop":
        y = np.sin(2 * np.pi * np.cumsum(950 * np.exp(-t * 28) + 260) / SR) * np.exp(-t * 55)
    elif name == "bubble":   # rising "bloop" like a bubble in a test tube
        p = random.uniform(0.8, 1.3)
        y = np.sin(2 * np.pi * np.cumsum((280 + 900 * (1 - np.exp(-t * 40))) * p) / SR) * np.exp(-t * 38)
    elif name == "beep":     # soft patient-monitor beep
        y = np.sin(2 * np.pi * 1000 * t) * np.minimum(1, t / 0.005) * (t < 0.11) * np.exp(-t * 6)
    elif name == "step":     # soft footstep thud
        y = (np.sin(2 * np.pi * 90 * t) * 0.8 + np.random.randn(n) * 0.25) * np.exp(-t * 35)
    elif name == "tick":
        y = np.random.randn(n) * np.exp(-t * 400)
    y = (y / (np.abs(y).max() + 1e-9) * 10 ** (db / 20)).astype(np.float32)
    s0 = int(at * SR); e = min(len(mix), s0 + n); mix[s0:e] += y[:e - s0]
def place(name, at, db=0):
    if name in ("pop", "bubble", "beep", "tick", "step"): return synth(name, at, db)
    c = cat[name]
    y = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(SFXDIR, c["file"]), "-f", "f32le",
                                      "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout, np.float32)
    s0 = int((at - c["sync_at_s"]) * SR); y = y[max(0, -s0):]; s0 = max(0, s0); e = min(len(mix), s0 + len(y))
    mix[s0:e] += 10 ** ((c["gain_db_for_minus14_voice"] + db) / 20) * y[:e - s0]
def pop(at, pitch=1.0, db=-12):
    n = int(0.09 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(950 * pitch * np.exp(-t * 28) + 260 * pitch) / SR) * np.exp(-t * 55) * 10 ** (db / 20)
    s0 = int(at * SR); mix[s0:s0 + n] += y.astype(np.float32)
if DROP is not None: place("My_fav_whoosh", DROP, 4)
for s in SHOTS:
    for j, t in enumerate(s.get("pops", [])): pop(t, random.uniform(0.85, 1.25), -12 if j == 0 else -14)
    if s.get("pop_on_cut"): pop(s["t"] + 0.03)
for name, t, db in spec.get("SFX", []): place(name, t, db)
mix = mix[:int(END * SR)]
pk = np.abs(mix).max()
if pk > 10 ** (-1.5 / 20): mix *= 10 ** (-1.5 / 20) / pk   # keep SFX from clipping
aud = os.path.join(W, f"{NAME}_sfx.wav"); sf.write(aud, mix, SR); inputs += ["-i", aud]

if not spec.get("WORD_CAPTIONS"):
    run(["ffmpeg", "-loglevel", "error", "-y"] + inputs + ["-filter_complex", ";".join(chain), "-map", f"[{last}]",
         "-map", f"{k+1}:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(END), OUT])
else:
    # ONE WORD AT A TIME: instant on, single centred line, monoline sans (Inter SemiBold)
    WFONT = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 104)
    def word_img(w):
        if is_emoji(w[0]):
            e = Image.new("RGBA", (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(e).text((0, 0), w, font=EMOJI, embedded_color=True)
            e = e.crop(e.getbbox()); return e.resize((int(e.width * 110 / e.height), 110))
        l, t_, r, b = WFONT.getbbox(w); pad = 24
        img = Image.new("RGBA", (r - l + 2 * pad, 150), (0, 0, 0, 0)); sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - l + 3, 19), w, font=WFONT, fill=(0, 0, 0, 210))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
        ImageDraw.Draw(img).text((pad - l, 14), w, font=WFONT, fill="white", stroke_width=2, stroke_fill=(0, 0, 0, 90))
        return img
    WORDS = []
    for i, s_ in enumerate(SHOTS):
        if not s_.get("text"): continue
        st = s_["t"] + (XD * 0.5 if XFADE and i else 0)          # start once the dissolve is half done
        en = SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else END
        ws = s_["text"].split(); per = min(spec.get("WORD_DUR", 0.38), (en - st) / len(ws))
        for j, w in enumerate(ws):
            WORDS.append((st + j * per, en if j == len(ws) - 1 else st + (j + 1) * per, word_img(w), s_.get("ty", 0.40)))
    print(len(WORDS), "word captions")
    grade = ("eq=saturation=1.06:contrast=0.97:brightness=0.01,colorbalance=rs=0.05:gs=0.01:bs=-0.05:rm=0.03:bm=-0.03,"
             f"fade=t=in:st=0:d=0.35,fade=t=out:st={END-0.9}:d=0.9")
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", pic, "-vf", grade, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}",
                            "-r", str(FPS), "-i", "-", "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset",
                            "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                            "-t", str(END), OUT], stdin=subprocess.PIPE)
    fsz = FW * FH * 3; fno = 0
    while True:
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz: break
        tt = fno / FPS; cur = [w for w in WORDS if w[0] <= tt < w[1]]
        if cur:
            fr = Image.frombuffer("RGB", (FW, FH), buf).convert("RGBA"); im, ty = cur[-1][2], cur[-1][3]
            fr.alpha_composite(im, ((FW - im.width) // 2, int(FH * ty) - im.height // 2)); buf = fr.convert("RGB").tobytes()
        enc.stdin.write(buf); fno += 1
    enc.stdin.close(); enc.wait(); dec.wait()
print("done", OUT, END)
