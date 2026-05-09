"""MCP tools for LearnFlow generation."""

from __future__ import annotations

from typing import Any

from podagent_server.learnflow.service import get_learnflow_service


def _ui_envelope(component: str, version: int, data: dict[str, Any]) -> dict[str, Any]:
    """Wrap tool output in an MCP Apps envelope with a _ui hint."""
    return {
        "_ui": {"component": component, "version": version},
        "data": data,
    }


async def generate_plan(goal: str) -> dict[str, Any]:
    """Generate a structured learning plan."""
    service = get_learnflow_service()
    plan = await service.generate_plan(goal)
    return _ui_envelope("PlanView", 1, plan.model_dump(exclude_none=True))


async def generate_section_content(section_id: str, goal: str) -> dict[str, Any]:
    """Generate structured content for a specific section."""
    service = get_learnflow_service()
    content = await service.generate_section_content(section_id=section_id, goal=goal)
    return _ui_envelope("SectionView", 1, content.model_dump(exclude_none=True))


async def answer_with_rag(question: str, context: str | None = None) -> dict[str, Any]:
    """Answer a question using RAG."""
    service = get_learnflow_service()
    answer = await service.answer_with_rag(question=question, context=context)
    return answer.model_dump(exclude_none=True)
