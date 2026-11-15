"""Build the "My room costs 5x my MBBS fees" vlog.

python build.py <assets_dir> <work_dir> <out.mp4>
assets_dir = the Drive folder "money spent" (Food/, CollegeNMCH/, B.RoLLs/)
work_dir   = holds vo_fast.wav, fonts/, sfx wavs; scratch files are written here.
Style: video-playbook/BUDGET_VLOG_STYLE.md. Timings come from the tightened voice-over.
"""
import os, sys, json, math, random, subprocess
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
import pillow_heif; pillow_heif.register_heif_opener()
import soundfile as sf, librosa

A, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(HERE, "..", "..", "audio-lab", "sfx")
FW, FH, FPS = 1080, 1920, 30
VO = os.path.join(W, "vo_fast.wav")
VO_LEN = sf.info(VO).duration
END = round(VO_LEN + 0.35, 2)
random.seed(7)

def p(folder, name): return os.path.join(A, folder, name)
B, C, F = "B.RoLLs", "CollegeNMCH", "Food"

def find(folder, stem):
    for fo in [folder] + [x for x in (B, C, F) if x != folder]:
        for f in sorted(os.listdir(os.path.join(A, fo))):
            if f.startswith(stem): return p(fo, f)
    raise FileNotFoundError(stem)

# ---------------------------------------------------------------- edit list
# (start_on_timeline, kind, source, source_in, extra)
# kinds: "v" video clip, "still" photo with slow push-in, "stack" photo pile with pops
def stack(photos, pops):
    return {"photos": [find(fo, st) for fo, st in photos], "pops": pops}

# Fast pace: ~45 shots, most 0.8-1.6 s, cut on the spoken words.
EDL = [
    (0.00, "v", find(B, "IMG_9323"), 0.55, {}),                     # hook: face to camera
    (1.78, "v", find(B, "IMG_9323"), 2.33, {"zoom": 1.3}),          # "paanch guna mehenga" punch-in
    (2.84, "v", find(B, "IMG_8307"), 15.0, {}),                     # "let me show you" walking in coat
    (4.00, "v", find(B, "IMG_8307"), 25.0, {}),                     # "where my money goes"
    (5.62, "v", find(C, "IMG_6261"), 0.2, {}),                      # "sabse pehle" college sign
    (6.30, "v", find(C, "IMG_6262"), 0.3, {}),                      # "college fee" campus
    (7.22, "v", find(C, "IMG_6451"), 0.3, {}),                      # "GMC main" lecture
    (8.06, "still", find(C, "IMG_0396"), 0, {}),                    # "poore saal ki fees" bones in hand
    (8.90, "v", find(B, "IMG_4318"), 1.5, {}),                      # "sirf 18,000" lab with the boys
    (10.42, "v", find(C, "IMG_6393"), 2.45, {}),                    # "matlab roughly" walking with friends
    (11.40, "v", find(C, "E56BD187"), 0.5, {}),                     # "1500 a month" lit-up college
    (12.32, "v", find(B, "IMG_9308"), 3.0, {}),                     # "the villain" dramatic night selfie
    (14.10, "v", find(B, "IMG_1480"), 0.3, {}),                     # "8,000" room desk
    (15.52, "still", find(B, "IMG_2410"), 0, {}),                   # "electricity" street light
    (16.54, "v", find(B, "IMG_1510"), 0.5, {}),                     # "bill" desk lamp + tablet
    (17.50, "v", find(B, "IMG_0959"), 6.0, {}),                     # "1000 hota hai" studying at night
    (18.66, "v", find(B, "26EEAFDA"), 0.3, {}),                     # "summer" sun
    (19.40, "v", find(B, "IMG_2135"), 0.2, {}),                     # "winter" rain
    (20.66, "stack", None, 0, stack([(B, "IMG_4056"), (B, "IMG_3677"), (B, "IMG_0863")],
                                    [20.66, 21.56, 22.28])),       # "mess ka khaana... 3000"
    (23.02, "v", find(C, "2FC33FFA"), 2.85, {}),                     # "aur actually mess ka khaana" friend looks back, confused
    (24.58, "v", find(B, "IMG_2134"), 0.3, {}),                     # "khaata kaun hai" reaction
    (25.42, "v", find(B, "FFC484C5"), 0.2, {}),                     # "so dine out is around" eating momos with friends
    (26.44, "stack", None, 0, stack([(F, "IMG_0094"), (F, "IMG_8621"), (F, "IMG_1146")],
                                    [26.44, 26.78, 27.10])),       # "1500 har month" quick triple pop
    (27.44, "v", find(B, "IMG_6575"), 1.0, {}),                     # "kyunki" drinking juice
    (28.10, "v", find(C, "0E716FE9"), 0.3, {}),                     # "mess ka khaana bilkul achha nahi" unimpressed face
    (29.54, "v", find(B, "4BB8245D"), 2.0, {"zoom": 1.4, "cy": 0.1}),  # "aur phir aata hai" friend coming up
    (30.48, "stack", None, 0, stack([(B, "IMG_0465"), (B, "IMG_0712")],
                                    [30.48, 31.12])),              # "Blinkit"
    (31.56, "v", find(B, "IMG_0959"), 2.0, {}),                     # "impulsive buys" late-night study cravings
    (32.74, "v", find(B, "IMG_8298"), 1.0, {"cx": 0.72}),           # "groceries" selfie
    (33.56, "stack", None, 0, stack([(B, "IMG_0868"), (F, "IMG_0924")],
                                    [33.56, 34.04])),              # "1500"
    (34.86, "v", find(C, "2A473245"), 1.0, {}),                     # "2000 per month" night ride out
    (36.12, "v", find(B, "IMG_9200"), 1.0, {"transpose": 1, "cx": 0.62}),  # "transportation" auto ride
    (37.80, "v", find(B, "IMG_4359"), 0.3, {}),                     # "college meri room se"
    (38.82, "v", find(B, "IMG_4198"), 3.0, {}),                     # "thoda hi dur" whip walk
    (39.90, "v", find(B, "IMG_2136"), 0.2, {}),                     # "lagbhag 500" road to college
    (40.96, "v", find(B, "IMG_8307"), 5.0, {}),                     # walking in coat
    (41.74, "v", find(B, "IMG_8161"), 0.5, {}),                     # "Rapido otherwise" walking selfie
    (42.82, "v", find(B, "IMG_8307"), 28.0, {}),                    # "walking"
    (43.40, "v", find(B, "IMG_1364"), 0.3, {}),                     # "subscriptions" tablet
    (44.56, "v", find(B, "IMG_1365"), 2.0, {}),                     # "music"
    (45.48, "v", find(B, "IMG_1479"), 4.0, {}),                     # "YouTube" lecture
    (46.62, "v", find(B, "IMG_1366"), 1.0, {}),                     # "apps"
    (47.96, "v", find(B, "IMG_2281"), 4.0, {}),                     # "500 lagte hai" selfie
    (49.18, "v", find(B, "26EEAFDA"), 3.45, {}),                     # "comment me" face to camera
    (50.48, "v", find(B, "IMG_9328"), 2.0, {}),                     # ending, standing in coat
]

