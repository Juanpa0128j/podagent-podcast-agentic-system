"""Shared test fixtures and configuration."""

from __future__ import annotations

import pytest

from podagent_server.storage.models import Transcript, TranscriptSegment


@pytest.fixture
def sample_transcript() -> Transcript:
    """Return a minimal transcript fixture."""
    return Transcript(
        segments=[
            TranscriptSegment(
                start=0.0, end=5.0, text="Hello and welcome to the show.", speaker=None
            ),
            TranscriptSegment(
                start=5.0, end=10.0, text="Today we are discussing AI.", speaker=None
            ),
        ]
    )
