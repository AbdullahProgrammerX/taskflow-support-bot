from dataclasses import dataclass

from chromadb.errors import NotFoundError

from src.ingestion.indexer import get_collection_stats
from src.rag.generator import SourceCitation, generate_answer
from src.rag.retriever import retrieve


@dataclass
class RagAnswer:
    answer: str
    model: str
    sources: list[SourceCitation]


def is_rag_available() -> bool:
    stats = get_collection_stats()
    return stats.get("chunk_count", 0) > 0


def answer_with_rag(question: str) -> RagAnswer:
    try:
        chunks = retrieve(question)
    except NotFoundError:
        answer, model, sources = generate_answer(question, [])
        return RagAnswer(answer=answer, model=model, sources=sources)

    answer, model, sources = generate_answer(question, chunks)
    return RagAnswer(answer=answer, model=model, sources=sources)
