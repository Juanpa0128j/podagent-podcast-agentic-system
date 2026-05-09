import { describe, expect, it } from "vitest";

import {
  createProgressState,
  progressReducer,
} from "../../src/lib/progress-store";

describe("progress store", () => {
  it("records flashcard results immutably", () => {
    const state = createProgressState();

    const next = progressReducer(state, {
      type: "recordFlashcardResult",
      cardId: "fc-1",
      result: "known",
    });

    expect(next.flashcard_results["fc-1"]).toBe("known");
    expect(next).not.toBe(state);
    expect(next.flashcard_results).not.toBe(state.flashcard_results);
  });
});
