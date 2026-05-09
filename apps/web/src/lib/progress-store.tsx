"use client";

import {
  createContext,
  useContext,
  useMemo,
  useReducer,
  type Dispatch,
  type ReactNode,
} from "react";

import type {
  CheckinResponse,
  FlashcardResult,
  UserProgress,
} from "../types/learnflow";

export type ProgressAction =
  | { type: "initialize"; goal: string; planId: string }
  | { type: "completeStep"; stepId: string }
  | { type: "completeSection"; sectionId: string }
  | {
      type: "recordFlashcardResult";
      cardId: string;
      result: FlashcardResult;
    }
  | { type: "addCheckinResponse"; response: CheckinResponse }
  | { type: "setStreak"; streak: number };

export function createProgressState(
  overrides: Partial<UserProgress> = {}
): UserProgress {
  const base: UserProgress = {
    goal: "",
    plan_id: "",
    completed_steps: [],
    completed_sections: [],
    flashcard_results: {},
    checkin_responses: [],
    streak: 0,
  };

  return {
    ...base,
    ...overrides,
    completed_steps: [...(overrides.completed_steps ?? base.completed_steps)],
    completed_sections: [
      ...(overrides.completed_sections ?? base.completed_sections),
    ],
    flashcard_results: {
      ...(overrides.flashcard_results ?? base.flashcard_results),
    },
    checkin_responses: [
      ...(overrides.checkin_responses ?? base.checkin_responses),
    ],
  };
}

function addUnique(values: string[], value: string): string[] {
  if (values.includes(value)) {
    return values;
  }
  return [...values, value];
}

export function progressReducer(
  state: UserProgress,
  action: ProgressAction
): UserProgress {
  switch (action.type) {
    case "initialize":
      return {
        ...state,
        goal: action.goal,
        plan_id: action.planId,
      };
    case "completeStep":
      return {
        ...state,
        completed_steps: addUnique(state.completed_steps, action.stepId),
      };
    case "completeSection":
      return {
        ...state,
        completed_sections: addUnique(
          state.completed_sections,
          action.sectionId
        ),
      };
    case "recordFlashcardResult":
      return {
        ...state,
        flashcard_results: {
          ...state.flashcard_results,
          [action.cardId]: action.result,
        },
      };
    case "addCheckinResponse":
      return {
        ...state,
        checkin_responses: [
          ...state.checkin_responses,
          action.response,
        ],
      };
    case "setStreak":
      return {
        ...state,
        streak: action.streak,
      };
    default: {
      const exhaustive: never = action;
      return state;
    }
  }
}

interface ProgressStore {
  state: UserProgress;
  actions: {
    initialize: (goal: string, planId: string) => void;
    completeStep: (stepId: string) => void;
    completeSection: (sectionId: string) => void;
    recordFlashcardResult: (
      cardId: string,
      result: FlashcardResult
    ) => void;
    addCheckinResponse: (response: CheckinResponse) => void;
    setStreak: (streak: number) => void;
  };
}

const ProgressStateContext = createContext<UserProgress | null>(
  null
);
const ProgressDispatchContext = createContext<Dispatch<ProgressAction> | null>(
  null
);

export function ProgressProvider({
  children,
  initial,
}: {
  children: ReactNode;
  initial?: Partial<UserProgress>;
}) {
  const [state, dispatch] = useReducer(
    progressReducer,
    initial,
    createProgressState
  );

  return (
    <ProgressStateContext.Provider value={state}>
      <ProgressDispatchContext.Provider value={dispatch}>
        {children}
      </ProgressDispatchContext.Provider>
    </ProgressStateContext.Provider>
  );
}

export function useProgressStore(): ProgressStore {
  const state = useContext(ProgressStateContext);
  const dispatch = useContext(ProgressDispatchContext);

  if (!state || !dispatch) {
    throw new Error("ProgressProvider is missing");
  }

  const actions = useMemo(
    () => ({
      initialize: (goal: string, planId: string) => {
        dispatch({ type: "initialize", goal, planId });
      },
      completeStep: (stepId: string) => {
        dispatch({ type: "completeStep", stepId });
      },
      completeSection: (sectionId: string) => {
        dispatch({ type: "completeSection", sectionId });
      },
      recordFlashcardResult: (
        cardId: string,
        result: FlashcardResult
      ) => {
        dispatch({
          type: "recordFlashcardResult",
          cardId,
          result,
        });
      },
      addCheckinResponse: (response: CheckinResponse) => {
        dispatch({ type: "addCheckinResponse", response });
      },
      setStreak: (streak: number) => {
        dispatch({ type: "setStreak", streak });
      },
    }),
    [dispatch]
  );

  return { state, actions };
}
