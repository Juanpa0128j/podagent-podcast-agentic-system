"""Chunk repository (stub)."""

from __future__ import annotations

from podagent_server.storage.models import Chunk
from podagent_server.storage.repositories import ChunkRepo


class SupabaseChunkRepo(ChunkRepo):
    """Supabase-backed chunk repository."""

    async def create_many(self, chunks: list[Chunk]) -> list[Chunk]:
        """Persist multiple chunks."""
        # TODO: implement via Supabase/postgrest
        return chunks

    async def get_by_episode(self, episode_id: str) -> list[Chunk]:
        """Fetch all chunks for an episode."""
        # TODO: implement
        return []
