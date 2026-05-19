"""Create Chroma index on first run if empty (Docker / deploy)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import settings
from src.ingestion.indexer import get_collection_stats, ingest_knowledge_base


def main() -> None:
    if not settings.api_key_configured:
        print("SKIP: OPENAI_API_KEY not set — index not created.")
        return

    stats = get_collection_stats()
    if stats.get("chunk_count", 0) > 0:
        print(f"Index OK: {stats['chunk_count']} chunks")
        return

    print("Index empty — running ingest…")
    result = ingest_knowledge_base(reset=True)
    print(f"Ingest done: {result['chunks']} chunks")


if __name__ == "__main__":
    main()
