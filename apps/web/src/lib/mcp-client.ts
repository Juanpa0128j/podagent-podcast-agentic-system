import type { Plan, SectionContent } from "../types/learnflow";
import type { MCPAppResponse } from "./mcp-apps/types";

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

async function callTool<T>(tool: string, args: Record<string, unknown>): Promise<T> {
  const response = await fetch(`/api/learnflow/${tool}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(args),
  });

  const json: ApiResponse<T> = await response.json();

  if (!json.success || !json.data) {
    throw new Error(json.error ?? `Tool ${tool} returned no data`);
  }

  return json.data;
}

/**
 * Call a UI-aware tool that returns an MCPAppResponse envelope.
 * Unwraps `data` for typed consumers; the envelope is available on the response
 * object for renderer-aware callers.
 */
async function callUiTool<T>(
  tool: string,
  args: Record<string, unknown>
): Promise<MCPAppResponse<T>> {
  return callTool<MCPAppResponse<T>>(tool, args);
}

export async function generatePlan(goal: string): Promise<Plan> {
  const envelope = await callUiTool<Plan>("generate_plan", { goal });
  return envelope.data;
}

export async function generateSectionContent(
  sectionId: string,
  goal: string
): Promise<SectionContent> {
  const envelope = await callUiTool<SectionContent>("generate_section_content", {
    section_id: sectionId,
    goal,
  });
  return envelope.data;
}

export async function answerWithRag(
  question: string,
  context?: string
): Promise<{ answer: string }> {
  return callTool<{ answer: string }>("answer_with_rag", { question, context });
}
