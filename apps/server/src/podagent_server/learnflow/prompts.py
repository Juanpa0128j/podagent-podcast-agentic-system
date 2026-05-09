"""Prompt builders for LearnFlow structured outputs."""

from __future__ import annotations

import json
from typing import Any


def build_plan_prompt(goal: str, retrieved_chunks: list[dict[str, Any]]) -> str:
    """Build prompt for plan generation."""
    chunks_json = json.dumps(retrieved_chunks, ensure_ascii=True)
    return (
        "You are a science-based wellness coach. "
        f"The user has this goal: {goal}. "
        f"You have access to these podcast episodes/sections: {chunks_json}. "
        "Generate a structured learning plan in JSON format with fields: "
        "goal, estimated_duration, phases (name, duration, steps[action, when, duration, why]), "
        "dos (action, when, why), donts (action, why), relevant_content (section_id, reason)."
    )


def build_section_prompt(goal: str, transcript: str) -> str:
    """Build prompt for section content generation."""
    return (
        "Generate educational content for this podcast section. "
        f"The user's goal is: {goal}. "
        f"The section transcript is: {transcript}. "
        "Generate JSON with fields: summary, key_points, glossary (term, definition), "
        "flashcards (id, question, answer), section_id."
    )


def build_answer_prompt(
    question: str,
    context: str | None,
    retrieved_chunks: list[dict[str, Any]],
) -> str:
    """Build prompt for RAG answer generation."""
    chunks_json = json.dumps(retrieved_chunks, ensure_ascii=True)
    context_text = context or ""
    return (
        "Answer the user's question using the retrieved podcast chunks. "
        f"Question: {question}. "
        f"Context: {context_text}. "
        f"Retrieved chunks: {chunks_json}. "
        "Return JSON with fields: answer, citations (chunk_id, episode_id, ts_start, ts_end, text)."
    )
