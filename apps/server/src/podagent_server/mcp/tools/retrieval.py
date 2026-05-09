"""MCP retrieval tools."""

from __future__ import annotations

from typing import Any

from podagent_server.config import get_embedder, get_vector_store


async def search_chunks(
    query: str,
    scope: dict[str, Any],
    k: int = 8,
    filters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Search for relevant transcript chunks.

    Args:
        query: The natural language query.
        scope: Search universe — {"type": "episode"|"podcast"|"library", "id": ...}.
        k: Number of results to return.
        filters: Optional metadata filters.

    Returns:
        A list of ranked chunks with episode metadata and timestamps.
    """
    embedder = get_embedder()
    vector_store = get_vector_store()

    query_vec = await embedder.embed([query])
    results = await vector_store.search(
        query_vec=query_vec[0],
        filters=filters,
        k=k,
    )

    # TODO: apply scope filtering (episode / podcast / library)
    return results
