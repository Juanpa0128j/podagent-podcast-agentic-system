"""UI resource hint generators.

These produce `_ui` keys on tool responses that compatible hosts
(Claude Desktop, web client) can render as rich widgets.
Programmatic consumers can safely ignore them.
"""

from __future__ import annotations

from typing import Any


def citation_card(chunk: dict[str, Any], score: float) -> dict[str, Any]:
    """Generate a citation card UI hint."""
    return {
        "type": "citation_card",
        "episode_title": chunk.get("episode_title", "Unknown"),
        "podcast_name": chunk.get("podcast_name", "Unknown"),
        "ts_start": chunk.get("ts_start", 0),
        "ts_end": chunk.get("ts_end", 0),
        "excerpt": chunk.get("text", "")[:200],
        "score": score,
    }


def import_progress(job_id: str, state: str, progress: float) -> dict[str, Any]:
    """Generate an import progress UI hint."""
    return {
        "type": "import_progress",
        "job_id": job_id,
        "state": state,
        "progress": progress,
    }
