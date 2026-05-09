# PodAgent

Agent-based system for interactive podcast intelligence.

## Monorepo Structure

- `apps/server` — Python MCP server (uv)
- `apps/web` — Next.js web client (pnpm)
- `packages/shared-types` — TypeScript types

## Phase 1 MVP

- Local transcript file ingestion (VTT/SRT/markdown)
- RAG-based Q&A with citations
- Chat UI

## Quick Start

```bash
# Install Python deps + server
cd apps/server && uv sync

# Install Node deps + web
pnpm install

# Run both (separate terminals)
pnpm dev:server
pnpm dev:web
```

## Docs

- `docs/podagent-srs.docx.md` — Software Requirements Specification
- `phase1.md` — System design document