CAPTIONS = [  # text, on, off   (on ~0.1-0.2 s before the topic's first word)
    ("college fee: ₹1500/month", 5.55, 12.22),
    ("room rent: ₹8000", 12.22, 15.42),
    ("electricity: ~₹1000", 15.42, 20.56),
    ("mess food: ₹3000", 20.56, 25.32),
    ("dining out: ₹1500", 25.32, 29.46),
    ("blinkit + impulse buys: ₹1500-2000", 29.46, 36.02),
    ("transport: ₹500", 36.02, 43.30),
    ("subscriptions: ₹500", 43.30, 49.08),
    ("comment the total!", 49.08, END),
]
TITLE = "MY ROOM COSTS 5X MY MBBS FEES?!"

# ---------------------------------------------------------------- video
def run(cmd): subprocess.run(cmd, check=True)

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]
segdir = os.path.join(W, "segs"); os.makedirs(segdir, exist_ok=True)

def cover_filter(cx=0.5, transpose=None, zoom=1.0, cy=0.5):
    f = []
    if transpose is not None: f.append(f"transpose={transpose}")
    f.append(f"scale={int(FW*zoom)}:{int(FH*zoom)}:force_original_aspect_ratio=increase")
    f.append(f"crop={FW}:{FH}:(iw-{FW})*{cx}:(ih-{FH})*{cy}")
    f += [f"fps={FPS}", "setsar=1"]
    return ",".join(f)

def load_photo(path, max_side=1400):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im.thumbnail((max_side, max_side)); return im

