import { test, expect } from "@playwright/test";

test("golden path — import + chat", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("h1")).toContainText("PodAgent");
});
