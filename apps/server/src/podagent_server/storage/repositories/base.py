"""Base repository interface (re-export for convenience)."""

from podagent_server.storage.repositories import ChunkRepo, EpisodeRepo, JobRepo

__all__ = ["ChunkRepo", "EpisodeRepo", "JobRepo"]
