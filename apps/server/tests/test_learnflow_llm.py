"""Tests for LearnFlow LLM wrappers."""

from __future__ import annotations

import pytest

from podagent_server.learnflow.llm import OutputValidationError, StructuredOutputGenerator
from podagent_server.learnflow.models import Plan


class FakeChatClient:
    """Fake chat client for structured output tests."""

    def __init__(self, responses: list[str]) -> None:
        self._responses = list(responses)
        self.calls = 0

    async def complete(self, prompt: str) -> str:
        self.calls += 1
        return self._responses.pop(0)


@pytest.mark.asyncio
async def test_structured_output_parses_valid_json() -> None:
    """Valid JSON returns a model instance."""
    payload = (
        '{"goal":"Focus","estimated_duration":"1 week","phases":[],'
        '"dos":[],"donts":[],"relevant_content":[]}'
    )
    client = FakeChatClient([payload])
    generator = StructuredOutputGenerator(client=client)

    result = await generator.generate("prompt", Plan)
    assert isinstance(result, Plan)
    assert client.calls == 1


@pytest.mark.asyncio
async def test_structured_output_retries_then_fails() -> None:
    """Invalid JSON retries then raises OutputValidationError."""
    client = FakeChatClient(["not-json", "still-not-json"])
    generator = StructuredOutputGenerator(client=client, max_retries=1)

    with pytest.raises(OutputValidationError):
        await generator.generate("prompt", Plan)
    assert client.calls == 2

