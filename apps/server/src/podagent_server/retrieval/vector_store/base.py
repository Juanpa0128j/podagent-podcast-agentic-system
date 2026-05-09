"""VectorStore interface."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from podagent_server.storage.models import Chunk


@runtime_checkable
class VectorStore(Protocol):
    """Protocol for vector databases."""

    async def upsert(self, chunks: list[Chunk]) -> None:
        """
        Insert or update chunks with embeddings.

        Args:
            chunks: List of Chunk models with embeddings populated.

        """
        ...

    async def search(
        self,
        query_vec: list[float],
        filters: dict[str, Any] | None,
        k: int,
    ) -> list[dict[str, Any]]:
        """
        Search for similar chunks.

        Args:
            query_vec: The query embedding vector.
            filters: Optional metadata filters.
            k: Number of results to return.

        Returns:
            A list of result dicts with chunk data and similarity scores.

        """
        ...
