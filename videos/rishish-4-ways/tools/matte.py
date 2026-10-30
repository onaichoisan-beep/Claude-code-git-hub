"""Cut the person out of a clip range → transparent VP9 WebM (for text-behind-head).

usage: python matte.py IN.mp4 START DUR OUT.webm
"""
import subprocess, sys
import cv2, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

src, start, dur, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
W, H, FPS = 1920, 1080, 30

seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path="/opt/alab/models/selfie_multiclass.tflite"),
    running_mode=vision.RunningMode.IMAGE, output_confidence_masks=True))

dec = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", src,
                        "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
                        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libvpx-vp9",
                        "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "24", "-row-mt", "1",
                        "-deadline", "realtime", "-cpu-used", "5", "-auto-alt-ref", "0", out],
                       stdin=subprocess.PIPE)
prev = None
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    res = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
    bg = res.confidence_masks[0].numpy_view()
    a = cv2.resize(1.0 - bg, (W, H), interpolation=cv2.INTER_LINEAR)
    prev = a if prev is None else 0.6 * a + 0.4 * prev   # temporal smoothing kills edge flicker
    m = np.clip((prev - 0.35) / 0.3, 0, 1)                 # tighten the soft edge
    m = cv2.GaussianBlur(m, (5, 5), 0)
    enc.stdin.write(np.dstack([rgb, (m * 255).astype(np.uint8)]).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
print("matte", out)
