"""MCP ingestion tools."""

from __future__ import annotations

from typing import Any

from podagent_server.ingestion.pipeline import run_ingestion_pipeline


async def import_episode(source: str, ref: str) -> dict[str, Any]:
    """Import an episode from a source.

    Args:
        source: The source type (e.g. "upload").
        ref: Source-specific reference (file path or upload id).

    Returns:
        A dict with the job_id for tracking progress.
    """
    job_id = await run_ingestion_pipeline(source=source, ref=ref)
    return {"job_id": job_id}


async def get_import_status(job_id: str) -> dict[str, Any]:
    """Get the status of an import job.

    Args:
        job_id: The job identifier returned by import_episode.

    Returns:
        A dict with state, progress, episode_id, error, and optional _ui hint.
    """
    # TODO: implement via JobRepo
    return {
        "state": "pending",
        "progress": 0.0,
        "episode_id": None,
        "error": None,
    }
