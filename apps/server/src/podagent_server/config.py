"""Runtime configuration and dependency wiring for PodAgent server."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from podagent_server.ingestion.sources.base import SourceAdapter
    from podagent_server.ingestion.chunking.base import Chunker
    from podagent_server.ingestion.transcription.base import Transcriber
    from podagent_server.retrieval.embeddings.base import Embedder
    from podagent_server.retrieval.vector_store.base import VectorStore


class Settings:
    """Server settings loaded from environment."""

    def __init__(self) -> None:
        self.database_url: str = os.environ.get(
            "DATABASE_URL",
            "postgresql+asyncpg://localhost/podagent",
        )
        self.openai_api_key: str | None = os.environ.get("OPENAI_API_KEY")
        self.supabase_jwt_secret: str | None = os.environ.get("SUPABASE_JWT_SECRET")
        self.environment: str = os.environ.get("ENVIRONMENT", "development")


# Global settings singleton
settings = Settings()


def get_source_adapter(source_type: str) -> SourceAdapter:
    """Return a concrete SourceAdapter for the given source type."""
    from podagent_server.ingestion.sources.local_upload import LocalUploadAdapter

    if source_type == "upload":
        return LocalUploadAdapter()
    raise ValueError(f"Unknown source type: {source_type}")


def get_chunker() -> Chunker:
    """Return the default chunker."""
    from podagent_server.ingestion.chunking.token_window import TokenWindowChunker

    return TokenWindowChunker()


def get_embedder() -> Embedder:
    """Return the default embedder."""
    from podagent_server.retrieval.embeddings.openai_embedder import OpenAIEmbedder

    return OpenAIEmbedder(api_key=settings.openai_api_key)


def get_vector_store() -> VectorStore:
    """Return the default vector store."""
    from podagent_server.retrieval.vector_store.pgvector import PgVectorStore

    return PgVectorStore(dsn=settings.database_url)


def get_transcriber() -> Transcriber | None:
    """Return the default transcriber, or None if not configured."""
    # STT is declared but not implemented in Phase 1.
    return None
