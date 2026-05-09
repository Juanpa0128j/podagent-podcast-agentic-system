"""In-memory vector store with cosine similarity and JSON persistence."""

from __future__ import annotations

import json
import math
import os
import tempfile
from pathlib import Path
from typing import Any

from podagent_server.storage.models import Chunk
from podagent_server.retrieval.vector_store.base import VectorStore

DEFAULT_PERSIST_PATH = "/tmp/podagent-vectors.json"


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


class InMemoryVectorStore(VectorStore):
    """In-memory vector store backed by a JSON file for persistence."""

    def __init__(self, persist_path: str | None = None) -> None:
        """Initialize and load existing data from disk."""
        self._path = Path(
            persist_path
            or os.environ.get("PODAGENT_VECTOR_STORE_PATH", DEFAULT_PERSIST_PATH)
        )
        # records: list of dicts with keys matching Chunk fields + "embedding"
        self._records: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            try:
                data = json.loads(self._path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self._records = data
            except (json.JSONDecodeError, OSError):
                self._records = []

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=self._path.parent, prefix=".podagent-vectors-"
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(self._records, f)
            os.replace(tmp_path, self._path)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    async def upsert(self, chunks: list[Chunk]) -> None:
        """Insert or update chunks. Keyed by chunk id."""
        existing_by_id = {r["id"]: idx for idx, r in enumerate(self._records)}
        for chunk in chunks:
            record: dict[str, Any] = {
                "id": chunk.id,
                "text": chunk.text,
                "ts_start": chunk.ts_start,
                "ts_end": chunk.ts_end,
                "episode_id": chunk.episode_id,
                "embedding": chunk.embedding,
                "speaker": chunk.speaker,
            }
            if chunk.id in existing_by_id:
                self._records[existing_by_id[chunk.id]] = record
            else:
                self._records.append(record)
        self._save()

    async def search(
        self,
        query_vec: list[float],
        filters: dict[str, Any] | None,
        k: int,
    ) -> list[dict[str, Any]]:
        """Return top-k chunks by cosine similarity, applying exact-match filters."""
        candidates = self._records
        if filters:
            candidates = [
                r for r in candidates
                if all(r.get(key) == val for key, val in filters.items())
            ]

        scored = [
            (r, _cosine_similarity(query_vec, r["embedding"]))
            for r in candidates
            if r.get("embedding")
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [
            {**r, "score": score}
            for r, score in scored[:k]
        ]
