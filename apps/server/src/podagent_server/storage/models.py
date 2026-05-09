"""Storage models — Pydantic + SQLAlchemy definitions."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TranscriptSegment(BaseModel):
    """A single segment of a transcript with timestamps."""

    start: float = Field(..., description="Start timestamp in seconds")
    end: float = Field(..., description="End timestamp in seconds")
    text: str = Field(..., description="Transcribed text")
    speaker: str | None = Field(None, description="Speaker label if available")


class Transcript(BaseModel):
    """Full transcript composed of segments."""

    segments: list[TranscriptSegment] = Field(default_factory=list)


class Episode(BaseModel):
    """Podcast episode metadata."""

    id: str
    title: str
    description: str = ""
    duration: int = 0
    podcast_name: str = ""
    source: str = ""  # e.g. "upload"
    source_ref: str = ""  # file path or external id
    status: str = "pending"  # pending | processing | ready | failed


class Chunk(BaseModel):
    """A searchable chunk of transcript text."""

    id: int
    text: str
    ts_start: float
    ts_end: float
    episode_id: str
    embedding: list[float] | None = None
    speaker: str | None = None


class Job(BaseModel):
    """Ingestion job tracking."""

    id: str
    type: str = "ingestion"
    state: str = "pending"  # pending | processing | ready | failed
    progress: float = 0.0
    episode_id: str | None = None
    error: str | None = None
