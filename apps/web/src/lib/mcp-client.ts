"""MCP client singleton.

Connects to Python MCP server, forwards user JWT.
Phase 1 stub — full impl after server contract stabilizes.
"""

export async function createMCPClient(jwt: string) {
  // TODO: wire @modelcontextprotocol/sdk client
  console.log("MCP client stub", jwt);
  return {
    callTool: async (name: string, args: Record<string, unknown>) => {
      return { content: [{ type: "text", text: "stub" }] };
    },
  };
}