def render_still(path, dur, out):
    im = load_photo(path, 2400)
    s = max(FW / im.width, FH / im.height); im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)))
    frames = int(round(dur * FPS))
    pr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}",
                           "-r", str(FPS), "-i", "-"] + ENC + [out], stdin=subprocess.PIPE)
    for i in range(frames):
        z = 1.0 + 0.08 * i / max(1, frames - 1)
        w, h = FW / z, FH / z
        x0, y0 = (im.width - w) / 2, (im.height - h) / 2
        fr = im.resize((FW, FH), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
        pr.stdin.write(fr.tobytes())
    pr.stdin.close(); pr.wait()

def card(im):
    """White-bordered photo with a drop shadow, ~760 px wide."""
    im = im.copy(); im.thumbnail((720, 940))
    bw = 16
    framed = Image.new("RGB", (im.width + 2 * bw, im.height + 2 * bw), "white"); framed.paste(im, (bw, bw))
    pad = 40
    out = Image.new("RGBA", (framed.width + 2 * pad, framed.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((pad + 10, pad + 14, pad + 10 + framed.width, pad + 14 + framed.height), fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    out.alpha_composite(sh); out.paste(framed, (pad, pad)); return out

def ease_pop(t):
    """0..1 -> scale: 0.55 -> 1.08 overshoot -> 1.0 over ~0.2 s."""
    if t <= 0: return None
    d = 0.20
    if t >= d: return 1.0
    u = t / d
    return 0.55 + 0.53 * math.sin(u * math.pi * 0.62) / math.sin(math.pi * 0.62) if u < 0.7 else 1.08 - 0.08 * (u - 0.7) / 0.3

def render_stack(photos, pops, start, dur, out):
    ims = [load_photo(x) for x in photos]
    cards = [card(im) for im in ims]
    bg = ims[0].copy(); s = max(FW / bg.width, FH / bg.height)
    bg = bg.resize((math.ceil(bg.width * s), math.ceil(bg.height * s))).crop((0, 0, FW, FH))
    bg = bg.filter(ImageFilter.GaussianBlur(40)); bg = Image.blend(bg, Image.new("RGB", bg.size, "black"), 0.45).convert("RGBA")
    place = []
    for i, c in enumerate(cards):
        ang = random.uniform(-9, 9) if i else random.uniform(-4, 4)
        dx = random.randint(-70, 70); dy = random.randint(-40, 50)
        place.append((c.rotate(ang, resample=Image.BICUBIC, expand=True), dx, dy))
    frames = int(round(dur * FPS))
    pr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}",
                           "-r", str(FPS), "-i", "-"] + ENC + [out], stdin=subprocess.PIPE)
    for f in range(frames):
        t = start + f / FPS
        fr = bg.copy()
        for (c, dx, dy), pt in zip(place, pops):
            sc = ease_pop(t - pt)
            if sc is None: continue
            cc = c if sc == 1.0 else c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.BILINEAR)
            x = min(max(FW // 2 + dx - cc.width // 2, 12), FW - cc.width - 12); y = int(FH * 0.56) + dy - cc.height // 2
            fr.alpha_composite(cc, (x, y))
        pr.stdin.write(fr.convert("RGB").tobytes())
    pr.stdin.close(); pr.wait()

seg_files = []
for i, (st, kind, src, sin, ex) in enumerate(EDL):
    en = EDL[i + 1][0] if i + 1 < len(EDL) else END
    dur = round(en - st, 3)
    out = os.path.join(segdir, f"{i:02d}.mp4"); seg_files.append(out)
    if kind == "v":
        run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(sin), "-i", src, "-t", str(dur),
             "-vf", cover_filter(ex.get("cx", 0.5), ex.get("transpose"), ex.get("zoom", 1.0), ex.get("cy", 0.5))] + ENC + [out])
        got = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                                   capture_output=True, text=True).stdout)
        if got < dur - 0.05:  # clip too short: hold its last frame
            run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(sin), "-i", src, "-t", str(dur),
                 "-vf", cover_filter(ex.get("cx", 0.5), ex.get("transpose"), ex.get("zoom", 1.0), ex.get("cy", 0.5)) + f",tpad=stop_mode=clone:stop_duration={dur}"] + ENC + ["-t", str(dur), out])
            print(f"seg {i}: source short ({got:.2f}s < {dur:.2f}s), held last frame")
    elif kind == "still":
        render_still(src, dur, out)
    else:
        render_stack(ex["photos"], ex["pops"], st, dur, out)
    print(f"seg {i:02d} {st:6.2f}-{en:6.2f} {kind} {os.path.basename(src) if src else 'stack'}")

lst = os.path.join(W, "concat.txt")
open(lst, "w").write("".join(f"file '{f}'\n" for f in seg_files))
picture = os.path.join(W, "picture.mp4")
run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", picture])

