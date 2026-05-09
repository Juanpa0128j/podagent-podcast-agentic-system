import { describe, expect, it, vi, beforeEach } from "vitest";

const fetchMock = vi.fn();
vi.stubGlobal("fetch", fetchMock);

import { generatePlan, generateSectionContent, answerWithRag } from "../../src/lib/mcp-client";

const fakePlan = {
  goal: "test",
  estimated_duration: "1 week",
  phases: [],
  dos: [],
  donts: [],
  relevant_content: [],
};

const fakeSectionContent = {
  section_id: "s1",
  summary: "test",
  key_points: [],
  glossary: [],
  flashcards: [],
};

function mockFetchSuccess(data: unknown) {
  fetchMock.mockResolvedValueOnce({
    json: () => Promise.resolve({ success: true, data }),
  });
}

function mockFetchError(error: string) {
  fetchMock.mockResolvedValueOnce({
    json: () => Promise.resolve({ success: false, error }),
  });
}

describe("mcp-client", () => {
  beforeEach(() => {
    fetchMock.mockClear();
  });

  it("generatePlan calls correct endpoint and returns plan", async () => {
    // Server now wraps in MCPAppResponse envelope; client unwraps data for callers.
    mockFetchSuccess({ _ui: { component: "PlanView", version: 1 }, data: fakePlan });

    const result = await generatePlan("test goal");

    expect(fetchMock).toHaveBeenCalledWith("/api/learnflow/generate_plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal: "test goal" }),
    });
    expect(result).toEqual(fakePlan);
  });

  it("generateSectionContent passes section_id and goal", async () => {
    // Server now wraps in MCPAppResponse envelope; client unwraps data for callers.
    mockFetchSuccess({ _ui: { component: "SectionView", version: 1 }, data: fakeSectionContent });

    const result = await generateSectionContent("s1", "my goal");

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/learnflow/generate_section_content",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ section_id: "s1", goal: "my goal" }),
      }
    );
    expect(result).toEqual(fakeSectionContent);
  });

  it("answerWithRag forwards question and optional context", async () => {
    mockFetchSuccess({ answer: "42" });

    const result = await answerWithRag("What is life?", "context here");

    expect(fetchMock).toHaveBeenCalledWith("/api/learnflow/answer_with_rag", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: "What is life?", context: "context here" }),
    });
    expect(result).toEqual({ answer: "42" });
  });

  it("throws on API error response", async () => {
    mockFetchError("Server unavailable");

    await expect(generatePlan("fail")).rejects.toThrow("Server unavailable");
  });
});
