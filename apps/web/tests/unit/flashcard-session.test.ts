import { describe, expect, it } from "vitest";

import {
  createFlashcardState,
  flashcardReducer,
} from "../../src/lib/flashcard-session";

describe("flashcard session reducer", () => {
  it("advances index and caps at total", () => {
    const initial = {
      ...createFlashcardState(2),
      currentIndex: 1,
    };

    const next = flashcardReducer(initial, { type: "advance" });
    expect(next.currentIndex).toBe(2);

    const capped = flashcardReducer(next, { type: "advance" });
    expect(capped.currentIndex).toBe(2);
  });
});
