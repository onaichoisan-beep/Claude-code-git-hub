"""Magadh Panthor Chhath offer reel: segments -> base -> FX (flash, film burn, logo, address card) -> mux."""
import subprocess as sp, numpy as np, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = os.path.dirname(os.path.abspath(__file__))
os.chdir(S)
W, H, FPS = 1080, 1920, 30
TOTAL = 50.6
R, A = 'real/', 'ai/'
# crop presets on 720x1280 sources: (x, y, w, h)
TOPCUT = lambda top: (int((720 - (1280 - top) * 720 / 1280) / 2), top, int((1280 - top) * 720 / 1280) // 2 * 2, 1280 - top)

# (dst_start, src, src_in, speed, crop, note)
EDL = [
    (0.00, R + 'R02.mp4', 2.60, 1.0, (44, 0, 630, 1120), 'night nets slog - "ab paison ki kami"'),
    (1.90, R + 'R03.mp4', 24.45, 1.0, None, 'kid posing with helmet - "aapke bachche"'),
    (3.30, R + 'R10.mp4', 9.60, 1.0, None, 'nets drive - "cricketer banne ke sapne"'),
    (4.95, R + 'R05.mp4', 6.45, 1.0, None, 'sled run past MAGADH PANTHOR CRICKET CLUB wall'),
    (7.40, R + 'R03.mp4', 30.00, 1.0, None, 'team walking - "BPL vidyarthiyon"'),
    (9.20, R + 'R11.mp4', 3.50, 1.0, None, 'squad warm-up - "chhath special offer"'),
    (11.10, R + 'R05.mp4', 0.00, 1.0, None, 'sled close-up - "aarthik roop se"'),
    (13.00, R + 'R01.mp4', 9.60, 1.0, None, 'nets batting - "pratibhashali bachchon"'),
    (15.95, R + 'R07.mp4', 45.90, 1.0, TOPCUT(250), 'boys in room - "1 mahine ka hostel free"'),
    (18.25, A + 'A3.mp4', 2.30, 0.76, None, 'AI: HOSTEL + FOOD / FREE - "bhojan bhi free"'),
    (20.75, R + 'R07.mp4', 72.60, 1.0, TOPCUT(250), 'boys in hostel beds - "ji haan, suvidha"'),
    (23.75, A + 'A3.mp4', 4.45, 0.72, None, 'AI: ONLY ADMISSION FEE'),
    (26.30, R + 'R12.mp4', 7.40, 1.0, None, 'batter walks out - "agar aapka bachcha"'),
    (28.00, R + 'R08.mp4', 65.45, 1.0, None, 'openers glove-bump - "bhavishya"'),
    (29.75, R + 'R10.mp4', 2.90, 1.0, None, 'lofted shot - "pratibha dikhane"'),
    (31.40, R + 'R08.mp4', 100.00, 1.0, None, 'batter walks off under lights - "sunehra mauka"'),
    (33.05, R + 'R06.mp4', 2.00, 1.0, TOPCUT(345), 'club nets at night - "aaj hi sampark karein"'),
    (34.70, A + 'A2.mp4', 3.75, 1.0, None, 'AI: MAGADH PANTHOR CRICKET CLUB title'),
    (36.60, R + 'R12.mp4', 3.80, 1.0, None, 'batters padded up (address card)'),
    (39.10, R + 'R11.mp4', 56.40, 1.0, None, 'push-up rows (address card)'),
    (41.60, R + 'R09.mp4', 2.00, 1.0, None, 'nets batting (address card / pincode)'),
    (43.60, A + 'A1.mp4', 4.25, 0.55, None, 'AI: phone number 97982 70035'),
    (47.60, A + 'A1.mp4', 7.20, 0.95, None, 'AI: logo reveal outro'),
]
CUTS = [e[0] for e in EDL[1:]]


def fr(t): return int(round(t * FPS))


def render_segments():
    os.makedirs('seg', exist_ok=True)
    for i, (t0, src, sin, spd, crop, note) in enumerate(EDL):
        t1 = EDL[i + 1][0] if i + 1 < len(EDL) else TOTAL
        nf = fr(t1) - fr(t0)
        need = (nf / FPS) * spd + 0.3
        vf = []
        if crop: vf.append('crop=%d:%d:%d:%d' % (crop[2], crop[3], crop[0], crop[1]))
        vf += [f'scale={W}:{H}:flags=lanczos', 'setsar=1', f'fps={FPS}']
        if spd != 1.0: vf.insert(0, f'setpts=PTS/{spd}')
        if src.startswith(R):
            vf += ['eq=contrast=1.06:saturation=1.12:gamma=0.98', 'unsharp=5:5:0.6']
        vf += ['tpad=stop_mode=clone:stop_duration=3']
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{sin}', '-t', f'{need + 1}', '-i', src,
               '-vf', ','.join(vf), '-frames:v', str(nf), '-an', '-c:v', 'libx264', '-preset', 'fast',
               '-crf', '14', '-pix_fmt', 'yuv420p', f'seg/{i:02d}.mp4']
        sp.run(cmd, check=True)
        print(f'seg {i:02d} {t0:5.2f}-{t1:5.2f} {nf:3d}f {os.path.basename(src)}@{sin} {note}')
    with open('seg/list.txt', 'w') as f:
        for i in range(len(EDL)): f.write(f"file '{i:02d}.mp4'\n")
    sp.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'seg/list.txt', '-c', 'copy', 'base.mp4'], check=True)


