#!/usr/bin/env python3
"""Download B-roll from a library's Google Drive source into organised folders.

  python3 broll-library/fetch.py pacagen                  # every clip
  python3 broll-library/fetch.py pacagen --category in-use
  python3 broll-library/fetch.py pacagen --tag hook --tag funny
  python3 broll-library/fetch.py pacagen --id USE-05 --id PRD-01
  python3 broll-library/fetch.py pacagen --shoot B --cat salem
  python3 broll-library/fetch.py pacagen --list           # print only, no download

Files land in broll-library/<brand>/media/<NN_category>/<ID>_<name>.<ext>
(gitignored). Needs `pip install gdown`.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brand")
    ap.add_argument("--id", action="append", default=[])
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--category", action="append", default=[])
    ap.add_argument("--cat", help="cat name, e.g. siamese / ragdoll / tiger / squirrel / salem")
    ap.add_argument("--shoot", help="A / B / C (see CATALOG.md)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--out", help="output dir (default: <brand>/media)")
    a = ap.parse_args()

    lib = os.path.join(HERE, a.brand)
    cat = json.load(open(os.path.join(lib, "catalog.json")))
    order = {c["key"]: i + 1 for i, c in enumerate(cat["categories"])}
    clips = [c for c in cat["clips"]
             if (not a.id or c["id"] in a.id)
             and (not a.tag or set(a.tag) & set(c["tags"]))
             and (not a.category or c["category"] in a.category)
             and (not a.cat or a.cat in c["cat"])
             and (not a.shoot or c.get("shoot", "A") == a.shoot)]
    if not clips:
        sys.exit("No clips match.")
    for c in clips:
        print(f'{c["id"]:8s} {c["duration_s"]:5.1f}s  {c["title"]}')
    if a.list:
        return
    try:
        import gdown
    except ImportError:
        sys.exit("pip install gdown")
    out = a.out or os.path.join(lib, "media")
    for c in clips:
        d = os.path.join(out, f'{order[c["category"]]:02d}_{c["category"]}')
        os.makedirs(d, exist_ok=True)
        dst = os.path.join(d, c["organised_name"])
        if os.path.exists(dst):
            continue
        for fid in c["drive_file_ids"]:  # fall back to duplicate uploads
            try:
                if gdown.download(id=fid, output=dst, quiet=True):
                    break
            except Exception as e:
                print("  retry:", e)
        print(("ok   " if os.path.exists(dst) else "FAIL ") + dst)

if __name__ == "__main__":
    main()
