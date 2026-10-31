#!/usr/bin/env bash
# Build script: generates output/ from src/ via Python.
# Run from project root: ./build-output.sh
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
if [ -x .venv/bin/python ]; then PY=.venv/bin/python; else PY=python3; fi
"$PY" src/build.py
