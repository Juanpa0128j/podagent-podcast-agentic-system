"""SourceAdapter interface."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from podagent_server.storage.models import Transcript


@runtime_checkable
class SourceAdapter(Protocol):
    """Protocol for podcast ingestion sources."""

    async def fetch_metadata(self, ref: str) -> dict:
        """
        Fetch episode metadata from the source.

        Args:
            ref: Source-specific reference (e.g. file path).

        Returns:
            A dict with keys: title, description, duration, podcast_name.

        """
        ...

    async def fetch_transcript(self, ref: str) -> Transcript:
        """
        Fetch or parse the transcript from the source.

        Args:
            ref: Source-specific reference.

        Returns:
            A Transcript model with segments.

        """
        ...
