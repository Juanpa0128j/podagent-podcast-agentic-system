"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

import { useProgressStore } from "../../lib/progress-store";
import type { SectionContent } from "../../types/learnflow";

interface SectionViewProps {
  title: string;
  description: string;
  content: SectionContent;
}

export default function SectionView({
  title,
  description,
  content,
}: SectionViewProps) {
  const router = useRouter();
  const { state, actions } = useProgressStore();
  const isCompleted = state.completed_sections.includes(content.section_id);

  const handleComplete = () => {
    actions.completeSection(content.section_id);
    router.push("/progress");
  };

  return (
    <section className="space-y-8">
      <div className="space-y-2">
        <Link
          href="/plan"
          className="text-sm font-medium text-primary hover:underline"
        >
          Volver al plan
        </Link>
        <span className="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
          Episodio Analizado
        </span>
        <h1 className="text-3xl font-bold tracking-tight text-on-surface">
          {title}
        </h1>
        <p className="text-base text-slate-600">{description}</p>
      </div>

      <div className="space-y-4">
        <details className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm" open>
          <summary className="cursor-pointer text-sm font-semibold text-on-surface">
            Resumen
          </summary>
          <p className="mt-3 text-sm text-slate-600">{content.summary}</p>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-600">
            {content.key_points.map((point) => (
              <li key={point}>{point}</li>
            ))}
          </ul>
        </details>

        <details className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <summary className="cursor-pointer text-sm font-semibold text-on-surface">
            Glosario
          </summary>
          <div className="mt-3 space-y-3 text-sm text-slate-600">
            {content.glossary.map((term) => (
              <div key={term.term}>
                <div className="font-semibold text-slate-700">{term.term}</div>
                <div>{term.definition}</div>
              </div>
            ))}
          </div>
        </details>

        <details className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <summary className="cursor-pointer text-sm font-semibold text-on-surface">
            Flashcards
          </summary>
          <div className="mt-3 grid gap-3 md:grid-cols-2">
            {content.flashcards.slice(0, 2).map((card) => (
              <div
                key={card.id}
                className="rounded-lg border border-slate-200 bg-slate-50 p-4"
              >
                <div className="text-xs font-semibold uppercase tracking-widest text-slate-400">
                  Pregunta
                </div>
                <div className="mt-2 text-sm font-semibold text-slate-700">
                  {card.question}
                </div>
              </div>
            ))}
          </div>
        </details>
      </div>

      <div className="flex flex-wrap gap-3">
        <Link
          href="/flashcards"
          className="inline-flex items-center gap-2 rounded-md bg-primary px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-container"
        >
          Iniciar estudio
        </Link>
        <button
          type="button"
          onClick={handleComplete}
          disabled={isCompleted}
          className="inline-flex items-center gap-2 rounded-md border border-slate-200 px-6 py-3 text-sm font-semibold text-slate-600 transition hover:border-primary hover:text-primary disabled:opacity-50"
        >
          {isCompleted ? "Completada ✓" : "Marcar como completada"}
        </button>
      </div>
    </section>
  );
}
