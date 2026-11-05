#!/usr/bin/env bash
# render_queue.sh <slug>... : check + render each project in turn (renders/video.mp4), logging to renders/render.log
V="$(cd "$(dirname "$0")/.." && pwd)"
for s in "$@"; do
  cd "$V/$s" || continue
  npx hyperframes check > renders/check.log 2>&1
  npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4 > renders/render.log 2>&1 && echo "RENDERED $s" || echo "FAILED $s"
done
