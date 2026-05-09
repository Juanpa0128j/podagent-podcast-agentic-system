"""MCP server definition and tool registration."""

from __future__ import annotations

from fastmcp import FastMCP

from podagent_server.config import get_azure_openai_config
from podagent_server.mcp.tools import ingestion, learnflow, library, retrieval

mcp = FastMCP("podagent")

# Register ingestion tools
mcp.tool()(ingestion.import_episode)
mcp.tool()(ingestion.get_import_status)

# Register library tools
mcp.tool()(library.list_library)
mcp.tool()(library.get_episode)
mcp.tool()(library.get_transcript_window)

# Register retrieval tools
mcp.tool()(retrieval.search_chunks)

# Register LearnFlow tools
mcp.tool()(learnflow.generate_plan)
mcp.tool()(learnflow.generate_section_content)
mcp.tool()(learnflow.answer_with_rag)


def main() -> None:
    """Run the MCP server."""
    get_azure_openai_config()
    mcp.run()


if __name__ == "__main__":
    main()
