"""Search orchestration."""

from __future__ import annotations

from typing import Any

from podagent_server.retrieval.embeddings.base import Embedder
from podagent_server.retrieval.vector_store.base import VectorStore


async def hybrid_search(
    query: str,
    embedder: Embedder,
    vector_store: VectorStore,
    filters: dict[str, Any] | None = None,
    k: int = 8,
) -> list[dict[str, Any]]:
    """Run a vector + metadata hybrid search.

    Args:
        query: Natural language query.
        embedder: Embedding provider.
        vector_store: Vector database.
        filters: Optional metadata filters.
        k: Number of results.

    Returns:
        Ranked chunks with metadata.
    """
    vectors = await embedder.embed([query])
    results = await vector_store.search(
        query_vec=vectors[0],
        filters=filters,
        k=k,
    )
    return results
