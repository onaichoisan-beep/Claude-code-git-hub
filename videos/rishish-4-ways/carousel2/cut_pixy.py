"""Cut PIXY (Dr. Dragon) poses out of the character sheet as transparent PNGs, upscaled 3x."""
import cv2, numpy as np

sheet = cv2.imread("sheet.png")
BG = np.array([184, 239, 254], np.float32)    # sheet background (BGR)
LINE = np.array([143, 213, 233], np.float32)  # faint ruled lines on the sheet

# name: (x0, y0, x1, y1) in sheet pixels; generous boxes, trimmed to the figure afterwards
BOX = {
    "front": (140, 222, 365, 722), "attitude": (495, 222, 740, 722), "walk": (1240, 222, 1475, 722),
    "wave": (95, 1155, 250, 1482), "point": (300, 1155, 478, 1482), "think": (515, 1155, 660, 1482),
    "celebrate": (720, 1155, 880, 1482), "shrug": (905, 1155, 1115, 1482), "facepalm": (1150, 1155, 1295, 1482),
    "hips": (1355, 1155, 1515, 1482),
}
faces = ["friendly", "joy", "sly", "gusto", "confusion", "watching", "upset", "angry", "shock"]
for i, n in enumerate(faces):
    cx = 147 + i * 163
    BOX["face_" + n] = (cx - 76, 866, cx + 76, 1024)

for name, (x0, y0, x1, y1) in BOX.items():
    crop = sheet[y0:y1, x0:x1]
    big = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    d = np.minimum(np.linalg.norm(big - BG, axis=2), np.linalg.norm(big - LINE, axis=2))
    alpha = np.clip((d - 12) / 18, 0, 1)
    # keep only the figure: largest connected blob (drops stray label bits at crop edges)
    m = (alpha > 0.5).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    blob = cv2.dilate((lab == keep).astype(np.uint8), np.ones((5, 5), np.uint8))
    alpha *= blob
    ys, xs = np.where(alpha > 0.05)
    out = np.dstack([big, alpha * 255]).astype(np.uint8)[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cv2.imwrite(f"pixy/{name}.png", out)
print("cut", len(BOX))
