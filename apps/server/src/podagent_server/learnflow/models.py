"""LearnFlow Pydantic models for structured outputs."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class Step(BaseModel):
    """A single plan step."""

    action: str
    when: str
    duration: str
    why: str


class Phase(BaseModel):
    """A plan phase with steps."""

    name: str
    duration: str
    steps: list[Step] = Field(default_factory=list)


class ActionItem(BaseModel):
    """A single action item in a plan."""

    action: str
    when: str | None = None
    why: str


class ContentMapping(BaseModel):
    """Mapping from plan to relevant content sections."""

    section_id: str
    reason: str

    @field_validator("section_id", mode="before")
    @classmethod
    def coerce_section_id(cls, value: object) -> str:
        return str(value)


class Plan(BaseModel):
    """Structured learning plan output."""

    goal: str
    estimated_duration: str
    phases: list[Phase] = Field(default_factory=list)
    dos: list[ActionItem] = Field(default_factory=list)
    donts: list[ActionItem] = Field(default_factory=list)
    relevant_content: list[ContentMapping] = Field(default_factory=list)


class GlossaryTerm(BaseModel):
    """Glossary term definition."""

    term: str
    definition: str


class Flashcard(BaseModel):
    """Flashcard for active recall."""

    id: str
    question: str
    answer: str

    @field_validator("id", mode="before")
    @classmethod
    def coerce_id(cls, value: object) -> str:
        return str(value)


class SectionContent(BaseModel):
    """Structured section content output."""

    section_id: str
    summary: str
    key_points: list[str] = Field(default_factory=list)
    glossary: list[GlossaryTerm] = Field(default_factory=list)
    flashcards: list[Flashcard] = Field(default_factory=list)

    @field_validator("flashcards")
    @classmethod
    def flashcards_must_not_be_empty(cls, value: list[Flashcard]) -> list[Flashcard]:
        if not value:
            raise ValueError("flashcards must not be empty")
        return value


class Citation(BaseModel):
    """Citation for an answer grounded in retrieved chunks."""

    chunk_id: int | None = None
    episode_id: str | None = None
    ts_start: float | None = None
    ts_end: float | None = None
    text: str | None = None


class Answer(BaseModel):
    """Answer with citations."""

    answer: str
    citations: list[Citation] = Field(default_factory=list)