# ---------- overlays ----------
LOGO = Image.open('logo.png').convert('RGBA').resize((230, 230), Image.LANCZOS)
LOGO_A = np.asarray(LOGO).astype(np.float32) / 255
LX, LY = W - 230 - 22, 30  # top-right corner


def address_card():
    cw, ch = 860, 330
    im = Image.new('RGBA', (cw + 60, ch + 60), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([30, 38, 30 + cw, 38 + ch], 28, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(14)); im.alpha_composite(sh)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([30, 30, 30 + cw, 30 + ch], 28, fill=(9, 22, 52, 228), outline=(214, 175, 92, 255), width=4)
    gold = (232, 192, 105, 255); white = (255, 255, 255, 255)
    fh = ImageFont.truetype('oswald-latin-700-normal.ttf', 52)
    fb = ImageFont.truetype('montserrat-latin-800-normal.ttf', 46)
    fs = ImageFont.truetype('montserrat-latin-600-normal.ttf', 40)
    cx = 30 + cw // 2
    # pin icon
    px, py = cx - 128, 72
    d.ellipse([px - 17, py - 4, px + 17, py + 30], fill=(229, 57, 53, 255))
    d.polygon([(px - 15, py + 20), (px + 15, py + 20), (px, py + 46)], fill=(229, 57, 53, 255))
    d.ellipse([px - 7, py + 6, px + 7, py + 20], fill=(9, 22, 52, 255))
    d.text((cx + 18, 70), 'VISIT US', font=fh, fill=gold, anchor='mt')
    d.line([cx - 300, 148, cx + 300, 148], fill=(214, 175, 92, 160), width=2)
    d.text((cx, 172), 'Gaurav Market, Above PNB ATM', font=fb, fill=white, anchor='mt')
    d.text((cx, 232), 'Near Creane School', font=fs, fill=white, anchor='mt')
    d.text((cx, 285), 'Gaya, Bihar – 823001', font=fb, fill=gold, anchor='mt')
    return np.asarray(im).astype(np.float32) / 255


CARD = address_card()
CARD_T0, CARD_T1 = 36.75, 43.45
CX, CY = (W - CARD.shape[1]) // 2, 1180


def comp(frame, ov, x, y, alpha=1.0):
    h, w = ov.shape[:2]
    reg = frame[y:y + h, x:x + w]
    a = ov[..., 3:4] * alpha
    frame[y:y + h, x:x + w] = reg * (1 - a) + ov[..., :3] * 255 * a


# film burn texture (low-res, animated), screen-blended near cuts
rng = np.random.default_rng(3)
BW, BH = 72, 128
yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32)


