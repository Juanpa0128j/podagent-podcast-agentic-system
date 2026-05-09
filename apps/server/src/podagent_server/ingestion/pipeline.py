"""Ingestion pipeline: source → transcript → chunks → embed → store."""

from __future__ import annotations

import uuid

from podagent_server.config import get_chunker, get_embedder, get_source_adapter, get_vector_store
from podagent_server.storage.models import Episode


async def run_ingestion_pipeline(source: str, ref: str) -> str:
    """
    Run the full ingestion pipeline for a single episode.

    Args:
        source: Source type (e.g. "upload").
        ref: Source-specific reference.

    Returns:
        The job id for tracking progress.

    """
    job_id = str(uuid.uuid4())

    # 1. Resolve source
    adapter = get_source_adapter(source)
    metadata = await adapter.fetch_metadata(ref)
    transcript = await adapter.fetch_transcript(ref)

    # 2. Create episode record
    episode = Episode(
        id=str(uuid.uuid4()),
        title=metadata.get("title", ""),
        description=metadata.get("description", ""),
        duration=metadata.get("duration", 0),
        podcast_name=metadata.get("podcast_name", ""),
        source=source,
        source_ref=ref,
    )
    # TODO: persist via EpisodeRepo

    # 3. Chunk
    chunker = get_chunker()
    chunks = chunker.chunk(transcript)

    # 4. Embed
    embedder = get_embedder()
    texts = [c.text for c in chunks]
    vectors = await embedder.embed(texts)

    # 5. Attach vectors and persist
    for chunk, vector in zip(chunks, vectors, strict=False):
        chunk.embedding = vector
        chunk.episode_id = episode.id
    # TODO: persist chunks via ChunkRepo

    # 6. Index in vector store
    vector_store = get_vector_store()
    await vector_store.upsert(chunks)

    return job_id
