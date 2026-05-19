from fastapi import FastAPI

from src.api.routes_chat import router as chat_router
from src.config import settings
from src.ingestion.indexer import get_collection_stats

app = FastAPI(
    title="TaskFlow Support Bot",
    description="RAG destek botu — Faz 3: kaynaklı cevap (Chroma + OpenAI)",
    version="0.3.0",
)
app.include_router(chat_router)


@app.get("/health")
def health() -> dict:
    index_stats = get_collection_stats()
    rag_ready = index_stats.get("chunk_count", 0) > 0
    return {
        "status": "ok",
        "phase": 3,
        "rag_enabled": rag_ready,
        "openai_configured": settings.api_key_configured,
        "chat_model": settings.openai_chat_model,
        "embedding_model": settings.openai_embedding_model,
        "rag_top_k": settings.rag_top_k,
        "index": index_stats,
    }