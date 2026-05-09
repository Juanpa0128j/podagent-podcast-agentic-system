"use client";

import { useLearnFlow } from "../../lib/plan-store";
import FlashcardSession from "./FlashcardSession";
import { sampleSection } from "../../lib/learnflow-sample";

export default function FlashcardsLoader() {
  const { state } = useLearnFlow();
  const cards = state.section?.flashcards ?? sampleSection.flashcards;
  const topic = state.section?.section_id ?? "Focus y energia";

  return <FlashcardSession topic={topic} cards={cards} />;
}
