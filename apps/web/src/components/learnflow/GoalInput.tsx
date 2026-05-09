"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { generatePlan } from "../../lib/mcp-client";
import { useLearnFlow } from "../../lib/plan-store";

const popularGoals = [
  "Concentracion",
  "Dormir mejor",
  "Mas energia",
  "Reducir estres",
];

export default function GoalInput() {
  const router = useRouter();
  const { actions } = useLearnFlow();
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const normalizedGoal = goal.trim();
  const canSubmit = normalizedGoal.length > 0 && !loading;

  const handleSubmit = async () => {
    if (!canSubmit) {
      return;
    }

    setLoading(true);
    setError(null);
    actions.setLoading(true);

    try {
      const plan = await generatePlan(normalizedGoal);
      actions.setPlan(plan);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Error generating plan";
      setError(message);
      actions.setError(message);
      // Fallback: navigate anyway — PlanPage will use samplePlan
    } finally {
      setLoading(false);
      actions.setLoading(false);
    }

    const encoded = encodeURIComponent(normalizedGoal);
    router.push(`/plan?goal=${encoded}`);
  };

  return (
    <section className="flex min-h-[70vh] flex-col items-center justify-center gap-8 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-white">
        ✨
      </div>
      <div className="space-y-3">
        <h1 className="text-4xl font-bold tracking-tight text-on-surface">
          Cual es tu meta?
        </h1>
        <p className="max-w-xl text-base text-slate-600">
          Aprende con ciencia aplicada. Generamos un plan accionable a partir
          de podcasts expertos.
        </p>
      </div>
      <div className="w-full max-w-xl space-y-4">
        <textarea
          className="min-h-[140px] w-full rounded-lg border border-slate-200 bg-white p-4 text-base text-slate-700 shadow-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
          placeholder="Ejemplo: Quiero mejorar mi concentracion para estudiar mejor"
          value={goal}
          onChange={(event) => setGoal(event.target.value)}
        />
        {error ? (
          <p role="alert" className="text-sm text-red-600">
            {error} — usando plan de muestra.
          </p>
        ) : null}
        <button
          type="button"
          onClick={handleSubmit}
          disabled={!canSubmit}
          className="flex w-full items-center justify-center gap-2 rounded-md bg-primary px-6 py-4 text-base font-semibold text-white transition hover:bg-primary-container disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {loading ? "Generando..." : "Generar mi plan"}
          <span aria-hidden>✨</span>
        </button>
      </div>
      <div className="w-full max-w-xl">
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
          Metas populares
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          {popularGoals.map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setGoal(item)}
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-600 transition hover:border-primary hover:text-primary"
            >
              {item}
            </button>
          ))}
        </div>
      </div>
      <footer className="mt-6 flex flex-col items-center gap-2 text-xs text-slate-400">
        <span className="font-semibold text-slate-500">LearnFlow</span>
        <div className="flex gap-4">
          <a href="#">Soporte</a>
          <a href="#">Privacidad</a>
          <a href="#">Terminos</a>
        </div>
      </footer>
    </section>
  );
}
