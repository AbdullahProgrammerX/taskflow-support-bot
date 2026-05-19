#!/bin/sh
set -e
cd /app
python scripts/ensure_index.py
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
