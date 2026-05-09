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
