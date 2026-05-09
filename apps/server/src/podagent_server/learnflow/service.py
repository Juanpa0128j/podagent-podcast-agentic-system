"""LearnFlow service layer for plan and content generation."""

from __future__ import annotations

from typing import Any

from podagent_server.config import get_azure_openai_config, get_embedder, get_vector_store
from podagent_server.learnflow.llm import AzureOpenAIChatClient, StructuredOutputGenerator
from podagent_server.learnflow.models import Answer, Plan, SectionContent
from podagent_server.learnflow.prompts import (
    build_answer_prompt,
    build_plan_prompt,
    build_section_prompt,
)
from podagent_server.retrieval.embeddings.base import Embedder
from podagent_server.retrieval.vector_store.base import VectorStore


class LearnFlowService:
    """Service for LearnFlow generation tasks."""

    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore,
        generator: StructuredOutputGenerator,
        k: int = 8,
    ) -> None:
        self._embedder = embedder
        self._vector_store = vector_store
        self._generator = generator
        self._k = k

    async def generate_plan(self, goal: str) -> Plan:
        """Generate a structured plan from a goal."""
        chunks = await self._retrieve_chunks(query=goal, filters=None)
        prompt = build_plan_prompt(goal=goal, retrieved_chunks=chunks)
        return await self._generator.generate(prompt, Plan)

    async def generate_section_content(self, section_id: str, goal: str) -> SectionContent:
        """Generate structured section content by section id."""
        chunks = await self._retrieve_chunks(
            query=goal,
            filters={"section_id": section_id},
        )
        transcript = "\n".join(chunk.get("text", "") for chunk in chunks)
        prompt = build_section_prompt(goal=goal, transcript=transcript)
        result = await self._generator.generate(prompt, SectionContent)
        return result.model_copy(update={"section_id": section_id})

    async def answer_with_rag(self, question: str, context: str | None) -> Answer:
        """Answer a question using retrieved chunks."""
        chunks = await self._retrieve_chunks(query=question, filters=None)
        prompt = build_answer_prompt(
            question=question,
            context=context,
            retrieved_chunks=chunks,
        )
        return await self._generator.generate(prompt, Answer)

    async def _retrieve_chunks(
        self,
        query: str,
        filters: dict[str, Any] | None,
    ) -> list[dict[str, Any]]:
        query_vec = await self._embedder.embed([query])
        return await self._vector_store.search(
            query_vec=query_vec[0],
            filters=filters,
            k=self._k,
        )


def get_learnflow_service() -> LearnFlowService:
    """Build a LearnFlowService instance using configured dependencies."""
    config = get_azure_openai_config()
    client = AzureOpenAIChatClient(config)
    generator = StructuredOutputGenerator(client=client)
    return LearnFlowService(
        embedder=get_embedder(),
        vector_store=get_vector_store(),
        generator=generator,
    )
