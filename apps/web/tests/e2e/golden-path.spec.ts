import { test, expect } from "@playwright/test";

/**
 * LearnFlow golden-path e2e.
 *
 * No real Azure/MCP backend needed — the app falls back to samplePlan /
 * sampleSection fixtures when the API route fails.
 *
 * Requires dev server running on http://localhost:3000 (`pnpm dev`).
 */

test("LearnFlow golden path — goal → plan → section → flashcards → progress", async ({
  page,
}) => {
  // ── 1. Home: GoalInput ────────────────────────────────────────────────────
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText(
    "Cual es tu meta?"
  );

  await page
    .getByPlaceholder("Ejemplo: Quiero mejorar mi concentracion")
    .fill("Mejorar mi concentracion");

  await page.getByRole("button", { name: /Generar mi plan/i }).click();

  // ── 2. Plan (/plan) ───────────────────────────────────────────────────────
  await page.waitForURL(/\/plan/);

  // Heading renders (uses goal param or samplePlan.goal as fallback)
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();

  // Phase names from samplePlan
  await expect(
    page.getByText("Fase 1: Base neurobiologica", { exact: false })
  ).toBeVisible();
  await expect(
    page.getByText("Fase 2: Consolidacion", { exact: false })
  ).toBeVisible();

  // DO / DON'T card headings (rendered as h3 inside the cards)
  await expect(page.getByRole("heading", { name: /DO/i }).first()).toBeVisible();

  // ── 3. Section (/section/focus-101) ──────────────────────────────────────
  // PlanView shows section_id text in <article> cards but wraps no <a>.
  // Navigate directly — same as clicking a deep link from the plan.
  await page.goto("/section/focus-101");

  await expect(
    page.getByRole("link", { name: /Volver al plan/i })
  ).toBeVisible();

  // "Resumen" accordion is open by default (has `open` attribute)
  await expect(page.getByText("Resumen").first()).toBeVisible();
  await expect(
    page.getByText("ciclos de alerta", { exact: false })
  ).toBeVisible();

  // Other accordion summaries visible (collapsed)
  await expect(page.getByText("Glosario")).toBeVisible();
  await expect(page.getByText("Flashcards")).toBeVisible();

  // ── 4. Flashcard session (/flashcards) ───────────────────────────────────
  await page.getByRole("link", { name: /Iniciar estudio/i }).click();
  await page.waitForURL(/\/flashcards/);

  // Progress counter e.g. "1/5"
  const counter = page.getByText(/\d+\/\d+/);
  await expect(counter).toBeVisible();
  const initialCounterText = await counter.textContent();

  // Front face shows "Pregunta"
  await expect(page.getByText("Pregunta", { exact: false }).first()).toBeVisible();

  // Flip the card → back face shows "Respuesta"
  await page.getByRole("button", { name: /Voltear tarjeta/i }).click();
  await expect(page.getByText("Respuesta", { exact: false })).toBeVisible();

  // Mark as known → advances counter (or ends session)
  await page.getByRole("button", { name: /Lo sabia/i }).click();

  // Counter text should change, or session finishes with "Sesion finalizada"
  const counterStillVisible = await counter.isVisible().catch(() => false);
  if (counterStillVisible) {
    const newText = await counter.textContent();
    expect(newText).not.toBe(initialCounterText);
  } else {
    await expect(
      page.getByText("Sesion finalizada", { exact: false })
    ).toBeVisible();
  }

  // ── 5. Progress (/progress) ───────────────────────────────────────────────
  await page.goto("/progress");

  await expect(page.getByRole("heading", { level: 1 })).toContainText(
    "Tu Progreso"
  );
  await expect(page.getByText("Cada paso suma", { exact: false })).toBeVisible();
  await expect(page.getByText("Plan General", { exact: false })).toBeVisible();
});
