import type { FlashcardResult } from "../types/learnflow";

export interface FlashcardState {
  currentIndex: number;
  isFlipped: boolean;
  results: Record<string, FlashcardResult>;
  total: number;
}

export type FlashcardAction =
  | { type: "flip" }
  | { type: "advance" }
  | { type: "recordResult"; cardId: string; result: FlashcardResult };

export function createFlashcardState(total: number): FlashcardState {
  return {
    currentIndex: 0,
    isFlipped: false,
    results: {},
    total,
  };
}

function getNextIndex(currentIndex: number, total: number): number {
  return Math.min(currentIndex + 1, total);
}

export function flashcardReducer(
  state: FlashcardState,
  action: FlashcardAction
): FlashcardState {
  switch (action.type) {
    case "flip":
      return {
        ...state,
        isFlipped: !state.isFlipped,
      };
    case "advance":
      return {
        ...state,
        currentIndex: getNextIndex(state.currentIndex, state.total),
      };
    case "recordResult":
      return {
        ...state,
        results: {
          ...state.results,
          [action.cardId]: action.result,
        },
        isFlipped: false,
        currentIndex: getNextIndex(state.currentIndex, state.total),
      };
    default: {
      const exhaustive: never = action;
      return state;
    }
  }
}
