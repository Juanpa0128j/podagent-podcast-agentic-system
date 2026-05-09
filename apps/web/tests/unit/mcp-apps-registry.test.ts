import { describe, expect, it } from "vitest";
import { lookupComponent, registeredComponents } from "../../src/lib/mcp-apps/registry";

describe("MCP Apps registry", () => {
  it("returns entry for PlanView", () => {
    const entry = lookupComponent("PlanView");
    expect(entry).toBeDefined();
    expect(typeof entry?.component).toBe("function");
  });

  it("returns entry for SectionView", () => {
    const entry = lookupComponent("SectionView");
    expect(entry).toBeDefined();
    expect(typeof entry?.component).toBe("function");
  });

  it("returns undefined for unknown component name", () => {
    const entry = lookupComponent("NonExistentWidget");
    expect(entry).toBeUndefined();
  });

  it("registeredComponents includes PlanView and SectionView", () => {
    const names = registeredComponents();
    expect(names).toContain("PlanView");
    expect(names).toContain("SectionView");
  });
});
