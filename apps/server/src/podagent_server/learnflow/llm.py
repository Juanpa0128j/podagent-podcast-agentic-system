"""LLM wrappers for structured LearnFlow outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeVar

import openai
from pydantic import BaseModel, ValidationError

ModelT = TypeVar("ModelT", bound=BaseModel)


class ChatClient(Protocol):
    """Minimal chat client protocol."""

    async def complete(self, prompt: str) -> str: ...


class OutputValidationError(RuntimeError):
    """Raised when structured output cannot be validated."""


@dataclass(frozen=True)
class AzureOpenAIConfig:
    """Azure OpenAI chat configuration."""

    endpoint: str
    api_key: str
    deployment: str
    api_version: str = "2024-02-15-preview"
    temperature: float = 0.2


class AzureOpenAIChatClient:
    """Azure OpenAI chat client wrapper."""

    def __init__(self, config: AzureOpenAIConfig) -> None:
        self._config = config
        self._client: openai.AsyncAzureOpenAI | None = None

    def _get_client(self) -> openai.AsyncAzureOpenAI:
        if self._client is None:
            self._client = openai.AsyncAzureOpenAI(
                api_key=self._config.api_key,
                azure_endpoint=self._config.endpoint,
                api_version=self._config.api_version,
            )
        return self._client

    async def complete(self, prompt: str) -> str:
        client = self._get_client()
        response = await client.chat.completions.create(
            model=self._config.deployment,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return ONLY a single valid JSON object. "
                        "Do NOT wrap in markdown code fences. "
                        "Do NOT add any prose before or after."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=self._config.temperature,
        )
        message = response.choices[0].message if response.choices else None
        content = message.content if message else None
        if not content:
            raise OutputValidationError("Empty response from Azure OpenAI")
        return content


class StructuredOutputGenerator:
    """Generate and validate structured output with retries."""

    def __init__(self, client: ChatClient, max_retries: int = 1) -> None:
        self._client = client
        self._max_retries = max_retries

    async def generate(self, prompt: str, model_type: type[ModelT]) -> ModelT:
        last_error: Exception | None = None
        for _ in range(self._max_retries + 1):
            response = await self._client.complete(prompt)
            cleaned = _strip_code_fence(response)
            try:
                return model_type.model_validate_json(cleaned)
            except (ValidationError, ValueError) as exc:
                last_error = exc

        raise OutputValidationError("Invalid JSON response") from last_error


def _strip_code_fence(text: str) -> str:
    """Strip leading/trailing markdown code fences from an LLM response."""
    stripped = text.strip()
    if stripped.startswith("```"):
        first_newline = stripped.find("\n")
        if first_newline != -1:
            stripped = stripped[first_newline + 1 :]
        if stripped.endswith("```"):
            stripped = stripped[: -len("```")]
    return stripped.strip()
