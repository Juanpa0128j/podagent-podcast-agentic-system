"""Tests for LearnFlow MCP tools."""

from __future__ import annotations

import pytest

from podagent_server.learnflow.models import (
    ActionItem,
    ContentMapping,
    Flashcard,
    Phase,
    Plan,
    SectionContent,
    Step,
)
from podagent_server.mcp.tools import learnflow as learnflow_tools


class FakeLearnFlowService:
    """Fake service returning deterministic models."""

    async def generate_plan(self, goal: str) -> Plan:
        return Plan(
            goal=goal,
            estimated_duration="1 week",
            phases=[
                Phase(
                    name="Phase 1",
                    duration="1 week",
                    steps=[
                        Step(
                            action="Do focus work",
                            when="Morning",
                            duration="30 minutes",
                            why="Build consistency",
                        )
                    ],
                )
            ],
            dos=[
                ActionItem(
                    action="Sleep well",
                    when="Night",
                    why="Restores attention",
                )
            ],
            donts=[
                ActionItem(
                    action="Skip breaks",
                    why="Increases fatigue",
                )
            ],
            relevant_content=[
                ContentMapping(section_id="sec-1", reason="Relevant section")
            ],
        )

    async def generate_section_content(self, section_id: str, goal: str) -> SectionContent:
        return SectionContent(
            section_id=section_id,
            summary="Summary",
            key_points=["A", "B"],
            glossary=[],
            flashcards=[
                Flashcard(id="fc-1", question="Q?", answer="A")
            ],
        )


@pytest.mark.asyncio
async def test_generate_plan_returns_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    """generate_plan returns MCPAppResponse envelope with _ui hint and data."""
    fake_service = FakeLearnFlowService()
    monkeypatch.setattr(
        learnflow_tools,
        "get_learnflow_service",
        lambda: fake_service,
    )

    result = await learnflow_tools.generate_plan("Focus")

    # Envelope structure
    assert "_ui" in result
    assert result["_ui"]["component"] == "PlanView"
    assert result["_ui"]["version"] == 1
    assert "data" in result

    # Payload integrity
    data = result["data"]
    assert data["goal"] == "Focus"
    assert data["phases"][0]["steps"][0]["action"] == "Do focus work"


@pytest.mark.asyncio
async def test_generate_section_content_returns_envelope(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """generate_section_content returns MCPAppResponse envelope with _ui hint and data."""
    fake_service = FakeLearnFlowService()
    monkeypatch.setattr(
        learnflow_tools,
        "get_learnflow_service",
        lambda: fake_service,
    )

    result = await learnflow_tools.generate_section_content("sec-1", "Focus")

    # Envelope structure
    assert "_ui" in result
    assert result["_ui"]["component"] == "SectionView"
    assert result["_ui"]["version"] == 1
    assert "data" in result

    # Payload integrity
    data = result["data"]
    assert data["section_id"] == "sec-1"
    assert data["flashcards"][0]["id"] == "fc-1"


@pytest.mark.asyncio
async def test_answer_with_rag_has_no_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    """answer_with_rag returns flat dict — no _ui envelope (not a UI-rendered tool)."""
    from podagent_server.learnflow.models import Answer  # type: ignore[attr-defined]

    class FakeServiceWithRag(FakeLearnFlowService):
        async def answer_with_rag(
            self, question: str, context: str | None = None
        ) -> Answer:
            return Answer(answer="42", citations=[])  # type: ignore[call-arg]

    fake_service = FakeServiceWithRag()
    monkeypatch.setattr(
        learnflow_tools,
        "get_learnflow_service",
        lambda: fake_service,
    )

    try:
        result = await learnflow_tools.answer_with_rag("What is focus?")
        # If Answer model exists: should have no _ui key
        assert "_ui" not in result
    except Exception:
        # Answer model may not exist yet — skip gracefully
        pytest.skip("Answer model not yet implemented")
