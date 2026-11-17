# Replace the AI clip's baked "PANTHER SPORTS" with "PANTHOR SPORTS" (tracked patch over base.mp4)
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FPS = 30
T0, T1 = 9.75, 12.70
f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 400)
txt = 'PANTHOR SPORTS'
bb = f.getbbox(txt)
big = Image.new('L', (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), 0)
ImageDraw.Draw(big).text((10 - bb[0], 10 - bb[1]), txt, font=f, fill=255)
big = big.crop(big.getbbox())
COL = (224, 216, 196)


def ramp(t, a, b):
    return float(np.clip((t - a) / (b - a), 0, 1))


for n in range(round(T0 * FPS), round(T1 * FPS)):
    t = n / FPS
    u = t - 10.4
    # tracked from the clip: line-1 cap box grows slowly with the clip's zoom
    left = 193 - 6.4 * u
    h = 61 + 2.7 * u
    top = 908 + 13.6 * u
    right = left + 12.0 * h
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    pa = ramp(t, 9.75, 9.95)
    patch = Image.new('L', (1080, 1920), 0)
    ImageDraw.Draw(patch).rounded_rectangle((left - 30, top - 20, right + 30, top + h + 16), 30, fill=255)
    patch = patch.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * pa))
    navy = Image.new('RGBA', (1080, 1920), (19, 23, 33, 255))
    navy.putalpha(patch)
    im.alpha_composite(navy)
    ta = ramp(t, 9.85, 10.35)
    if ta > 0:
        g = big.resize((int(right - left), int(h)), Image.LANCZOS).point(lambda v: int(v * ta))
        layer = Image.new('RGBA', g.size, COL + (255,))
        layer.putalpha(g)
        txtl = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        txtl.alpha_composite(layer, (int(left), int(top)))
        sh = np.asarray(txtl.filter(ImageFilter.GaussianBlur(6))).copy()
        sh[..., 3] = (sh[..., 3] * 0.35).astype(np.uint8)
        im.alpha_composite(Image.fromarray(sh))
        im.alpha_composite(txtl)
    im.save(f'a2fix/{n - round(T0 * FPS):04d}.png')