# ---------------------------------------------------------------- text overlays (PIL -> PNG)
FONT = os.path.join(W, "fonts", "Ubuntu-MediumItalic.ttf")
def text_png(text, size, fill, stroke, shadow, path, max_w=FW - 120):
    font = ImageFont.truetype(FONT, size)
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if font.getlength(t) > max_w and cur: lines.append(cur); cur = w_
        else: cur = t
    lines.append(cur)
    lh = int(size * 1.18)
    img = Image.new("RGBA", (FW, lh * len(lines) + 40), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
        for k, ln in enumerate(lines):
            d.text(((FW - font.getlength(ln)) / 2 + 5, 20 + k * lh + 5), ln, font=font, fill=(0, 0, 0, 170))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    d = ImageDraw.Draw(img)
    for k, ln in enumerate(lines):
        d.text(((FW - font.getlength(ln)) / 2, 20 + k * lh), ln, font=font, fill=fill, stroke_width=stroke, stroke_fill="black")
    img.save(path); return img.height

ovl = os.path.join(W, "ovl"); os.makedirs(ovl, exist_ok=True)
th = text_png(TITLE, 54, "white", 4, True, os.path.join(ovl, "title.png"), max_w=FW - 40)
inputs, chain, last = ["-i", picture, "-i", os.path.join(ovl, "title.png")], [], "0:v"
chain.append(f"[{last}][1:v]overlay=0:{int(FH*0.21) - th//2}[t0]"); last = "t0"
for k, (txt, on, off) in enumerate(CAPTIONS):
    fn = os.path.join(ovl, f"cap{k}.png")
    h = text_png(txt, 56, (240, 249, 47), 6, False, fn, max_w=800)
    inputs += ["-i", fn]
    chain.append(f"[{last}][{k+2}:v]overlay=0:{int(FH*0.65) - h//2}:enable='between(t,{on},{off})'[c{k}]"); last = f"c{k}"

# ---------------------------------------------------------------- audio
SR = 48000
vo, _ = librosa.load(VO, sr=SR, mono=True)
mix = np.zeros(int(END * SR) + SR, dtype=np.float32); mix[:len(vo)] += vo
cat = {c["name"]: c for c in json.load(open(os.path.join(SFX, "catalog.json")))}

def place_sfx(name, at, extra_db=0.0, fade_out=None):
    c = cat[name]
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(SFX, c["file"]), "-f", "f32le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32).copy()
    g = 10 ** ((c["gain_db_for_minus14_voice"] + extra_db) / 20)
    if fade_out: n = int(fade_out * SR); y = y[:n].copy(); y[-int(0.25 * SR):] *= np.linspace(1, 0, int(0.25 * SR))
    s = int((at - c["sync_at_s"]) * SR)
    if s < 0: y = y[-s:]; s = 0
    e = min(len(mix), s + len(y)); mix[s:e] += g * y[:e - s]

def pop(at, pitch=1.0, db=-15.0):
    n = int(0.09 * SR); t = np.arange(n) / SR
    f = (950 * pitch) * np.exp(-t * 28) + 260 * pitch
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t * 55)
    click = np.random.randn(int(0.004 * SR)) * np.linspace(1, 0, int(0.004 * SR)) * 0.35
    y[:len(click)] += click
    y = y / np.abs(y).max() * 10 ** (db / 20)
    s = int(at * SR); mix[s:s + n] += y.astype(np.float32)

place_sfx("Reverse_Bass", 1.78, -2)                       # rises into "paanch"
place_sfx("THE_Boom_Sound_Effect", 2.28, 0, fade_out=1.6)  # lands on "mehenga"
place_sfx("Quick_whoosh", 5.55, -5)                        # first caption
place_sfx("Lit_heartbeat1", 13.45, -1)                     # after "the villain,"
place_sfx("Bass_Explosion", 14.10, -1, fade_out=1.2)       # "8,000"
place_sfx("Lit_body_punch", 14.10, -6)
place_sfx("Quick_whoosh", 15.42, -6)                       # electricity caption
for k, (st, kind, src, sin, ex) in enumerate(EDL):
    if kind == "stack":
        for j, t in enumerate(ex["pops"]):
            pop(t, pitch=random.uniform(0.85, 1.25), db=-16 if j else -14)
place_sfx("Lit_whoosh+punch", 24.58, -6)                   # "khaata kaun hai" punchline
place_sfx("My_fav_whoosh", 36.12, -4)                      # out of the photo piles
place_sfx("Whoosh_4", 43.40, -4)                           # subscriptions
place_sfx("Quick_whoosh", 49.08, -4)                       # CTA

mix = mix[:int(END * SR)]
aud = os.path.join(W, "mix.wav"); sf.write(aud, mix, SR)
inputs += ["-i", aud]
na = len(CAPTIONS) + 2
run(["ffmpeg", "-loglevel", "error", "-y"] + inputs + ["-filter_complex", ";".join(chain) +
     f";[{na}:a]loudnorm=I=-14:TP=-1:LRA=7[a]", "-map", f"[{last}]", "-map", "[a]",
     "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", str(END), OUT])
print("done", OUT, END)
