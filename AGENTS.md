# AGENTS.md

> Agent-specific guidance for PodAgent.

---

## Project Overview

**PodAgent** — agent-based system for interactive podcast intelligence.

**Current Phase:** Phase 1 MVP (local transcript ingestion only)

- Ingest transcript files (VTT/SRT/markdown)
- RAG Q&A with timestamped citations
- Chat via Next.js + Python MCP server

---

## Repository Structure

```
podagent/
├── apps/
│   ├── server/               # Python MCP server (uv)
│   │   └── src/podagent_server/
│   │       ├── mcp/          # tool registration
│   │       ├── ingestion/    # pipeline, sources, chunking, transcription
│   │       ├── retrieval/    # embeddings, vector store, search
│   │       ├── storage/      # models, repositories
│   │       ├── auth/         # JWT + tier middleware
│   │       └── ui_resources/ # MCP-UI hints
│   └── web/                  # Next.js client (pnpm)
│       └── src/
│           ├── app/          # routes
│           ├── components/   # React components
│           ├── lib/          # supabase, mcp-client
│           └── types/
├── packages/
│   └── shared-types/         # TS types from Pydantic
├── docs/
│   └── podagent-srs.docx.md  # SRS
├── pyproject.toml            # uv workspace root
├── package.json              # pnpm workspace root
└── pnpm-workspace.yaml
```

---

## Technology Stack

| Layer | Tech |
|-------|------|
| Server | Python 3.10+, FastMCP, Pydantic, SQLAlchemy, asyncpg |
| Client | Next.js 15, TypeScript, Tailwind, Vercel AI SDK |
| DB | Supabase (Postgres + pgvector + Auth + Storage) |
| Embeddings | OpenAI `text-embedding-3-small` |

---

## Running

### Server
```bash
cd apps/server
uv sync
uv run python -m podagent_server.mcp.server
```

### Web
```bash
pnpm install
pnpm dev:web
```

---

## Adding Dependencies

```bash
# Python (server)
cd apps/server
uv add package-name

# TypeScript (web)
pnpm --filter web add package-name
```

---

## Key Interfaces

All cross-module deps go through Protocols in `base.py`. Swapping impl = binding change in `config.py`, zero call-site changes.

| Interface | Phase 1 Impl |
|-----------|--------------|
| `SourceAdapter` | `LocalUploadAdapter` |
| `Chunker` | `TokenWindowChunker` |
| `Embedder` | `OpenAIEmbedder` |
| `VectorStore` | `PgVectorStore` |
| `Transcriber` | declared, no impl |

---

*Last updated: May 2026*
