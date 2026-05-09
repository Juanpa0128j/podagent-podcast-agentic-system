"""Tests for InMemoryVectorStore."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from podagent_server.retrieval.vector_store.in_memory import InMemoryVectorStore
from podagent_server.storage.models import Chunk


def _make_chunk(
    id: int,
    text: str,
    embedding: list[float],
    episode_id: str = "ep1",
    speaker: str | None = None,
) -> Chunk:
    return Chunk(
        id=id,
        text=text,
        ts_start=0.0,
        ts_end=1.0,
        episode_id=episode_id,
        embedding=embedding,
        speaker=speaker,
    )


def _normalize(v: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in v))
    return [x / norm for x in v]


@pytest.mark.asyncio
async def test_upsert_and_search_nearest(tmp_path: Path) -> None:
    store = InMemoryVectorStore(persist_path=str(tmp_path / "vecs.json"))

    # Two orthogonal unit vectors
    v1 = _normalize([1.0, 0.0, 0.0])
    v2 = _normalize([0.0, 1.0, 0.0])

    chunks = [
        _make_chunk(1, "chunk one", v1),
        _make_chunk(2, "chunk two", v2),
    ]
    await store.upsert(chunks)

    # Query close to v1
    results = await store.search(query_vec=v1, filters=None, k=2)
    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[0]["score"] == pytest.approx(1.0, abs=1e-6)
    assert results[1]["id"] == 2


@pytest.mark.asyncio
async def test_search_filter_exact_match(tmp_path: Path) -> None:
    store = InMemoryVectorStore(persist_path=str(tmp_path / "vecs.json"))

    v = _normalize([1.0, 0.0])
    chunks = [
        _make_chunk(1, "ep1 chunk", v, episode_id="ep1"),
        _make_chunk(2, "ep2 chunk", v, episode_id="ep2"),
    ]
    await store.upsert(chunks)

    results = await store.search(query_vec=v, filters={"episode_id": "ep1"}, k=10)
    assert len(results) == 1
    assert results[0]["id"] == 1


@pytest.mark.asyncio
async def test_persistence_round_trip(tmp_path: Path) -> None:
    path = str(tmp_path / "vecs.json")
    store1 = InMemoryVectorStore(persist_path=path)

    v = _normalize([1.0, 1.0])
    await store1.upsert([_make_chunk(42, "persisted", v)])

    # New store instance loads from disk
    store2 = InMemoryVectorStore(persist_path=path)
    results = await store2.search(query_vec=v, filters=None, k=5)
    assert len(results) == 1
    assert results[0]["id"] == 42
    assert results[0]["text"] == "persisted"


@pytest.mark.asyncio
async def test_upsert_updates_existing(tmp_path: Path) -> None:
    store = InMemoryVectorStore(persist_path=str(tmp_path / "vecs.json"))

    v = _normalize([1.0, 0.0])
    await store.upsert([_make_chunk(1, "original", v)])
    await store.upsert([_make_chunk(1, "updated", v)])

    results = await store.search(query_vec=v, filters=None, k=5)
    assert len(results) == 1
    assert results[0]["text"] == "updated"


@pytest.mark.asyncio
async def test_persistence_file_is_valid_json(tmp_path: Path) -> None:
    path = tmp_path / "vecs.json"
    store = InMemoryVectorStore(persist_path=str(path))

    v = _normalize([0.5, 0.5])
    await store.upsert([_make_chunk(7, "hello", v)])

    data = json.loads(path.read_text())
    assert isinstance(data, list)
    assert data[0]["id"] == 7
