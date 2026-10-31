"""Fetch real foley from Openverse (CC0 / CC BY only) into a project.

  python3 fetch_sfx.py <project_dir> name="search query" [name="query" ...]

Each cue becomes <project>/assets/sfx/<name>.wav (48 kHz mono, leading silence trimmed, max 8 s).
CC0 wins over CC BY when both match; clips over 10 s are skipped. Every pick is credited in
<project>/assets/sfx/CREDITS.md. Already-fetched names are kept (delete the file to re-pick).
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.openverse.org/v1/audio/"


def search(q):
    url = API + "?" + urllib.parse.urlencode({"q": q, "license": "cc0,by", "page_size": 20})
    tries, timeout = int(os.environ.get("OPENVERSE_TRIES", 6)), int(os.environ.get("OPENVERSE_TIMEOUT", 90))
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "pixel-shorts/1.0"})
            return json.load(urllib.request.urlopen(req, timeout=timeout))["results"]
        except Exception as e:  # slow API / rate limit: back off and retry
            print(f"  search retry {attempt + 1}: {e}")
            time.sleep(2 ** (attempt + 1))
    return []


def pick(results):
    ok = [r for r in results if r.get("license") in ("cc0", "by") and r.get("url")
          and 300 <= (r.get("duration") or 0) <= 10000]
    # keep relevance order, but CC0 in the top few beats CC BY
    ranked = sorted(enumerate(ok), key=lambda ir: ir[0] + (0 if ir[1]["license"] == "cc0" else 3))
    return [r for _, r in ranked]


def fetch(proj, name, q):
    out_dir = os.path.join(proj, "assets", "sfx")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, name + ".wav")
    if os.path.exists(dst):
        print(f"{name}: kept")
        return None
    for r in pick(search(q))[:4]:
        raw = os.path.join(out_dir, name + ".src")
        try:
            req = urllib.request.Request(r["url"], headers={"User-Agent": "pixel-shorts/1.0"})
            open(raw, "wb").write(urllib.request.urlopen(req, timeout=90).read())
            af = "silenceremove=start_periods=1:start_threshold=-45dB,atrim=end=8,loudnorm=I=-16:TP=-1.5"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ac", "1", "-ar", "48000", dst],
                           check=True)
        except Exception as e:
            print(f"  {name}: skip {r.get('title')!r}: {e}")
            continue
        finally:
            if os.path.exists(raw):
                os.remove(raw)
        lic = "CC0" if r["license"] == "cc0" else "CC BY " + (r.get("license_version") or "")
        credit = f"- `{name}.wav`: \"{r.get('title')}\" by {r.get('creator') or 'unknown'} ({lic}) {r.get('foreign_landing_url')}"
        print(f"{name}: {r.get('title')!r} ({lic}, {r['duration'] / 1000:.1f}s)")
        return credit
    print(f"{name}: NO MATCH for {q!r}")
    return None


def main():
    proj = sys.argv[1]
    credits_path = os.path.join(proj, "assets", "sfx", "CREDITS.md")
    lines = []
    for arg in sys.argv[2:]:
        name, q = arg.split("=", 1)
        c = fetch(proj, name, q)
        if c:
            lines.append(c)
    if lines:
        new = not os.path.exists(credits_path)
        with open(credits_path, "a") as f:
            if new:
                f.write("# Sound credits (Openverse; CC0 needs none, CC BY must be credited where published)\n\n")
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
