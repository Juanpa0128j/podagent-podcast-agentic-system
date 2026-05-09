import React from "react";
import type { ReactNode } from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

const push = vi.fn();

vi.mock("next/navigation", () => {
  return {
    useRouter: () => ({ push }),
  };
});

vi.mock("next/link", () => {
  return {
    default: ({
      href,
      children,
    }: {
      href: string;
      children: ReactNode;
    }) => <a href={href}>{children}</a>,
  };
});

// Stub fetch so GoalInput API call resolves quickly
const fetchMock = vi.fn().mockResolvedValue({
  json: () => Promise.resolve({ success: false, error: "test stub" }),
});
vi.stubGlobal("fetch", fetchMock);

import HomePage from "../../src/app/page";
import PlanPage from "../../src/app/plan/page";
import SectionPage from "../../src/app/section/[id]/page";
import FlashcardsPage from "../../src/app/flashcards/page";
import ProgressPage from "../../src/app/progress/page";
import { ProgressProvider } from "../../src/lib/progress-store";
import { LearnFlowProvider } from "../../src/lib/plan-store";

const renderWithProviders = (ui: React.ReactElement) =>
  render(
    <LearnFlowProvider>
      <ProgressProvider>{ui}</ProgressProvider>
    </LearnFlowProvider>
  );

describe("LearnFlow pages", () => {
  beforeEach(() => {
    push.mockClear();
    fetchMock.mockClear();
  });

  it("renders goal input and routes to plan", async () => {
    renderWithProviders(<HomePage />);

    expect(
      screen.getByRole("heading", { name: /cual es tu meta/i })
    ).toBeInTheDocument();

    const button = screen.getByRole("button", {
      name: /generar mi plan/i,
    });
    expect(button).toBeDisabled();

    const user = userEvent.setup();
    await user.type(screen.getByRole("textbox"), "Dormir mejor");
    expect(button).toBeEnabled();

    await user.click(button);
    expect(push).toHaveBeenCalledWith("/plan?goal=Dormir%20mejor");
  });

  it("renders the plan view", async () => {
    const ui = await PlanPage({
      searchParams: Promise.resolve({ goal: "Dormir mejor" }),
    });
    renderWithProviders(ui);

    expect(
      screen.getByText(/generado para ti/i)
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: /comenzar plan/i })
    ).toBeInTheDocument();
  });

  it("renders the section view", async () => {
    const ui = await SectionPage({
      params: Promise.resolve({ id: "section-1" }),
      searchParams: Promise.resolve({ goal: "Dormir mejor" }),
    });
    renderWithProviders(ui);

    expect(
      screen.getByText(/episodio analizado/i)
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: /iniciar estudio/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /marcar como completada/i })
    ).toBeInTheDocument();
  });

  it("renders the flashcard session", () => {
    renderWithProviders(<FlashcardsPage />);

    expect(
      screen.getByRole("button", { name: /^lo sabia$/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /^no lo sabia$/i })
    ).toBeInTheDocument();
  });

  it("renders the progress dashboard", () => {
    renderWithProviders(<ProgressPage />);

    expect(
      screen.getByRole("heading", { name: /tu progreso/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /guardar check-in/i })
    ).toBeInTheDocument();
  });
});
