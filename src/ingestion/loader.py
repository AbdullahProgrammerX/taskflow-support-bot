from dataclasses import dataclass
from pathlib import Path

from src.config import settings


@dataclass
class Document:
    source: str
    content: str


def load_markdown_documents(base_dir: Path | None = None) -> list[Document]:
    """Read all .md files from the knowledge base directory."""
    root = base_dir or settings.knowledge_base_dir
    if not root.is_dir():
        raise FileNotFoundError(f"Knowledge base directory not found: {root}")

    documents: list[Document] = []
    for path in sorted(root.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        documents.append(Document(source=path.name, content=text))
    return documents
