"""Prompt builders for LearnFlow structured outputs."""

from __future__ import annotations

import json
from typing import Any

LANGUAGE_RULE = (
    "IMPORTANTE: TODO el contenido (titulos, descripciones, pasos, glosario, "
    "preguntas, respuestas, razones) DEBE estar en espanol. "
    "Las claves del JSON permanecen en ingles, pero los valores en espanol."
)


def build_plan_prompt(goal: str, retrieved_chunks: list[dict[str, Any]]) -> str:
    """Build prompt for plan generation."""
    chunks_json = json.dumps(retrieved_chunks, ensure_ascii=False)
    return (
        "Eres un coach de bienestar basado en evidencia cientifica. "
        f"El objetivo del usuario es: {goal}. "
        f"Tienes acceso a estos episodios/secciones de podcast: {chunks_json}. "
        "Genera un plan de aprendizaje estructurado en formato JSON con los campos: "
        "goal, estimated_duration, phases (name, duration, steps[action, when, duration, why]), "
        "dos (action, when, why), donts (action, why), relevant_content (section_id, reason). "
        + LANGUAGE_RULE
    )


def build_section_prompt(goal: str, transcript: str) -> str:
    """Build prompt for section content generation."""
    return (
        "Genera contenido educativo para esta seccion del podcast. "
        f"El objetivo del usuario es: {goal}. "
        f"La transcripcion de la seccion es: {transcript}. "
        "Genera un JSON con los campos: summary, key_points, glossary (term, definition), "
        "flashcards (id, question, answer), section_id. "
        + LANGUAGE_RULE
    )


def build_answer_prompt(
    question: str,
    context: str | None,
    retrieved_chunks: list[dict[str, Any]],
) -> str:
    """Build prompt for RAG answer generation."""
    chunks_json = json.dumps(retrieved_chunks, ensure_ascii=False)
    context_text = context or ""
    return (
        "Responde la pregunta del usuario usando los fragmentos de podcast recuperados. "
        f"Pregunta: {question}. "
        f"Contexto: {context_text}. "
        f"Fragmentos recuperados: {chunks_json}. "
        "Responde en JSON con los campos: answer, citations (chunk_id, episode_id, ts_start, ts_end, text). "
        + LANGUAGE_RULE
    )
