"""Drop CREDITS.md lines for sounds that are no longer in assets/sfx/.  python3 prune_credits.py <project>"""
import os
import re
import sys

d = os.path.join(sys.argv[1], "assets", "sfx")
p = os.path.join(d, "CREDITS.md")
if os.path.exists(p):
    keep = []
    for ln in open(p).read().splitlines():
        m = re.match(r"- `([^`]+)`", ln)
        if m and not os.path.exists(os.path.join(d, m.group(1))):
            continue
        keep.append(ln)
    open(p, "w").write("\n".join(keep) + "\n")
