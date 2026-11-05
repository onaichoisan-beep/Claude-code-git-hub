"""Open-source sound effects for the pixel shorts. House rule: sound effects come from OPEN SOURCE.

    import sys, os; sys.path.insert(0, HERE)
    os.environ["SFX_DUR"] = str(DUR)          # before importing sfxlib
    from sfxlib import *
    import osfx
    osfx.project(ROOT)                        # freeze every sound this film uses into ROOT/assets/sfx

    fx.put(osfx.sound("impactPlate_heavy_002"), t, 0.6)         # CC0 packs: Kenney.nl + OpenGameArt
    fx.put(osfx.openverse("thunder", "thunder clap"), t, 0.5)   # Openverse / Freesound, CC0 or CC BY
    fx.put(osfx.sfxr("explosion", seed=7), t, 0.4)              # jsfxr 8-bit generator (Unlicense)
    fx.put(osfx.lib("whoosh-cinematic"), t, 0.3)                # bundled HyperFrames library

Sources, best first:
  1. Real recordings with open licences: CC0 packs from Kenney.nl (impact, RPG, interface, sci-fi, digital,
     casino, UI, voiceover, jingles) and OpenGameArt (100+100 general SFX, 80 creatures, water/splash,
     bangs/fireworks, sci-fi, retro synth), then Openverse (CC0 / CC BY only; mostly Freesound).
     osfx.find("splash") lists what the packs have.
  2. Open-source generators: jsfxr (sfxr presets, perfect for pixel art) and the numpy kits in this folder
     (sfxlib.py cinematic hits, foley.py story foley), also the fallback when a download fails.
Every downloaded sound lands in the shared cache videos/_sfx_library/ (gitignored) and a copy is frozen into
the project (assets/sfx/<key>.wav), so a project re-synthesises identically on any machine. CC BY sounds are
written to the project's assets/sfx/CREDITS.md; put those credits in the post caption too.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import numpy as np

from sfxlib import LIB, SR, load

HERE = os.path.dirname(os.path.abspath(__file__))


def _videos_dir():
    d = HERE
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, "_engine")):
            return d
        d = os.path.dirname(d)
    return HERE


VIDEOS = _videos_dir()
CACHE = os.path.join(VIDEOS, "_sfx_library")
ENGINE = os.path.join(VIDEOS, "_engine")
_PROJ = None
_UA = {"User-Agent": "pixel-shorts/2.0"}

KENNEY_PACKS = ["impact-sounds", "rpg-audio", "interface-sounds", "sci-fi-sounds", "digital-audio",
                "casino-audio", "ui-audio", "voiceover-pack", "music-jingles"]


def project(root):
    """Freeze every sound used from now on into <root>/assets/sfx (and its credits into CREDITS.md)."""
    global _PROJ
    _PROJ = root
    os.makedirs(os.path.join(root, "assets", "sfx"), exist_ok=True)


def _freeze(key, src, credit=None):
    """copy a cached sound into the project as 48 kHz mono wav; return the project path"""
    if not _PROJ:
        return src
    dst = os.path.join(_PROJ, "assets", "sfx", key + ".wav")
    if not os.path.exists(dst):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", str(SR), dst], check=True)
    if credit:
        cp = os.path.join(_PROJ, "assets", "sfx", "CREDITS.md")
        old = open(cp).read() if os.path.exists(cp) else "# Sound credits (CC0 needs none; CC BY must be credited where published)\n\n"
        line = f"- `{key}.wav`: {credit}"
        if line not in old:
            open(cp, "w").write(old.rstrip("\n") + "\n" + line + "\n")
    return dst


def _frozen(key):
    if _PROJ:
        p = os.path.join(_PROJ, "assets", "sfx", key + ".wav")
        if os.path.exists(p):
            return load(p)
    return None


# ------------------------------------------------------------------ CC0 sound packs (Kenney.nl + OpenGameArt)
# Every pack here is CC0 (public domain): no credit needed, free for commercial use.
PACKS = {
    "kenney/impact": "https://kenney.nl/assets/impact-sounds",
    "kenney/rpg": "https://kenney.nl/assets/rpg-audio",
    "kenney/interface": "https://kenney.nl/assets/interface-sounds",
    "kenney/scifi": "https://kenney.nl/assets/sci-fi-sounds",
    "kenney/digital": "https://kenney.nl/assets/digital-audio",
    "kenney/casino": "https://kenney.nl/assets/casino-audio",
    "kenney/ui": "https://kenney.nl/assets/ui-audio",
    "kenney/voiceover": "https://kenney.nl/assets/voiceover-pack",
    "kenney/jingles": "https://kenney.nl/assets/music-jingles",
    "oga/100-sfx": "https://opengameart.org/content/100-cc0-sfx",
    "oga/100-sfx-2": "https://opengameart.org/content/100-cc0-sfx-2",
    "oga/creatures": "https://opengameart.org/content/80-cc0-creature-sfx",
    "oga/retro-synth": "https://opengameart.org/content/50-cc0-retro-synth-sfx",
    "oga/scifi": "https://opengameart.org/content/50-cc0-sci-fi-sfx",
    "oga/bangs-fireworks": "https://opengameart.org/content/25-cc0-bang-firework-sfx",
    "oga/water-splash": "https://opengameart.org/content/40-cc0-water-splash-slime-sfx",
}
_ZIP = re.compile(r'https://(?:kenney\.nl/media/pages/assets/[^"\']+|opengameart\.org/sites/default/files/[^"\'/]+)\.zip')


def fetch_packs(names=None):
    """Download the CC0 packs into the shared cache (once per machine, ~40 MB)."""
    root = os.path.join(CACHE, "packs")
    for name in names or PACKS:
        dest = os.path.join(root, name)
        if os.path.isdir(dest) and os.listdir(dest):
            continue
        try:
            page = urllib.request.urlopen(urllib.request.Request(PACKS[name], headers=_UA), timeout=60).read().decode("utf8", "ignore")
            if "CC0" not in page:
                print(f"packs: {name} is no longer CC0, skipped")
                continue
            os.makedirs(dest, exist_ok=True)
            for url in sorted(set(_ZIP.findall(page)) | set(m.group(0) for m in _ZIP.finditer(page))):
                z = os.path.join(dest, "pack.zip")
                open(z, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=180).read())
                with zipfile.ZipFile(z) as zf:
                    zf.extractall(dest)
                os.remove(z)
            print(f"packs: {name} ok")
        except Exception as e:  # noqa: BLE001 - offline / site changed: the synth kits still work
            print(f"packs: {name} failed ({e})")
    _index(rebuild=True)


def _index(rebuild=False):
    p = os.path.join(CACHE, "packs", "index.json")
    if os.path.exists(p) and not rebuild:
        return json.load(open(p))
    idx = {}
    root = os.path.join(CACHE, "packs")
    for dp, _, fs in sorted(os.walk(root)):
        pack = os.path.relpath(dp, root).split(os.sep)[:2]
        for f in sorted(fs):
            if f.lower().endswith((".ogg", ".wav", ".mp3", ".flac")) and "preview" not in f.lower():
                stem = os.path.splitext(f)[0]
                idx.setdefault(stem, os.path.join(dp, f))
                idx.setdefault("/".join(pack) + "/" + stem, os.path.join(dp, f))
    os.makedirs(root, exist_ok=True)
    json.dump(idx, open(p, "w"), indent=0, sort_keys=True)
    return idx


def find(word=""):
    """list pack sounds whose name contains word, e.g. find('footstep'), find('splash'), find('growl')"""
    idx = _index()
    if not idx:
        fetch_packs()
        idx = _index()
    return sorted(k for k in idx if "/" in k and word.lower() in k.lower())


def sound(name, fallback=None, dur=None):
    """a CC0 pack sound by name ('impactPlate_heavy_002', or 'oga/creatures/<file>'); the first name that starts
    with it if not exact; fallback if unavailable"""
    key = "cc0_" + re.sub(r"[^A-Za-z0-9_-]+", "_", name.split("/")[-1])
    x = _frozen(key)
    if x is not None:
        return x
    idx = _index()
    if not idx:
        fetch_packs()
        idx = _index()
    path = idx.get(name) or next((idx[k] for k in sorted(idx) if k.split("/")[-1].startswith(name.split("/")[-1])), None)
    if not path:
        print(f"osfx: no pack sound '{name}'")
        return fallback if fallback is not None else np.zeros(10)
    return load(_freeze(key, path), 0, dur)


kenney = sound  # older name


# ------------------------------------------------------------------ Openverse (CC0 / CC BY)
def openverse(name, query, fallback=None, dur=None, tries=3):
    """a real recording from Openverse (Freesound and others), CC0 or CC BY only, cached library-wide.
    Openverse is often slow or down: this gives up quickly and returns the fallback."""
    key = "ov_" + name
    x = _frozen(key)
    if x is not None:
        return x
    cache = os.path.join(CACHE, "openverse")
    src = os.path.join(cache, "assets", "sfx", name + ".wav")
    credits = os.path.join(cache, "credits.json")
    cmap = json.load(open(credits)) if os.path.exists(credits) else {}
    if not os.path.exists(src):
        sys.path.insert(0, ENGINE)
        import fetch_sfx
        os.environ.setdefault("OPENVERSE_TRIES", str(tries))
        os.environ.setdefault("OPENVERSE_TIMEOUT", "25")
        try:
            c = fetch_sfx.fetch(cache, name, query)
        except Exception as e:  # noqa: BLE001
            print(f"osfx: openverse '{query}' failed ({e})")
            c = None
        if c:
            cmap[name] = c.split(": ", 1)[1] if ": " in c else c
            json.dump(cmap, open(credits, "w"), indent=1)
    if not os.path.exists(src):
        return fallback if fallback is not None else np.zeros(10)
    credit = cmap.get(name, "")
    return load(_freeze(key, src, credit if "CC BY" in credit else None), 0, dur)


# ------------------------------------------------------------------ jsfxr (open-source 8-bit generator)
def sfxr(preset, seed=1, fallback=None):
    """an sfxr sound: pickupCoin laserShoot explosion powerUp hitHurt jump blipSelect synth tone click random,
    or a b58 code copied from https://sfxr.me. Deterministic per seed."""
    key = f"sfxr_{preset if len(preset) < 24 else preset[:12]}_{seed}"
    x = _frozen(key)
    if x is not None:
        return x
    node_dir = os.path.join(CACHE, "node")
    try:
        if not os.path.exists(os.path.join(node_dir, "node_modules", "jsfxr")):
            os.makedirs(node_dir, exist_ok=True)
            subprocess.run(["npm", "install", "--silent", "--prefix", node_dir, "jsfxr@1.4.1"], check=True)
        out = os.path.join(CACHE, "sfxr", key + ".wav")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if not os.path.exists(out):
            subprocess.run(["node", os.path.join(ENGINE, "sfxr_gen.mjs"), node_dir, preset, str(seed), out], check=True)
        return load(_freeze(key, out))
    except Exception as e:  # noqa: BLE001
        print(f"osfx: sfxr failed ({e})")
        return fallback if fallback is not None else np.zeros(10)


