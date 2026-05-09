"use client";

/**
 * MCP Apps — generic renderer.
 *
 * Receives a `_ui` hint and typed `data`, looks up the component in the
 * registry, and renders it by spreading `data` as props.
 *
 * Unknown component names render a diagnostic fallback instead of crashing.
 */

import type { UIHint } from "./types";
import { lookupComponent, registeredComponents } from "./registry";

interface MCPAppRendererProps {
  hint: UIHint;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: Record<string, any>;
}

export default function MCPAppRenderer({ hint, data }: MCPAppRendererProps) {
  const entry = lookupComponent(hint.component);

  if (!entry) {
    return (
      <div
        role="alert"
        className="rounded-md border border-red-300 bg-red-50 p-4 text-sm text-red-700"
      >
        <strong>MCPAppRenderer:</strong> unknown component &quot;{hint.component}
        &quot;. Registered: {registeredComponents().join(", ")}.
      </div>
    );
  }

  const Component = entry.component;
  return <Component {...data} />;
}
