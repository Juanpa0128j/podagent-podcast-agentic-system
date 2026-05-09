"""Embedder interface."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Embedder(Protocol):
    """Protocol for text embedding providers."""

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Embed a batch of texts into vectors.

        Args:
            texts: List of raw text strings.

        Returns:
            A list of embedding vectors (one per input text).

        """
        ...
