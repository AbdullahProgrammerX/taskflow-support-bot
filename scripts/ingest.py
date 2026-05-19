"""
Index TaskFlow knowledge base into Chroma.

Usage (from project root, venv active):
  python scripts/ingest.py
  python scripts/ingest.py --reset
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running as: python scripts/ingest.py
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import settings
from src.ingestion.indexer import get_collection_stats, ingest_knowledge_base


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest knowledge base into Chroma")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete and recreate the collection before ingest",
    )
    args = parser.parse_args()

    if not settings.api_key_configured:
        print("ERROR: OPENAI_API_KEY is not set in .env")
        sys.exit(1)

    print(f"Knowledge base: {settings.knowledge_base_dir}")
    print(f"Chroma path:    {settings.chroma_persist_dir}")
    print(f"Chunk size:     {settings.chunk_size} (overlap {settings.chunk_overlap})")
    print(f"Embedding:      {settings.openai_embedding_model}")
    print()

    if args.reset:
        print("Resetting collection...")

    stats = ingest_knowledge_base(reset=args.reset)
    after = get_collection_stats()

    print("Ingest complete.")
    print(f"  Documents:  {stats['documents']}")
    print(f"  Chunks:     {stats['chunks']}")
    print(f"  In Chroma:  {after['chunk_count']}")


if __name__ == "__main__":
    main()
