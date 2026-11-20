"""Cut, reframe, grade every shot to 1080x1920@30 so the composition just sequences them.

Shot list = (end_time_sec, source, src_in, speed, crop_center_x or None, note).
Each shot starts where the previous one ended. Times are on the final (sped-up) VO.
"""
import json, subprocess, sys
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Claude-code-git-hub/e8d8199e-3c87-5631-a59d-0d0c44dcb89a/scratchpad")
OUT = Path(__file__).resolve().parent.parent / "assets" / "video"
FPS = 30

def R(n): return str(SCR / "real" / f"VID-20261110-{n}.mp4")
def A(n): return str(SCR / "ai" / f"ai{n}.mp4")

SHOTS = [
    # --- SCENE 1 · HOOK ---
    (1.90,  A(5), 1.70, 1.0, None, "AI kid batting, ground-level, swing"),
    (3.00,  R("WA0024"), 0.50, 1.0, None, "real: young bowler drill"),
    (4.10,  R("WA0029"), 4.30, 1.0, None, "real: bowler run-up close"),
    (5.90,  A(1), 2.10, 1.0, None, "AI father, push-in to hopeful face"),
    (8.30,  A(4), 0.00, 1.0, None, "AI bat + ball close-up"),
    (9.80,  A(4), 2.50, 1.0, None, "AI kid, ball in the air"),
    (11.40, R("WA0043"), 2.20, 1.0, None, "real: coach guiding bowling arm"),
    # --- SCENE 2 · BRAND ---
    (15.40, A(6), 0.00, 1.0, None, "AI navy/orange flare bg - logo reveal"),
    (17.00, R("WA0042"), 5.00, 1.0, None, "real: kid batting indoor nets"),
    (18.78, R("WA0037"), 20.0, 1.0, 0.50, "real: academy rows shadow batting"),
    (21.16, A(2), 1.20, 1.0, None, "AI network lines - kadi"),
    (24.00, A(3), 1.00, 1.0, None, "AI India map - 5 cities / 20 branches"),
    (26.00, R("WA0038"), 23.0, 1.0, 0.58, "real: coach demonstrating to group"),
    (28.00, R("WA0023"), 19.0, 1.0, None, "real: coaches with kids indoor"),
    # --- SCENE 3 · WHAT WE DO ---
    (29.10, R("WA0036"), 22.8, 1.0, None, "real: talent - batting indoor"),
    (30.30, R("WA0024"), 14.0, 1.0, None, "real: age - young bowler"),
    (31.69, R("WA0045"), 2.40, 1.0, None, "real: need - batsman in nets"),
    (33.74, R("WA0033"), 2.00, 1.0, None, "real: coach adjusting stance"),
    (35.30, R("WA0043"), 8.60, 1.0, None, "real: coach shaping action"),
    (36.62, R("WA0041"), 4.30, 1.0, None, "real: coach demo to kids indoor"),
    # --- SCENE 4 · CLOSE + CTA ---
    (38.50, A(1), 0.00, 1.0, None, "AI father watching son play"),
    (41.02, R("WA0019"), 26.0, 1.0, 0.56, "real: kid honoured, team clapping - pehchaan"),
    (43.54, A(5), 0.00, 0.7, None, "AI kid takes stance, slow-mo"),
    (46.14, R("WA0032"), 3.80, 1.0, None, "real: batsman in cage (CTA bg)"),
    (48.01, R("WA0041"), 8.50, 1.0, None, "real: team/coach with kids"),
    (49.90, R("WA0043"), 15.0, 1.0, None, "real: coach guiding"),
    (51.70, R("WA0034"), 0.20, 1.0, None, "real: bowler run-up - shuruaat"),
    (54.98, R("WA0016"), 23.5, 1.0, 0.50, "real: rows of kids marching - kadam"),
    (60.00, A(6), 0.00, 0.78, None, "AI bg - end card"),
]

GRADE_REAL = "eq=contrast=1.08:saturation=1.22:brightness=0.005:gamma=0.97,colorbalance=rm=0.03:bm=-0.03,unsharp=5:5:0.7"
GRADE_AI = "eq=saturation=1.05"

def probe_wh(src):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:stream_side_data=rotation", "-of", "json", src],
                       capture_output=True, text=True).stdout
    s = json.loads(o)["streams"][0]
    w, h = s["width"], s["height"]
    rot = 0
    for sd in s.get("side_data_list", []):
        rot = int(sd.get("rotation", 0))
    if abs(rot) == 90:
        w, h = h, w
    return w, h

def main(only=None):
    OUT.mkdir(parents=True, exist_ok=True)
    edl, start_f = [], 0
    for i, (end, src, sin, speed, cx, note) in enumerate(SHOTS):
        end_f = round(end * FPS)
        n = end_f - start_f
        name = f"s{i:02d}.mp4"
        w, h = probe_wh(src)
        chain = [f"setpts=(PTS-STARTPTS)/{speed}"]
        if speed < 1:
            chain.append(f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1")
        else:
            chain.append(f"fps={FPS}")
        if w > h:  # landscape -> 9:16 crop around cx
            cw = int(h * 9 / 16) // 2 * 2
            x = max(0, min(w - cw, int(cx * w - cw / 2)))
            chain.append(f"crop={cw}:{h}:{x}:0")
        chain.append("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920")
        chain.append(GRADE_AI if "/ai/" in src else GRADE_REAL)
        chain.append("format=yuv420p")
        src_need = n / FPS * speed + 0.2
        if only is None or i in only:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sin:.3f}", "-t", f"{src_need:.3f}", "-i", src,
                            "-vf", ",".join(chain), "-frames:v", str(n), "-an",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", str(FPS),
                            str(OUT / name)], check=True)
            got = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                  "stream=nb_read_frames", "-of", "csv=p=0", str(OUT / name)],
                                 capture_output=True, text=True).stdout.strip()
            flag = "" if int(got) == n else f"  !! got {got} frames"
            print(f"{name} {start_f/FPS:6.2f}-{end_f/FPS:6.2f} ({n}f) {note}{flag}")
        edl.append({"id": f"s{i:02d}", "file": f"assets/video/{name}", "start": start_f / FPS,
                    "dur": n / FPS, "ai": "/ai/" in src, "note": note})
        start_f = end_f
    (OUT.parent.parent / "edl.json").write_text(json.dumps(edl, indent=1))
    ai = sum(s["dur"] for s in edl if s["ai"])
    print(f"AI share: {ai:.1f}s / {start_f/FPS:.1f}s = {ai/(start_f/FPS)*100:.0f}%")

if __name__ == "__main__":
    only = set(map(int, sys.argv[1:])) or None
    main(only)
