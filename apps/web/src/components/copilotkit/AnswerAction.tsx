"use client";

import { useCopilotAction } from "@copilotkit/react-core";

export function AnswerAction() {
  useCopilotAction({
    name: "answerWithRag",
    description:
      "Responde preguntas sobre el contenido del podcast usando búsqueda semántica RAG.",
    parameters: [
      {
        name: "question",
        type: "string",
        description: "La pregunta del usuario sobre el contenido del podcast.",
        required: true,
      },
      {
        name: "context",
        type: "string",
        description: "Contexto adicional opcional para la búsqueda.",
        required: false,
      },
    ],
    handler: async ({
      question,
      context,
    }: {
      question: string;
      context?: string;
    }) => {
      const body: Record<string, unknown> = { question };
      if (context) body.context = context;

      const response = await fetch("/api/learnflow/answer_with_rag", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const json: { success: boolean; data?: { answer: string }; error?: string } =
        await response.json();

      if (!json.success || !json.data) {
        return `Lo siento, no pude encontrar una respuesta: ${json.error ?? "error desconocido"}`;
      }

      return json.data.answer;
    },
  });

  return null;
}
