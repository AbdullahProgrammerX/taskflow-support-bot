import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.errors import NotFoundError

from src.config import settings
from src.ingestion.chunker import Chunk, chunk_documents
from src.ingestion.loader import load_markdown_documents
from src.llm.embeddings import embed_texts_batched


def _get_chroma_client() -> chromadb.PersistentClient:
    settings.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(settings.chroma_persist_dir))


def _get_collection(client: chromadb.PersistentClient, reset: bool = False) -> Collection:
    name = settings.chroma_collection_name
    if reset:
        try:
            client.delete_collection(name)
        except (ValueError, NotFoundError):
            pass
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def ingest_knowledge_base(reset: bool = False) -> dict:
    """
    Load MD files → chunk → embed → store in Chroma.
    Returns summary stats for logging and reports.
    """
    documents = load_markdown_documents()
    if not documents:
        raise ValueError("No markdown documents found in knowledge base.")

    chunks: list[Chunk] = chunk_documents(documents)
    if not chunks:
        raise ValueError("Chunking produced no chunks.")

    texts = [c.text for c in chunks]
    vectors = embed_texts_batched(texts)

    client = _get_chroma_client()
    collection = _get_collection(client, reset=reset)

    ids = [f"{c.source}::{c.chunk_index}" for c in chunks]
    metadatas = [
        {"source": c.source, "chunk_index": c.chunk_index}
        for c in chunks
    ]

    # Chroma upsert in batches (avoid huge single write)
    batch_size = 100
    for i in range(0, len(ids), batch_size):
        collection.upsert(
            ids=ids[i : i + batch_size],
            documents=texts[i : i + batch_size],
            embeddings=vectors[i : i + batch_size],
            metadatas=metadatas[i : i + batch_size],
        )

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "collection": settings.chroma_collection_name,
        "persist_dir": str(settings.chroma_persist_dir),
    }


def get_indexed_collection() -> Collection:
    """Return the Chroma collection (must exist — run ingest first)."""
    client = _get_chroma_client()
    return client.get_collection(settings.chroma_collection_name)


def get_collection_stats() -> dict:
    client = _get_chroma_client()
    try:
        collection = client.get_collection(settings.chroma_collection_name)
        count = collection.count()
    except (ValueError, NotFoundError):
        count = 0
    return {
        "collection": settings.chroma_collection_name,
        "chunk_count": count,
        "persist_dir": str(settings.chroma_persist_dir),
    }
