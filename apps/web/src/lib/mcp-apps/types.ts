/**
 * MCP Apps — shared types for the UI hint envelope.
 *
 * The server wraps `generate_plan` and `generate_section_content` responses in
 * this envelope so the renderer can dispatch to the correct React component
 * without hard-coded tool names on the client.
 */

export interface UIHint {
  /** Registered component name in the registry (e.g. "PlanView"). */
  component: string;
  /** Schema version — increment when the component's data contract changes. */
  version: number;
}

/**
 * Envelope returned by MCP-aware tool calls.
 * `T` is the typed payload that the chosen component expects.
 */
export interface MCPAppResponse<T = unknown> {
  _ui: UIHint;
  data: T;
}