def burn_frame(seed, p):
    """p in [0,1] across the burn; returns HxWx3 float 0..1 at full res."""
    r = np.random.default_rng(seed)
    acc = np.zeros((BH, BW), np.float32)
    for k in range(4):
        cx0, cy0 = r.uniform(-0.2, 1.2) * BW, r.uniform(-0.1, 1.1) * BH
        vx, vy = r.uniform(-40, 40), r.uniform(-80, 80)
        rad = r.uniform(25, 55)
        cx_, cy_ = cx0 + vx * p, cy0 + vy * p
        acc += np.exp(-(((xx - cx_) ** 2) / (rad ** 2) + ((yy - cy_) ** 2) / ((rad * 1.6) ** 2)) * 1.6)
    side = r.integers(0, 2)
    edge = np.exp(-((xx if side == 0 else (BW - xx)) / (BW * 0.35)))
    acc = np.clip(acc * 0.7 + edge * 0.8, 0, 1.4)
    col = np.stack([np.clip(acc * 1.15, 0, 1), np.clip(acc ** 1.6 * 0.62, 0, 1), np.clip(acc ** 3 * 0.25, 0, 1)], -1)
    img = Image.fromarray((col * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    return np.asarray(img).astype(np.float32) / 255


def fx(frame, t, idx):
    # transitions
    for ci, tc in enumerate(CUTS):
        dt = t - tc
        if -0.32 < dt < 0.5:
            # white flash: quick rise into the cut, soft decay out
            w = np.exp(-(dt / 0.07) ** 2) if dt < 0 else np.exp(-dt / 0.11)
            # soft film burn around the cut
            b = np.exp(-((dt - 0.02) / 0.2) ** 2) * 0.62
            if b > 0.02:
                bf = burn_frame(1000 + ci, (dt + 0.32) / 0.82)
                frame[:] = 255 - (255 - frame) * (1 - bf * b)
            if w > 0.01:
                frame[:] = frame + (255 - frame) * (w * 0.85)
    # address card (fade + slide up)
    if CARD_T0 <= t <= CARD_T1:
        a = min(1, (t - CARD_T0) / 0.3, (CARD_T1 - t) / 0.25)
        a = max(0, a)
        off = int((1 - a) * 40)
        comp(frame, CARD, CX, CY + off, a)
    # logo, top-right, whole video
    comp(frame, LOGO_A, LX, LY)
    return frame


def render_fx():
    nf = fr(TOTAL)
    dec = sp.Popen(['ffmpeg', '-v', 'error', '-i', 'base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=sp.PIPE)
    enc = sp.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                    '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', 'fx.mp4'], stdin=sp.PIPE)
    sz = W * H * 3
    for i in range(nf):
        buf = dec.stdout.read(sz)
        if len(buf) < sz: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        f = fx(f, i / FPS, i)
        enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
        if i % 150 == 0: print('fx', i, '/', nf, flush=True)
    enc.stdin.close(); enc.wait(); dec.wait()


def mix_audio():
    inputs = ['-i', 'vo.mp3', '-i', 'bgm.wav']
    parts = ['[0:a]aresample=44100,apad=whole_dur=50.6,asplit=2[vo][vosc]',
             '[1:a]volume=0.32[bg]',
             '[bg][vosc]sidechaincompress=threshold=0.04:ratio=4:attack=20:release=300[bgd]']
    labels = ['[vo]', '[bgd]']
    for k, tc in enumerate(CUTS):
        inputs += ['-i', f'whoosh{k % 4}.wav']
        st = max(0, tc - 0.5)
        d = int(st * 1000)
        parts.append(f'[{k + 2}:a]adelay={d}|{d},volume=0.30[w{k}]')
        labels.append(f'[w{k}]')
    parts.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0,atrim=0:{TOTAL},'
                 'loudnorm=I=-14:TP=-1.5:LRA=11[a]')
    sp.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(parts), '-map', '[a]',
            '-ar', '48000', '-c:a', 'pcm_s16le', 'mix.wav'], check=True)


if __name__ == '__main__':
    steps = sys.argv[1:] or ['seg', 'fx', 'audio', 'mux']
    if 'seg' in steps: render_segments()
    if 'fx' in steps: render_fx()
    if 'audio' in steps: mix_audio()
    if 'mux' in steps:
        sp.run(['ffmpeg', '-v', 'error', '-y', '-i', 'fx.mp4', '-i', 'mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
                'Magadh_Panthor_Chhath_Offer.mp4'], check=True)
        print('done')
