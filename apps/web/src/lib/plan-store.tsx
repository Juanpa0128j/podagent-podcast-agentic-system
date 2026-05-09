"use client";

import {
  createContext,
  useContext,
  useState,
  useCallback,
  type ReactNode,
} from "react";

import type { Plan, SectionContent } from "../types/learnflow";

interface LearnFlowState {
  plan: Plan | null;
  section: SectionContent | null;
  error: string | null;
  loading: boolean;
}

interface LearnFlowActions {
  setPlan: (plan: Plan) => void;
  setSection: (section: SectionContent) => void;
  setError: (error: string) => void;
  setLoading: (loading: boolean) => void;
  reset: () => void;
}

interface LearnFlowStore {
  state: LearnFlowState;
  actions: LearnFlowActions;
}

const INITIAL_STATE: LearnFlowState = {
  plan: null,
  section: null,
  error: null,
  loading: false,
};

const LearnFlowContext = createContext<LearnFlowStore | null>(null);

export function LearnFlowProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<LearnFlowState>(INITIAL_STATE);

  const setPlan = useCallback((plan: Plan) => {
    setState((prev) => ({ ...prev, plan, error: null }));
  }, []);

  const setSection = useCallback((section: SectionContent) => {
    setState((prev) => ({ ...prev, section, error: null }));
  }, []);

  const setError = useCallback((error: string) => {
    setState((prev) => ({ ...prev, error, loading: false }));
  }, []);

  const setLoading = useCallback((loading: boolean) => {
    setState((prev) => ({ ...prev, loading }));
  }, []);

  const reset = useCallback(() => {
    setState(INITIAL_STATE);
  }, []);

  const actions: LearnFlowActions = {
    setPlan,
    setSection,
    setError,
    setLoading,
    reset,
  };

  return (
    <LearnFlowContext.Provider value={{ state, actions }}>
      {children}
    </LearnFlowContext.Provider>
  );
}

export function useLearnFlow(): LearnFlowStore {
  const store = useContext(LearnFlowContext);
  if (!store) {
    throw new Error("LearnFlowProvider is missing");
  }
  return store;
}
