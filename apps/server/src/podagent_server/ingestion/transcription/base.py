"""
Transcriber interface.

STT providers implement this interface. Phase 1 does not include STT;
transcripts are uploaded directly. This interface is declared for Phase 2.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from podagent_server.storage.models import Transcript


@runtime_checkable
class Transcriber(Protocol):
    """Protocol for speech-to-text providers."""

    async def transcribe(self, audio_path: str) -> Transcript:
        """
        Transcribe an audio file to a timestamped transcript.

        Args:
            audio_path: Path to the local audio file.

        Returns:
            A Transcript with segments and optional speaker labels.

        """
        ...
