"""MCP library tools."""

from __future__ import annotations

from typing import Any


async def list_library() -> list[dict[str, Any]]:
    """List all imported episodes in the user's library.

    Returns:
        A list of episode metadata dicts.
    """
    # TODO: implement via EpisodeRepo
    return []


async def get_episode(episode_id: str) -> dict[str, Any]:
    """Get metadata for a single episode.

    Args:
        episode_id: The episode UUID.

    Returns:
        Episode metadata and transcript URL.
    """
    # TODO: implement via EpisodeRepo
    return {
        "id": episode_id,
        "title": "",
        "description": "",
        "duration": 0,
        "podcast_name": "",
        "transcript_url": None,
    }


async def get_transcript_window(
    episode_id: str,
    start_ts: float,
    end_ts: float,
) -> list[dict[str, Any]]:
    """Get transcript chunks within a timestamp window.

    Args:
        episode_id: The episode UUID.
        start_ts: Start timestamp in seconds.
        end_ts: End timestamp in seconds.

    Returns:
        A list of chunk dicts with text and timestamps.
    """
    # TODO: implement via ChunkRepo
    return []
