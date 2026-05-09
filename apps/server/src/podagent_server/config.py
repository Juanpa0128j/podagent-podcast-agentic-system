"""Runtime configuration and dependency wiring for PodAgent server."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from podagent_server.ingestion.chunking.base import Chunker
    from podagent_server.ingestion.sources.base import SourceAdapter
    from podagent_server.ingestion.transcription.base import Transcriber
    from podagent_server.retrieval.embeddings.base import Embedder
    from podagent_server.retrieval.vector_store.base import VectorStore


class Settings:
    """Server settings loaded from environment."""

    def __init__(self) -> None:
        """Load settings from environment."""
        self.database_url: str = os.environ.get(
            "DATABASE_URL",
            "postgresql+asyncpg://localhost/podagent",
        )
        self.openai_api_key: str | None = os.environ.get("OPENAI_API_KEY")
        self.azure_openai_endpoint: str | None = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_api_key: str | None = os.environ.get("AZURE_OPENAI_API_KEY")
        self.azure_openai_deployment_chat: str | None = os.environ.get(
            "AZURE_OPENAI_DEPLOYMENT_CHAT"
        )
        self.azure_openai_deployment_embeddings: str | None = os.environ.get(
            "AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS"
        )
        self.azure_openai_api_version: str = os.environ.get(
            "AZURE_OPENAI_API_VERSION",
            "2024-02-15-preview",
        )
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
    """Return the default embedder.

    Uses AzureOpenAIEmbedder when AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS is set,
    otherwise falls back to OpenAIEmbedder.
    """
    if settings.azure_openai_deployment_embeddings:
        from podagent_server.retrieval.embeddings.azure_openai_embedder import (
            AzureOpenAIEmbedder,
        )

        return AzureOpenAIEmbedder(
            azure_endpoint=settings.azure_openai_endpoint or "",
            api_key=settings.azure_openai_api_key or "",
            deployment=settings.azure_openai_deployment_embeddings,
            api_version=settings.azure_openai_api_version,
        )

    from podagent_server.retrieval.embeddings.openai_embedder import OpenAIEmbedder

    return OpenAIEmbedder(api_key=settings.openai_api_key)


def get_vector_store() -> VectorStore:
    """Return the default vector store.

    Uses InMemoryVectorStore by default.
    Set PODAGENT_VECTOR_STORE=pgvector to use PgVectorStore instead.
    """
    if os.environ.get("PODAGENT_VECTOR_STORE") == "pgvector":
        from podagent_server.retrieval.vector_store.pgvector import PgVectorStore

        return PgVectorStore(dsn=settings.database_url)

    from podagent_server.retrieval.vector_store.in_memory import InMemoryVectorStore

    return InMemoryVectorStore()


def get_azure_openai_config() -> "AzureOpenAIConfig":
    """Return Azure OpenAI config or raise if required settings are missing."""
    from podagent_server.learnflow.llm import AzureOpenAIConfig

    missing: list[str] = []
    if not settings.azure_openai_endpoint:
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not settings.azure_openai_api_key:
        missing.append("AZURE_OPENAI_API_KEY")
    if not settings.azure_openai_deployment_chat:
        missing.append("AZURE_OPENAI_DEPLOYMENT_CHAT")

    if missing:
        missing_vars = ", ".join(missing)
        raise ValueError(f"Missing required Azure OpenAI settings: {missing_vars}")

    return AzureOpenAIConfig(
        endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        deployment=settings.azure_openai_deployment_chat,
        api_version=settings.azure_openai_api_version,
    )


def get_transcriber() -> Transcriber | None:
    """Return the default transcriber, or None if not configured."""
    # STT is declared but not implemented in Phase 1.
    return None
