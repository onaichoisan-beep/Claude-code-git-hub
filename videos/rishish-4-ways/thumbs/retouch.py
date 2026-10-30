"""Natural portrait retouch on an RGBA cut-out: skin smoothing that keeps texture,
soft key light on the face, crisper detail, warm grade, and a red rim light on the edge.

usage: python retouch.py IN.png OUT.png
"""
import sys
import cv2, numpy as np

src, out = sys.argv[1:3]
img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
bgr, a = img[:, :, :3].astype(np.float32) / 255, img[:, :, 3].astype(np.float32) / 255
H, W = a.shape

# --- skin mask (YCrCb range), softened and limited to the person
ycc = cv2.cvtColor((bgr * 255).astype(np.uint8), cv2.COLOR_BGR2YCrCb)
skin = cv2.inRange(ycc, (40, 135, 85), (255, 180, 135)).astype(np.float32) / 255
skin = cv2.GaussianBlur(cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)), (0, 0), 6) * a

# --- frequency-separation style smoothing: blur the low frequencies, keep 45% of fine texture
low = cv2.bilateralFilter((bgr * 255).astype(np.uint8), 15, 40, 12).astype(np.float32) / 255
high = bgr - cv2.GaussianBlur(bgr, (0, 0), 2.2)
smooth = np.clip(low + 0.35 * high, 0, 1)
bgr = bgr * (1 - 0.85 * skin[..., None]) + smooth * (0.85 * skin[..., None])

# --- soft key light centred on the face (upper part of the head)
ys, xs = np.where(a > 0.5)
top = ys.min(); row = np.where(a[top + 180] > 0.5)[0]
cx, cy, r = (row.min() + row.max()) / 2, top + 260, (row.max() - row.min()) * 0.9
yy, xx = np.mgrid[0:H, 0:W]
key = np.exp(-(((xx - cx) ** 2 + ((yy - cy) * 1.15) ** 2) / (2 * r ** 2)))
bgr = bgr * (1 + 0.14 * key[..., None])
# lift shadows on skin (under-eyes, jaw) without flattening highlights
bgr = bgr + skin[..., None] * 0.35 * (1 - bgr) * np.clip(0.55 - bgr, 0, 1)

# --- local contrast + crisp detail (eyes, hair, eyebrows)
lab = cv2.cvtColor(np.clip(bgr * 255, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
lab[:, :, 0] = cv2.createCLAHE(clipLimit=1.05, tileGridSize=(8, 8)).apply(lab[:, :, 0])
bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR).astype(np.float32) / 255
sharp = bgr + 0.4 * (bgr - cv2.GaussianBlur(bgr, (0, 0), 1.4))
bgr = sharp * (1 - 0.6 * skin[..., None]) + bgr * (0.6 * skin[..., None])   # don't re-sharpen smoothed skin

# --- warm, slightly richer grade
bgr[:, :, 2] *= 1.04; bgr[:, :, 0] *= 0.96
hsv = cv2.cvtColor(np.clip(bgr, 0, 1).astype(np.float32), cv2.COLOR_BGR2HSV)
hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.08, 0, 1)
bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# --- red rim light hugging the silhouette (strongest on the sides and hair)
edge = np.clip(a - cv2.erode(a, np.ones((3, 3), np.uint8), iterations=12), 0, 1)
edge = cv2.GaussianBlur(edge, (0, 0), 7) * a
rim = np.array([0.18, 0.22, 1.0], np.float32)  # BGR red
bgr = bgr + edge[..., None] * rim * 0.45

res = np.dstack([np.clip(bgr, 0, 1) * 255, a * 255]).astype(np.uint8)
cv2.imwrite(out, res)
print("retouched", out)
