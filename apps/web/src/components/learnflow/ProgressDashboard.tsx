"use client";

import { useMemo, useState } from "react";

import { useLearnFlow } from "../../lib/plan-store";
import { useProgressStore } from "../../lib/progress-store";

const CHECKIN_QUESTIONS = [
  "Cumpliste tu bloque de enfoque?",
  "Dormiste 7+ horas?",
];

export default function ProgressDashboard() {
  const { state: planState } = useLearnFlow();
  const plan = planState.plan;
  const { state, actions } = useProgressStore();
  const [checkinAnswers, setCheckinAnswers] = useState<Record<string, "yes" | "no">>({});
  const [savedAt, setSavedAt] = useState<number | null>(null);

  const totalSections = plan?.relevant_content.length ?? 0;
  const completedSections = state.completed_sections.length;
  const planPercent = totalSections
    ? Math.round((completedSections / totalSections) * 100)
    : 0;

  const flashcardSummary = useMemo(() => {
    const entries = Object.values(state.flashcard_results);
    const known = entries.filter((r) => r === "known").length;
    const unknown = entries.filter((r) => r === "unknown").length;
    const total = known + unknown;
    const knownPercent = total ? Math.round((known / total) * 100) : 0;
    return { known, unknown, knownPercent };
  }, [state.flashcard_results]);

  const planSteps = useMemo(() => {
    if (!plan) return [] as { id: string; label: string; done: boolean }[];
    return plan.phases.flatMap((phase) =>
      phase.steps.map((step) => ({
        id: step.action,
        label: step.action,
        done: state.completed_steps.includes(step.action),
      }))
    );
  }, [plan, state.completed_steps]);

  const handleCheckinAnswer = (question: string, answer: "yes" | "no") => {
    setCheckinAnswers((prev) => ({ ...prev, [question]: answer }));
  };

  const handleSaveCheckin = () => {
    const date = new Date().toISOString().slice(0, 10);
    Object.entries(checkinAnswers).forEach(([question, answer]) => {
      actions.addCheckinResponse({ date, question, answer });
    });
    setCheckinAnswers({});
    setSavedAt(Date.now());
    window.setTimeout(() => setSavedAt(null), 2500);
  };

  return (
    <section className="space-y-8 relative">
      {savedAt ? (
        <div
          role="status"
          className="fixed right-6 top-6 z-50 rounded-md bg-secondary px-4 py-3 text-sm font-semibold text-white shadow-lg"
        >
          Check-in guardado ✓
        </div>
      ) : null}
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-on-surface">
          Tu Progreso
        </h1>
        <p className="text-base text-slate-600">
          Cada paso suma. Sigue el plan y observa tu avance.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-on-surface">
              Plan General
            </h2>
            <span className="text-xs text-slate-500">
              {planPercent}% completado
            </span>
          </div>
          <div className="mt-4 h-2 rounded-full bg-slate-100">
            <div
              className="h-2 rounded-full bg-primary"
              style={{ width: `${planPercent}%` }}
            />
          </div>
          <p className="mt-3 text-xs text-slate-500">
            Secciones completadas: {completedSections}/{totalSections}
          </p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🔥</span>
            <div>
              <p className="text-sm font-semibold">
                {state.streak} dias seguidos
              </p>
              <p className="text-xs text-slate-500">Sigue la racha</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-on-surface">
            Pasos del Plan
          </h2>
          {planSteps.length === 0 ? (
            <p className="mt-4 text-sm text-slate-500">
              Genera un plan en la pagina principal para ver tus pasos.
            </p>
          ) : (
            <ul className="mt-4 space-y-3 text-sm text-slate-600">
              {planSteps.map((step) => (
                <li key={step.id} className="flex items-center gap-3">
                  <span
                    className={`h-4 w-4 rounded-full border ${
                      step.done
                        ? "border-secondary bg-secondary"
                        : "border-slate-300"
                    }`}
                  />
                  <span className={step.done ? "line-through text-slate-400" : ""}>
                    {step.label}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-on-surface">
            Conocimiento
          </h2>
          <div className="mt-4 space-y-3 text-sm text-slate-600">
            <div className="flex items-center justify-between">
              <span>Dominados</span>
              <span className="text-secondary">{flashcardSummary.known}</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Por Repasar</span>
              <span className="text-tertiary">{flashcardSummary.unknown}</span>
            </div>
            <div className="h-2 rounded-full bg-slate-100">
              <div
                className="h-2 rounded-full bg-secondary"
                style={{ width: `${flashcardSummary.knownPercent}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 bg-primary/5 p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-on-surface">Check-in Rapido</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          {CHECKIN_QUESTIONS.map((question) => (
            <div
              key={question}
              className="rounded-lg border border-slate-200 bg-white p-4"
            >
              <p className="text-sm font-semibold text-slate-700">{question}</p>
              <div className="mt-3 flex gap-3">
                <button
                  type="button"
                  onClick={() => handleCheckinAnswer(question, "no")}
                  className={`rounded-md border px-3 py-2 text-xs ${
                    checkinAnswers[question] === "no"
                      ? "border-tertiary bg-tertiary text-white"
                      : "border-slate-200 text-slate-500"
                  }`}
                >
                  No
                </button>
                <button
                  type="button"
                  onClick={() => handleCheckinAnswer(question, "yes")}
                  className={`rounded-md px-3 py-2 text-xs ${
                    checkinAnswers[question] === "yes"
                      ? "bg-secondary text-white"
                      : "border border-slate-200 text-slate-500"
                  }`}
                >
                  Si
                </button>
              </div>
            </div>
          ))}
        </div>
        <button
          type="button"
          onClick={handleSaveCheckin}
          disabled={Object.keys(checkinAnswers).length === 0}
          className="mt-4 rounded-md bg-primary px-5 py-3 text-sm font-semibold text-white disabled:opacity-50"
        >
          Guardar Check-in
        </button>
      </div>
    </section>
  );
}
