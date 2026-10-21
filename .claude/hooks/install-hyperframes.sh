#!/bin/bash
# Installs the HyperFrames CLI and its render browser at session start.
set -euo pipefail

# Only run in Claude Code cloud sessions; local machines manage their own tools.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if ! command -v hyperframes >/dev/null 2>&1; then
  npm install -g hyperframes >/dev/null 2>&1
fi

# Finds a cached Chrome Headless Shell or downloads one (no-op when present).
hyperframes browser ensure >/dev/null 2>&1

echo "HyperFrames $(hyperframes --version) ready"
