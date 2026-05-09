"""Token-window chunker."""

from __future__ import annotations

from podagent_server.ingestion.chunking.base import Chunker
from podagent_server.storage.models import Chunk, Transcript


class TokenWindowChunker(Chunker):
    """Chunk transcript into fixed token windows with overlap.

    Phase 1 uses a naive word-count approximation.
    """

    def __init__(self, window_size: int = 750, overlap: int = 100) -> None:
        self.window_size = window_size
        self.overlap = overlap

    def chunk(self, transcript: Transcript) -> list[Chunk]:
        """Split transcript into chunks."""
        chunks: list[Chunk] = []
        words: list[tuple[float, float, str]] = []

        for seg in transcript.segments:
            for word in seg.text.split():
                words.append((seg.start, seg.end, word))

        if not words:
            return chunks

        step = self.window_size - self.overlap
        i = 0
        chunk_id = 0
        while i < len(words):
            window = words[i : i + self.window_size]
            text = " ".join(w[2] for w in window)
            ts_start = window[0][0]
            ts_end = window[-1][1]
            chunks.append(
                Chunk(
                    id=chunk_id,
                    text=text,
                    ts_start=ts_start,
                    ts_end=ts_end,
                    episode_id="",  # filled in by pipeline
                    embedding=None,
                )
            )
            i += step
            chunk_id += 1

        return chunks
