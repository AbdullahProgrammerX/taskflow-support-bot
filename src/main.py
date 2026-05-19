from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.routes_admin import router as admin_router
from src.api.routes_chat import router as chat_router
from src.config import settings
from src.ingestion.indexer import get_collection_stats
from src.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(
    title="TaskFlow Support Bot",
    description="RAG destek botu — Faz 4: rate limit ve admin reindex",
    version="0.4.0",
)

app.add_middleware(RateLimitMiddleware)
app.include_router(chat_router)
app.include_router(admin_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.get("/health")
def health() -> dict:
    index_stats = get_collection_stats()
    rag_ready = index_stats.get("chunk_count", 0) > 0
    return {
        "status": "ok",
        "phase": 4,
        "rag_enabled": rag_ready,
        "openai_configured": settings.api_key_configured,
        "admin_configured": settings.admin_api_key_configured,
        "chat_model": settings.openai_chat_model,
        "embedding_model": settings.openai_embedding_model,
        "rag_top_k": settings.rag_top_k,
        "rate_limit": {
            "requests": settings.rate_limit_requests,
            "window_seconds": settings.rate_limit_window_seconds,
        },
        "index": index_stats,
    }
