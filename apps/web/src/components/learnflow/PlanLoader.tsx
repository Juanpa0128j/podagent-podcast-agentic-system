"use client";

import type { ReactNode } from "react";
import { useLearnFlow } from "../../lib/plan-store";
import MCPAppRenderer from "../../lib/mcp-apps/renderer";
import type { Plan } from "../../types/learnflow";

interface PlanLoaderProps {
  fallback: ReactNode;
  fallbackPlan: Plan;
}

const PLAN_HINT = { component: "PlanView", version: 1 } as const;

export default function PlanLoader({ fallback, fallbackPlan }: PlanLoaderProps) {
  const { state } = useLearnFlow();

  if (state.plan) {
    return <MCPAppRenderer hint={PLAN_HINT} data={{ plan: state.plan }} />;
  }

  // No real plan yet — render fallback (the sample plan path constructs hint manually)
  return <>{fallback}</>;
}
