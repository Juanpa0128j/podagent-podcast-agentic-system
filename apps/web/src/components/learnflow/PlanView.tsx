import Link from "next/link";

import type { Plan } from "../../types/learnflow";

interface PlanViewProps {
  plan: Plan;
}

export default function PlanView({ plan }: PlanViewProps) {
  const firstSectionId = plan.relevant_content[0]?.section_id;
  const startHref = firstSectionId
    ? `/section/${encodeURIComponent(firstSectionId)}`
    : "/flashcards";

  return (
    <section className="space-y-10">
      <div className="space-y-3">
        <span className="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
          Generado para ti
        </span>
        <h1 className="text-3xl font-bold tracking-tight text-on-surface">
          {plan.goal}
        </h1>
        <p className="text-base text-slate-600">
          Plan estimado: {plan.estimated_duration}. Ajusta segun tu ritmo.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[2fr,1fr]">
        <div className="space-y-6 rounded-xl border border-slate-200 bg-surface-container p-6 shadow-sm">
          <h2 className="text-xl font-semibold">Timeline</h2>
          <div className="space-y-6">
            {plan.phases.map((phase, index) => (
              <div key={phase.name} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <span className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-primary text-sm font-semibold text-primary">
                    {index + 1}
                  </span>
                  {index < plan.phases.length - 1 ? (
                    <span className="mt-2 h-full w-px bg-slate-200" />
                  ) : null}
                </div>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-semibold text-on-surface">
                      {phase.name}
                    </h3>
                    <span className="text-xs text-slate-500">
                      {phase.duration}
                    </span>
                  </div>
                  <ul className="space-y-2 text-sm text-slate-600">
                    {phase.steps.map((step) => (
                      <li key={step.action} className="rounded-lg bg-slate-50 p-3">
                        <div className="font-semibold text-slate-700">
                          {step.action}
                        </div>
                        <div className="text-xs text-slate-500">
                          {step.when} · {step.duration}
                        </div>
                        <div className="text-xs text-slate-500">
                          {step.why}
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div className="rounded-xl border border-slate-200 bg-surface-container p-5 shadow-sm">
            <div className="flex items-center gap-2 text-secondary">
              <span>✅</span>
              <h3 className="text-lg font-semibold">DO&apos;s</h3>
            </div>
            <div className="mt-4 space-y-3">
              {plan.dos.map((item) => (
                <div
                  key={item.action}
                  className="rounded-lg border-l-4 border-secondary bg-white p-3"
                >
                  <div className="text-sm font-semibold text-slate-700">
                    {item.action}
                  </div>
                  {item.when ? (
                    <div className="text-xs text-slate-500">
                      {item.when}
                    </div>
                  ) : null}
                  <div className="text-xs text-slate-500">{item.why}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-surface-container p-5 shadow-sm">
            <div className="flex items-center gap-2 text-tertiary">
              <span>❌</span>
              <h3 className="text-lg font-semibold">DON&apos;Ts</h3>
            </div>
            <div className="mt-4 space-y-3">
              {plan.donts.map((item) => (
                <div
                  key={item.action}
                  className="rounded-lg border-l-4 border-tertiary bg-white p-3"
                >
                  <div className="text-sm font-semibold text-slate-700">
                    {item.action}
                  </div>
                  <div className="text-xs text-slate-500">{item.why}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {plan.relevant_content.length > 0 ? (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Material recomendado</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {plan.relevant_content.map((content, index) => (
              <Link
                key={content.section_id}
                href={`/section/${encodeURIComponent(content.section_id)}`}
                className="group flex items-start gap-4 rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-primary hover:shadow-md"
              >
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-lg font-semibold text-primary">
                  {index + 1}
                </div>
                <div className="space-y-2">
                  <h3 className="text-sm font-semibold text-on-surface">
                    Seccion {index + 1}
                  </h3>
                  <p className="text-xs leading-relaxed text-slate-600">
                    {content.reason}
                  </p>
                  <span className="inline-flex items-center gap-1 text-xs font-semibold text-primary group-hover:underline">
                    Abrir seccion <span aria-hidden>→</span>
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      ) : null}

      <div className="flex justify-end">
        <Link
          href={startHref}
          className="inline-flex items-center gap-2 rounded-md bg-primary px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-container"
        >
          Comenzar plan
          <span aria-hidden>→</span>
        </Link>
      </div>
    </section>
  );
}
