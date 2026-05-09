"""Azure OpenAI embedding provider."""

from __future__ import annotations

import openai

from podagent_server.retrieval.embeddings.base import Embedder


class AzureOpenAIEmbedder(Embedder):
    """Azure OpenAI embedder using AsyncAzureOpenAI client."""

    def __init__(
        self,
        azure_endpoint: str,
        api_key: str,
        deployment: str,
        api_version: str = "2024-02-15-preview",
    ) -> None:
        """Initialize Azure OpenAI embedder."""
        self._azure_endpoint = azure_endpoint
        self._api_key = api_key
        self._deployment = deployment
        self._api_version = api_version
        self._client: openai.AsyncAzureOpenAI | None = None

    def _get_client(self) -> openai.AsyncAzureOpenAI:
        if self._client is None:
            self._client = openai.AsyncAzureOpenAI(
                azure_endpoint=self._azure_endpoint,
                api_key=self._api_key,
                api_version=self._api_version,
            )
        return self._client

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts via Azure OpenAI API."""
        client = self._get_client()
        response = await client.embeddings.create(
            model=self._deployment,
            input=texts,
        )
        return [item.embedding for item in response.data]
