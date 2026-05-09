"""Repository interfaces."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from podagent_server.storage.models import Chunk, Episode, Job


@runtime_checkable
class EpisodeRepo(Protocol):
    """Protocol for episode persistence."""

    async def create(self, episode: Episode) -> Episode:
        """Persist a new episode."""
        ...

    async def get(self, episode_id: str) -> Episode | None:
        """Fetch an episode by id."""
        ...

    async def list_all(self) -> list[Episode]:
        """List all episodes."""
        ...


@runtime_checkable
class ChunkRepo(Protocol):
    """Protocol for chunk persistence."""

    async def create_many(self, chunks: list[Chunk]) -> list[Chunk]:
        """Persist multiple chunks."""
        ...

    async def get_by_episode(self, episode_id: str) -> list[Chunk]:
        """Fetch all chunks for an episode."""
        ...


@runtime_checkable
class JobRepo(Protocol):
    """Protocol for job tracking persistence."""

    async def create(self, job: Job) -> Job:
        """Persist a new job."""
        ...

    async def get(self, job_id: str) -> Job | None:
        """Fetch a job by id."""
        ...

    async def update(self, job: Job) -> Job:
        """Update job state and progress."""
        ...
