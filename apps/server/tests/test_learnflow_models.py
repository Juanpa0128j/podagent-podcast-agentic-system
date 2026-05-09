"""Tests for LearnFlow data models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from podagent_server.learnflow.models import (
    ActionItem,
    ContentMapping,
    Flashcard,
    Phase,
    Plan,
    SectionContent,
    Step,
)


def test_plan_serializes_to_expected_shape() -> None:
    """Plan serializes to expected JSON shape."""
    plan = Plan(
        goal="Improve focus",
        estimated_duration="4 weeks",
        phases=[
            Phase(
                name="Phase 1",
                duration="2 weeks",
                steps=[
                    Step(
                        action="Do deep work",
                        when="Morning",
                        duration="30 minutes",
                        why="Build focus habits",
                    )
                ],
            )
        ],
        dos=[
            ActionItem(
                action="Sleep 8 hours",
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
            ContentMapping(section_id="sec-1", reason="Explains focus protocols")
        ],
    )

    assert plan.model_dump(exclude_none=True) == {
        "goal": "Improve focus",
        "estimated_duration": "4 weeks",
        "phases": [
            {
                "name": "Phase 1",
                "duration": "2 weeks",
                "steps": [
                    {
                        "action": "Do deep work",
                        "when": "Morning",
                        "duration": "30 minutes",
                        "why": "Build focus habits",
                    }
                ],
            }
        ],
        "dos": [
            {
                "action": "Sleep 8 hours",
                "when": "Night",
                "why": "Restores attention",
            }
        ],
        "donts": [
            {
                "action": "Skip breaks",
                "why": "Increases fatigue",
            }
        ],
        "relevant_content": [
            {"section_id": "sec-1", "reason": "Explains focus protocols"}
        ],
    }


def test_section_content_requires_flashcards() -> None:
    """SectionContent rejects empty flashcards."""
    with pytest.raises(ValidationError):
        SectionContent(
            section_id="sec-1",
            summary="Summary",
            key_points=["A", "B"],
            glossary=[],
            flashcards=[],
        )

    SectionContent(
        section_id="sec-1",
        summary="Summary",
        key_points=["A", "B"],
        glossary=[],
        flashcards=[
            Flashcard(id="fc-1", question="Q?", answer="A")
        ],
    )
