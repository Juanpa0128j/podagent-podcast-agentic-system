"""Episode repository (stub)."""

from __future__ import annotations

from podagent_server.storage.models import Episode
from podagent_server.storage.repositories import EpisodeRepo


class SupabaseEpisodeRepo(EpisodeRepo):
    """Supabase-backed episode repository."""

    async def create(self, episode: Episode) -> Episode:
        """Persist a new episode."""
        # TODO: implement via Supabase/postgrest
        return episode

    async def get(self, episode_id: str) -> Episode | None:
        """Fetch an episode by id."""
        # TODO: implement
        return None

    async def list_all(self) -> list[Episode]:
        """List all episodes."""
        # TODO: implement
        return []
