"use client";

import { useMemo, useReducer } from "react";

import { createFlashcardState, flashcardReducer } from "../../lib/flashcard-session";
import { useProgressStore } from "../../lib/progress-store";
import type { Flashcard, FlashcardResult } from "../../types/learnflow";

interface FlashcardSessionProps {
  topic: string;
  cards: Flashcard[];
}

export default function FlashcardSession({
  topic,
  cards,
}: FlashcardSessionProps) {
  const { actions } = useProgressStore();
  const [state, dispatch] = useReducer(
    flashcardReducer,
    cards.length,
    createFlashcardState
  );

  const { currentIndex, isFlipped, results, total } = state;

  const currentCard = cards[currentIndex];

  const progressText = useMemo(
    () =>
      total > 0
        ? `${Math.min(currentIndex + 1, total)}/${total}`
        : "0/0",
    [currentIndex, total]
  );

  const recordResult = (result: FlashcardResult) => {
    if (!currentCard) {
      return;
    }

    dispatch({
      type: "recordResult",
      cardId: currentCard.id,
      result,
    });
    actions.recordFlashcardResult(currentCard.id, result);
  };

  if (!currentCard) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 rounded-xl border border-slate-200 bg-white p-10 text-center shadow-sm">
        <h1 className="text-2xl font-semibold">Sesion finalizada</h1>
        <p className="text-sm text-slate-500">
          Resultados registrados: {Object.keys(results).length}
        </p>
      </div>
    );
  }

  return (
    <section className="space-y-8">
      <div className="flex items-center justify-between text-sm text-slate-600">
        <span className="font-semibold text-on-surface">{topic}</span>
        <div className="flex flex-1 items-center gap-4 px-6">
          <span className="text-xs font-semibold text-slate-500">
            {progressText}
          </span>
          <div className="h-2 flex-1 rounded-full bg-slate-100">
            <div
              className="h-2 rounded-full bg-primary"
              style={{
                width: total
                  ? `${(Math.min(currentIndex + 1, total) / total) * 100}%`
                  : "0%",
              }}
            />
          </div>
        </div>
        <button type="button" aria-label="Cerrar">
          ✕
        </button>
      </div>

      <div className="flip-card">
        <div
          className={`flip-card-inner ${isFlipped ? "is-flipped" : ""}`}
        >
          <div className="flip-card-face rounded-2xl bg-white p-8 shadow-[0_10px_20px_rgba(0,0,0,0.04)]">
            <div className="text-xs font-semibold uppercase tracking-widest text-slate-400">
              Pregunta
            </div>
            <p className="mt-4 text-2xl font-semibold text-on-surface">
              {currentCard.question}
            </p>
          </div>
          <div className="flip-card-face flip-card-back rounded-2xl bg-white p-8 shadow-[0_10px_20px_rgba(0,0,0,0.04)]">
            <div className="text-xs font-semibold uppercase tracking-widest text-slate-400">
              Respuesta
            </div>
            <p className="mt-4 text-2xl font-semibold text-on-surface">
              {currentCard.answer}
            </p>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <button
          type="button"
          onClick={() => dispatch({ type: "flip" })}
          className="rounded-md border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-600"
        >
          Voltear tarjeta
        </button>
        <div className="grid gap-3 md:grid-cols-2">
          <button
            type="button"
            onClick={() => recordResult("unknown")}
            className="flex items-center justify-center gap-2 rounded-md bg-tertiary px-5 py-4 text-sm font-semibold text-white"
          >
            No lo sabia
          </button>
          <button
            type="button"
            onClick={() => recordResult("known")}
            className="flex items-center justify-center gap-2 rounded-md bg-secondary px-5 py-4 text-sm font-semibold text-white"
          >
            Lo sabia
          </button>
        </div>
      </div>
    </section>
  );
}