# ------------------------------------------------------------------ the bundled HyperFrames library
def lib(name):
    """whoosh whoosh-short whoosh-cinematic pop sparkle glitch-1/2/3 notification error chime riser
    impact-bass-1 impact-bass-2 ping click click-soft typing key-press"""
    x = load(os.path.join(LIB, name + ".mp3")) if LIB else None
    return x if x is not None else np.zeros(10)


if __name__ == "__main__":
    # python3 osfx.py packs            -> download every CC0 pack
    # python3 osfx.py find footstep     -> list matching pack sounds
    if len(sys.argv) > 1 and sys.argv[1] == "packs":
        fetch_packs()
        print(len([k for k in _index() if "/" in k]), "CC0 sounds in", os.path.join(CACHE, "packs"))
    elif len(sys.argv) > 2 and sys.argv[1] == "find":
        print("\n".join(find(sys.argv[2])))
    elif len(sys.argv) > 1 and sys.argv[1] == "catalog":  # python3 osfx.py catalog > SOUNDS.md
        import collections
        by = collections.defaultdict(list)
        for k in find(""):
            by["/".join(k.split("/")[:2])].append(k.split("/")[-1])
        print("# CC0 sound packs (osfx.sound(name))\n")
        print("Public-domain (CC0) recordings, downloaded once into `videos/_sfx_library/packs/` by "
              "`python3 videos/_engine/osfx.py packs`. Use a name exactly, or its prefix (`osfx.sound(\"splash\")` "
              "picks the first splash). `python3 videos/_engine/osfx.py find <word>` lists matches.\n")
        for pk, v in by.items():
            groups = collections.Counter(re.sub(r"[ _-]*\(?\d+\)?$", "", x) or x for x in v)
            items = ", ".join(f"`{g}`" + (f" ×{n}" if n > 1 else "") for g, n in sorted(groups.items()))
            print(f"- **{pk}** ({len(v)}, [source]({PACKS.get(pk, '')})): {items}")
