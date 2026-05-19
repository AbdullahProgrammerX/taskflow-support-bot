from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    knowledge_base_dir: Path = PROJECT_ROOT / "data" / "knowledge_base"
    chroma_persist_dir: Path = PROJECT_ROOT / "chroma_data"
    chroma_collection_name: str = "taskflow_support"

    chunk_size: int = 800
    chunk_overlap: int = 100
    embedding_batch_size: int = 64
    rag_top_k: int = 4
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def api_key_configured(self) -> bool:
        return bool(self.openai_api_key.strip())


settings = Settings()
