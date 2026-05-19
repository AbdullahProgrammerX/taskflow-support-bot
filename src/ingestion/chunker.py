from dataclasses import dataclass

from src.config import settings
from src.ingestion.loader import Document


@dataclass
class Chunk:
    source: str
    chunk_index: int
    text: str


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping character windows."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = end - overlap
    return [c for c in chunks if c]


def chunk_documents(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    size = chunk_size or settings.chunk_size
    ov = overlap or settings.chunk_overlap
    all_chunks: list[Chunk] = []
    for doc in documents:
        parts = chunk_text(doc.content, size, ov)
        for index, part in enumerate(parts):
            all_chunks.append(
                Chunk(source=doc.source, chunk_index=index, text=part)
            )
    return all_chunks
