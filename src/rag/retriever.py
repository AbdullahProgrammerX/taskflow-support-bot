from dataclasses import dataclass

from src.config import settings
from src.ingestion.indexer import get_indexed_collection
from src.llm.embeddings import embed_texts


@dataclass
class RetrievedChunk:
    source: str
    chunk_index: int
    text: str
    distance: float


def retrieve(query: str, top_k: int | None = None) -> list[RetrievedChunk]:
    """Embed the query and return the most similar chunks from Chroma."""
    k = top_k or settings.rag_top_k
    collection = get_indexed_collection()

    if collection.count() == 0:
        return []

    query_vector = embed_texts([query])[0]
    result = collection.query(
        query_embeddings=[query_vector],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]

    chunks: list[RetrievedChunk] = []
    for doc, meta, dist in zip(documents, metadatas, distances, strict=True):
        if not doc or not meta:
            continue
        chunks.append(
            RetrievedChunk(
                source=str(meta.get("source", "unknown")),
                chunk_index=int(meta.get("chunk_index", 0)),
                text=doc,
                distance=float(dist),
            )
        )
    return chunks
