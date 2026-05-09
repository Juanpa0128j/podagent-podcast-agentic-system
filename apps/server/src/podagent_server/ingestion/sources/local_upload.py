"""Local transcript file upload adapter."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from podagent_server.ingestion.sources.base import SourceAdapter
from podagent_server.storage.models import Transcript, TranscriptSegment


class LocalUploadAdapter(SourceAdapter):
    """Adapter for locally-uploaded transcript files (VTT/SRT/markdown)."""

    async def fetch_metadata(self, ref: str) -> dict:
        """Derive metadata from the file path and contents."""
        path = Path(ref)
        return {
            "title": path.stem,
            "description": "Uploaded transcript",
            "duration": 0,  # parsed from transcript later
            "podcast_name": "Local Upload",
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }

    async def fetch_transcript(self, ref: str) -> Transcript:
        """
        Parse a local transcript file.

        Supports VTT, SRT, and markdown with [hh:mm:ss] timestamps.
        """
        path = Path(ref)
        content = path.read_text(encoding="utf-8")

        # TODO: implement VTT/SRT/md parsers
        segments = [
            TranscriptSegment(
                start=0.0,
                end=1.0,
                text=content[:500],
                speaker=None,
            ),
        ]
        return Transcript(segments=segments)
