from openai import OpenAI

from src.config import settings
from src.llm.openai_client import get_client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Convert texts to embedding vectors via OpenAI."""
    if not texts:
        return []
    client: OpenAI = get_client()
    response = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]


def embed_texts_batched(texts: list[str]) -> list[list[float]]:
    """Embed large lists in batches to respect API limits."""
    batch_size = settings.embedding_batch_size
    all_vectors: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        all_vectors.extend(embed_texts(batch))
    return all_vectors
