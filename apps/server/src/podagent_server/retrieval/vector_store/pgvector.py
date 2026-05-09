"""pgvector vector store implementation."""

from __future__ import annotations

from typing import Any

from podagent_server.retrieval.vector_store.base import VectorStore
from podagent_server.storage.models import Chunk


class PgVectorStore(VectorStore):
    """PostgreSQL pgvector-backed vector store.

    Assumes a table `chunks` with a `vector(1536)` column.
    """

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    async def upsert(self, chunks: list[Chunk]) -> None:
        """Insert or update chunks with embeddings."""
        # TODO: implement asyncpg batch insert
        pass

    async def search(
        self,
        query_vec: list[float],
        filters: dict[str, Any] | None,
        k: int,
    ) -> list[dict[str, Any]]:
        """Search for similar chunks via cosine similarity."""
        # TODO: implement asyncpg query with ivfflat index
        return []
