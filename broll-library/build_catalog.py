#!/usr/bin/env python3
"""Regenerate <brand>/CATALOG.md from <brand>/catalog.json.   python3 broll-library/build_catalog.py pacagen"""
import json, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); b = sys.argv[1]
d = json.load(open(os.path.join(HERE, b, "catalog.json"))); C = d["clips"]
tot = sum(c["duration_s"] for c in C); hdr = [c["id"] for c in C if c["hdr"]]
odd = [f'`{c["id"]}` ({c["resolution"]})' for c in C if c["resolution"] not in ("2160x3840",)]
shoots = Counter(c.get("shoot", "A") for c in C)
L = [f'# {d["brand"]} B-roll library\n',
     f'**Product:** {d["product"]}  ',
     "**Drive folders:** " + " · ".join(f"[folder {i+1}]({u})" for i, u in enumerate(d["drive_folders"])) + "  ",
     f'**Clips:** {len(C)} unique · {int(tot//60)} min {int(tot%60)} s total. Duplicates on Drive are merged (see `also_named` in catalog.json).  ',
     "**Audio:** room sound only, no talking. Mute it or use it as quiet ambience.\n",
     "## Shoots: don't mix homes in one ad unless the script allows it\n", "| Shoot | Clips | What |", "|---|---|---|"]
L += [f'| **{k}** | {shoots[k]} | {v} |' for k, v in d["shoots"].items()]
if d.get("creators"):
    L += ["", "**Creators:** " + " · ".join(f"**{k}**: {v}" for k, v in d["creators"].items())]
if d.get("excluded"):
    L += ["", "**Excluded:** " + "; ".join(f'`{e["file"]}` ({e["reason"]})' for e in d["excluded"])]
L += ["", f'> ⚠ **HDR (HLG) clips ({len(hdr)}):** convert to Rec.709/SDR in your NLE or they look washed out next to SDR clips: ' + ", ".join(f"`{h}`" for h in hdr),
      "", "> ⚠ **Not standard 4K vertical:** " + ", ".join(odd) + ". Most are slightly cropped vertical; `BOND-10` is landscape.",
      "", "**Get files:** `python3 broll-library/fetch.py " + b + " --id SUP-11` · `--tag hook` · `--category supplement` · `--shoot B` · `--cat salem`\n",
      "---\n", "## Story map: which clip for which beat\n", "| Ad beat | Clips (A/B/C = shoot) |", "|---|---|"]
L += [f"| **{k}** | {v} |" for k, v in d["story_map"]]
L += ["", "## Quick index\n", "| ID | Shoot | Clip | Length | Cat |", "|---|---|---|---|---|"]
L += [f'| `{c["id"]}` | {c.get("shoot","A")} | {c["title"]} | {c["duration_s"]}s | {c["cat"]} |' for c in C]
L.append("\n---")
for cat in d["categories"]:
    cs = [c for c in C if c["category"] == cat["key"]]
    if not cs: continue
    L.append(f'\n## {cat["label"]}  ({len(cs)} clips)\n')
    for c in cs:
        fl = (["⚠ HDR"] if c["hdr"] else []) + ([f'⚠ {c["resolution"]}'] if c["resolution"] != "2160x3840" else [])
        L.append(f'### `{c["id"]}` {c["title"]}\n![]({c["thumb"]})\n')
        L.append(f'- **File:** `{c["source_file"]}`' + (f' (also on Drive as `{"`, `".join(c["also_named"])}`)' if c["also_named"] else ""))
        L.append(f'- **Shoot {c.get("shoot","A")}** · {c["duration_s"]}s · {c["resolution"]} · {c["fps"]}fps · {c["shot"]}' + (" · " + " ".join(fl) if fl else ""))
        if c["description"] != c["title"]: L.append(f'- **What\'s in it:** {c["description"]}')
        L.append(f'- **Use for:** {c["use_for"]}')
        if c.get("best_section"): L.append(f'- **Best section:** {c["best_section"]}')
        if c.get("notes"): L.append(f'- **Note:** {c["notes"]}')
        L.append(f'- **Cat:** {c["cat"]} · **Tags:** {", ".join(c["tags"])}\n')
open(os.path.join(HERE, b, "CATALOG.md"), "w").write("\n".join(L))
print("wrote", len(C), "clips")
