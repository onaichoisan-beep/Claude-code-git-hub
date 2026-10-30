"""Search Wikimedia Commons for landscape photos and download candidates + a contact sheet.

usage: python stock.py OUTDIR "query one" "query two" ...
Writes OUTDIR/<slug>_<n>.jpg, OUTDIR/credits.json, OUTDIR/<slug>_sheet.jpg
"""
import json, os, re, subprocess, sys, time, urllib.parse, urllib.request

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
UA = {"User-Agent": "rishish-video-edit/1.0 (https://github.com/onaichoisan-beep/Claude-code-git-hub)"}
cred_path = os.path.join(out, "credits.json")
credits = json.load(open(cred_path)) if os.path.exists(cred_path) else {}

def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for wait in (3, 30, 60, 120, 240):
        time.sleep(wait)
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
    return {}

def fetch(url):
    for wait in (3, 20, 60, 120):
        time.sleep(wait)
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                return None
    return None

for q in sys.argv[2:]:
    slug = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")
    r = api(dict(action="query", format="json", generator="search", gsrsearch=f"{q} filetype:bitmap",
                 gsrnamespace=6, gsrlimit=30, prop="imageinfo", iiprop="url|size|extmetadata|mime",
                 iiurlwidth=1920))
    pages = sorted(r.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    got = []
    for p in pages:
        ii = p["imageinfo"][0]
        if ii.get("mime") != "image/jpeg" or ii["width"] < 1600 or ii["width"] < ii["height"] * 1.2:
            continue
        fn = os.path.join(out, f"{slug}_{len(got) + 1}.jpg")
        if os.path.exists(fn) and os.path.getsize(fn) > 0:
            data = None
        else:
            data = fetch(ii["thumburl"])
            if data is None:
                continue
            open(fn, "wb").write(data)
        md = ii.get("extmetadata", {})
        credits[os.path.basename(fn)] = dict(
            title=p["title"], page=ii["descriptionurl"],
            license=md.get("LicenseShortName", {}).get("value", "?"),
            artist=re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "?")).strip())
        got.append(fn)
        if len(got) == 4:
            break
    if got:
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y"] + sum([["-i", g] for g in got], []) +
                       ["-filter_complex", "".join(f"[{i}]scale=480:270:force_original_aspect_ratio=increase,crop=480:270[s{i}];" for i in range(len(got))) +
                        "".join(f"[s{i}]" for i in range(len(got))) + f"xstack=inputs={len(got)}:layout=" +
                        "|".join(f"{(i % 3) * 480}_{(i // 3) * 270}" for i in range(len(got))) + ":fill=black" if len(got) > 1 else "[0]scale=480:270",
                        os.path.join(out, f"{slug}_sheet.jpg")])
    print(q, "->", len(got))
json.dump(credits, open(cred_path, "w"), indent=1)
