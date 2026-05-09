"""Chunker interface."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from podagent_server.storage.models import Chunk, Transcript


@runtime_checkable
class Chunker(Protocol):
    """Protocol for transcript chunking strategies."""

    def chunk(self, transcript: Transcript) -> list[Chunk]:
        """
        Split a transcript into overlapping chunks.

        Args:
            transcript: The full transcript with segments.

        Returns:
            A list of Chunk objects with text and timestamp ranges.

        """
        ...
