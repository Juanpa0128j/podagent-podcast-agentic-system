"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import type { ReactNode } from "react";

import { AnswerAction } from "./AnswerAction";

interface CopilotShellProps {
  children: ReactNode;
}

export function CopilotShell({ children }: CopilotShellProps) {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <AnswerAction />
      <CopilotSidebar
        instructions="Eres el asistente de LearnFlow. SIEMPRE respondes en espanol. Ayudas al usuario a entender su plan de aprendizaje, secciones del podcast y conceptos cientificos. Cuando el usuario hace una pregunta sobre el contenido del podcast, usa la accion answerWithRag."
        labels={{
          title: "Asistente LearnFlow",
          initial:
            "Pregunta sobre tu plan, secciones o conceptos del podcast.",
          placeholder: "Escribe tu pregunta aqui...",
        }}
      >
        {children}
      </CopilotSidebar>
    </CopilotKit>
  );
}
