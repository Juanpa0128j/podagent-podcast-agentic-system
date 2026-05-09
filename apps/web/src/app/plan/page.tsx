import PlanView from "../../components/learnflow/PlanView";
import PlanLoader from "../../components/learnflow/PlanLoader";
import { samplePlan } from "../../lib/learnflow-sample";

interface PlanPageProps {
  searchParams?: Promise<{ goal?: string | string[] }>;
}

export default async function PlanPage({ searchParams }: PlanPageProps) {
  const resolved = (await searchParams) ?? {};
  const goalParam = Array.isArray(resolved.goal)
    ? resolved.goal[0]
    : resolved.goal;

  const fallbackPlan = {
    ...samplePlan,
    goal: goalParam ?? samplePlan.goal,
  };

  return (
    <PlanLoader
      fallback={<PlanView plan={fallbackPlan} />}
      fallbackPlan={fallbackPlan}
    />
  );
}
