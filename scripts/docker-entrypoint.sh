#!/bin/sh
set -e
cd /app
python scripts/ensure_index.py
PORT="${PORT:-8000}"
exec uvicorn src.main:app --host 0.0.0.0 --port "$PORT"
