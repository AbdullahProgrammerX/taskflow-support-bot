from dataclasses import dataclass

from src.config import settings
from src.llm.openai_client import chat_messages
from src.rag.retriever import RetrievedChunk

RAG_SYSTEM_PROMPT = """You are the official support assistant for TaskFlow (project management SaaS).

Rules:
1. Answer ONLY using the context blocks below. Do not use outside knowledge.
2. If the context does not contain enough information, say clearly that you do not know \
and suggest contacting support@taskflow.io.
3. Reply in the same language as the user's question.
4. Be concise and factual. Do not invent prices, limits, or features.
5. When stating numbers or plan limits, they must match the context exactly."""


@dataclass
class SourceCitation:
    file: str
    chunk_index: int
    excerpt: str


def _build_context_block(chunks: list[RetrievedChunk]) -> str:
    parts: list[str] = []
    for i, chunk in enumerate(chunks, start=1):
        parts.append(
            f"--- Context {i} ({chunk.source}, part {chunk.chunk_index}) ---\n"
            f"{chunk.text}"
        )
    return "\n\n".join(parts)


def _build_user_prompt(question: str, context: str) -> str:
    return f"""Use the following documentation context to answer the question.

{context}

---
Question: {question}"""


def chunks_to_sources(chunks: list[RetrievedChunk], excerpt_len: int = 200) -> list[SourceCitation]:
    seen: set[tuple[str, int]] = set()
    sources: list[SourceCitation] = []
    for chunk in chunks:
        key = (chunk.source, chunk.chunk_index)
        if key in seen:
            continue
        seen.add(key)
        excerpt = chunk.text[:excerpt_len]
        if len(chunk.text) > excerpt_len:
            excerpt += "..."
        sources.append(
            SourceCitation(
                file=chunk.source,
                chunk_index=chunk.chunk_index,
                excerpt=excerpt,
            )
        )
    return sources


def generate_answer(question: str, chunks: list[RetrievedChunk]) -> tuple[str, str, list[SourceCitation]]:
    """Build RAG prompt and return (answer, model, sources)."""
    if not chunks:
        answer = (
            "Bu konuda dokümantasyonumuzda bilgi bulamadım. "
            "Lütfen support@taskflow.io adresine yazın."
        )
        return answer, settings.openai_chat_model, []

    context = _build_context_block(chunks)
    user_prompt = _build_user_prompt(question, context)
    messages = [
        {"role": "system", "content": RAG_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    answer, model = chat_messages(messages)
    sources = chunks_to_sources(chunks)
    return answer, model, sources
