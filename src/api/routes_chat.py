from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.config import settings
from src.ingestion.indexer import get_collection_stats
from src.llm.openai_client import chat
from src.rag.pipeline import answer_with_rag, is_rag_available

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000, description="User question")


class SourceItem(BaseModel):
    file: str
    chunk_index: int
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    model: str
    rag_enabled: bool
    sources: list[SourceItem] = Field(default_factory=list)


@router.post("", response_model=ChatResponse)
def post_chat(body: ChatRequest) -> ChatResponse:
    if not settings.api_key_configured:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured. Create a .env file from .env.example.",
        )

    use_rag = is_rag_available()

    try:
        if use_rag:
            result = answer_with_rag(body.message)
            return ChatResponse(
                answer=result.answer,
                model=result.model or settings.openai_chat_model,
                rag_enabled=True,
                sources=[
                    SourceItem(
                        file=s.file,
                        chunk_index=s.chunk_index,
                        excerpt=s.excerpt,
                    )
                    for s in result.sources
                ],
            )

        answer, model = chat(body.message)
        return ChatResponse(answer=answer, model=model, rag_enabled=False)

    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"OpenAI API error: {exc}",
        ) from exc
