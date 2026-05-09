import { describe, it, expect, vi, beforeEach } from "vitest";

const ENDPOINT = "/api/learnflow/answer_with_rag";

function makeSuccessResponse(answer: string) {
  return {
    ok: true,
    json: async () => ({ success: true, data: { answer } }),
  };
}

function makeErrorResponse(error: string) {
  return {
    ok: false,
    json: async () => ({ success: false, error }),
  };
}

// Inline handler logic mirroring AnswerAction for unit testing
async function answerActionHandler({
  question,
  context,
}: {
  question: string;
  context?: string;
}): Promise<string> {
  const body: Record<string, unknown> = { question };
  if (context) body.context = context;

  const response = await fetch(ENDPOINT, {
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
}

describe("AnswerAction handler", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("calls correct endpoint with question body", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(makeSuccessResponse("Respuesta de prueba"));
    vi.stubGlobal("fetch", fetchMock);

    await answerActionHandler({ question: "¿Qué es RAG?" });

    expect(fetchMock).toHaveBeenCalledOnce();
    expect(fetchMock).toHaveBeenCalledWith(
      ENDPOINT,
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: "¿Qué es RAG?" }),
      })
    );
  });

  it("includes context in body when provided", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(makeSuccessResponse("Con contexto"));
    vi.stubGlobal("fetch", fetchMock);

    await answerActionHandler({ question: "Explica esto", context: "sección 2" });

    const call = fetchMock.mock.calls[0];
    const body = JSON.parse(call[1].body as string);
    expect(body).toEqual({ question: "Explica esto", context: "sección 2" });
  });

  it("returns answer string on success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(makeSuccessResponse("El RAG usa embeddings"))
    );

    const result = await answerActionHandler({ question: "¿Cómo funciona RAG?" });
    expect(result).toBe("El RAG usa embeddings");
  });

  it("returns error message when API fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(makeErrorResponse("vector store unavailable"))
    );

    const result = await answerActionHandler({ question: "test" });
    expect(result).toContain("Lo siento");
    expect(result).toContain("vector store unavailable");
  });

  it("omits context key when not provided", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(makeSuccessResponse("ok"));
    vi.stubGlobal("fetch", fetchMock);

    await answerActionHandler({ question: "solo pregunta" });

    const body = JSON.parse(fetchMock.mock.calls[0][1].body as string);
    expect(Object.keys(body)).not.toContain("context");
  });
});
