"""OpenAI embedding provider."""

from __future__ import annotations

import os

import openai

from podagent_server.retrieval.embeddings.base import Embedder


class OpenAIEmbedder(Embedder):
    """OpenAI text-embedding-3-small embedder."""

    def __init__(self, api_key: str | None = None, model: str = "text-embedding-3-small") -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self._client: openai.AsyncOpenAI | None = None

    def _get_client(self) -> openai.AsyncOpenAI:
        if self._client is None:
            self._client = openai.AsyncOpenAI(api_key=self.api_key)
        return self._client

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts via OpenAI API."""
        client = self._get_client()
        response = await client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]
