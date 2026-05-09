import React from "react";
import type { ReactNode } from "react";
import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";

// Mock Next.js Link used inside SectionView
vi.mock("next/link", () => ({
  default: ({ href, children }: { href: string; children: ReactNode }) => (
    <a href={href}>{children}</a>
  ),
}));

import MCPAppRenderer from "../../src/lib/mcp-apps/renderer";
import { ProgressProvider } from "../../src/lib/progress-store";
import type { Plan, SectionContent } from "../../src/types/learnflow";

function renderWithProviders(ui: React.ReactElement) {
  return render(<ProgressProvider>{ui}</ProgressProvider>);
}

const samplePlan: Plan = {
  goal: "Test goal",
  estimated_duration: "1 week",
  phases: [],
  dos: [],
  donts: [],
  relevant_content: [],
};

const sampleSection: SectionContent = {
  section_id: "sec-1",
  summary: "Test summary",
  key_points: [],
  glossary: [],
  flashcards: [],
};

describe("MCPAppRenderer", () => {
  it("renders PlanView when hint component is PlanView", () => {
    renderWithProviders(
      <MCPAppRenderer hint={{ component: "PlanView", version: 1 }} data={{ plan: samplePlan }} />
    );
    expect(screen.getByText(/generado para ti/i)).toBeInTheDocument();
    expect(screen.getByText(/test goal/i)).toBeInTheDocument();
  });

  it("renders SectionView when hint component is SectionView", () => {
    renderWithProviders(
      <MCPAppRenderer
        hint={{ component: "SectionView", version: 1 }}
        data={{
          title: "Episode Title",
          description: "Episode description",
          content: sampleSection,
        }}
      />
    );
    expect(screen.getByText(/episode title/i)).toBeInTheDocument();
  });

  it("renders diagnostic fallback for unknown component", () => {
    renderWithProviders(
      <MCPAppRenderer hint={{ component: "UnknownWidget", version: 1 }} data={{}} />
    );
    const alert = screen.getByRole("alert");
    expect(alert).toBeInTheDocument();
    expect(alert).toHaveTextContent("UnknownWidget");
    expect(alert).toHaveTextContent("PlanView");
  });
});
