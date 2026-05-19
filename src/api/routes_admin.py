from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.api.deps import verify_admin_key
from src.config import settings
from src.ingestion.indexer import get_collection_stats, ingest_knowledge_base

router = APIRouter(prefix="/admin", tags=["admin"])


class ReindexRequest(BaseModel):
    reset: bool = Field(
        default=True,
        description="If true, delete and recreate the Chroma collection before ingest",
    )


class ReindexResponse(BaseModel):
    status: str
    documents: int
    chunks: int
    collection: str
    chunk_count: int


@router.post("/reindex", response_model=ReindexResponse, dependencies=[Depends(verify_admin_key)])
def reindex(body: ReindexRequest) -> ReindexResponse:
    if not settings.api_key_configured:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is required for embedding during reindex.",
        )
    try:
        stats = ingest_knowledge_base(reset=body.reset)
        after = get_collection_stats()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Reindex failed: {exc}") from exc

    return ReindexResponse(
        status="ok",
        documents=stats["documents"],
        chunks=stats["chunks"],
        collection=stats["collection"],
        chunk_count=after["chunk_count"],
    )


@router.get("/index-stats", dependencies=[Depends(verify_admin_key)])
def index_stats() -> dict:
    return get_collection_stats()
