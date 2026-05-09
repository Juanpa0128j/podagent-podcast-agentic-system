/**
 * MCP Apps — component registry.
 *
 * Maps component names (from `_ui.component`) to lazy-loadable React
 * component factories. Add new entries here as new MCP tools get UI hints.
 */

import type { ComponentType } from "react";

// Typed imports — the registry holds factory functions to avoid loading every
// component upfront and to keep bundle splitting possible.
import type { Plan, SectionContent } from "../../types/learnflow";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AnyComponent = ComponentType<any>;

// Synchronous registry for Phase 1 (two components only).
// Replace with dynamic imports when the list grows.
import PlanView from "../../components/learnflow/PlanView";
import SectionView from "../../components/learnflow/SectionView";

export interface RegistryEntry {
  component: AnyComponent;
}

const REGISTRY: Record<string, RegistryEntry> = {
  PlanView: { component: PlanView as AnyComponent },
  SectionView: { component: SectionView as AnyComponent },
};

/**
 * Look up a component by name.
 * Returns `undefined` if the name is not registered.
 */
export function lookupComponent(name: string): RegistryEntry | undefined {
  return REGISTRY[name];
}

/**
 * Returns all registered component names (useful for diagnostics).
 */
export function registeredComponents(): string[] {
  return Object.keys(REGISTRY);
}
