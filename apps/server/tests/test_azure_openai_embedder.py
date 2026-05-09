"""Unit tests for AzureOpenAIEmbedder — mocked client, no live API."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from podagent_server.retrieval.embeddings.azure_openai_embedder import AzureOpenAIEmbedder


def _make_embedder() -> AzureOpenAIEmbedder:
    return AzureOpenAIEmbedder(
        azure_endpoint="https://my-resource.openai.azure.com",
        api_key="fake-key",
        deployment="text-embedding-ada-002",
        api_version="2024-02-15-preview",
    )


@pytest.mark.asyncio
async def test_embed_returns_vectors() -> None:
    embedder = _make_embedder()

    fake_embedding = [0.1, 0.2, 0.3]
    mock_item = MagicMock()
    mock_item.embedding = fake_embedding
    mock_response = MagicMock()
    mock_response.data = [mock_item]

    mock_client = MagicMock()
    mock_client.embeddings.create = AsyncMock(return_value=mock_response)

    with patch("openai.AsyncAzureOpenAI", return_value=mock_client):
        # Force new client creation
        embedder._client = None
        embedder._client = mock_client

        result = await embedder.embed(["hello world"])

    assert result == [fake_embedding]
    mock_client.embeddings.create.assert_called_once_with(
        model="text-embedding-ada-002",
        input=["hello world"],
    )


@pytest.mark.asyncio
async def test_embed_batch_multiple_texts() -> None:
    embedder = _make_embedder()

    vecs = [[0.1, 0.2], [0.3, 0.4]]
    items = [MagicMock(embedding=v) for v in vecs]
    mock_response = MagicMock(data=items)

    mock_client = MagicMock()
    mock_client.embeddings.create = AsyncMock(return_value=mock_response)
    embedder._client = mock_client

    result = await embedder.embed(["text one", "text two"])

    assert result == vecs
    mock_client.embeddings.create.assert_called_once_with(
        model="text-embedding-ada-002",
        input=["text one", "text two"],
    )
