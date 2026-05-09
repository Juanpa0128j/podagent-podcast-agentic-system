# PodAgent

Agent-based system for interactive podcast intelligence. Current focus: **LearnFlow** — goal-driven study plans grounded in podcast transcripts (Huberman corpus).

## Monorepo Structure

- `apps/server` — Python MCP server (uv, FastMCP)
- `apps/web` — Next.js 15 web client (pnpm)
- `packages/shared-types` — TypeScript types

## LearnFlow MVP

Routes:
- `/` GoalInput
- `/plan` PlanView
- `/section/[id]` SectionView (Resumen / Glosario / Flashcards)
- `/flashcards` FlashcardSession
- `/progress` ProgressDashboard

MCP tools (`apps/server/src/podagent_server/mcp/tools/learnflow.py`):
- `generate_plan(goal)` → `Plan`
- `generate_section_content(section_id, goal)` → `SectionContent`
- `answer_with_rag(question, context?)` → `Answer`

LLM: Azure OpenAI (chat + embeddings). RAG over local Huberman markdown transcripts.

### Agentic UI

- **MCP Apps** (primary): tool responses carry `_ui` hints; `apps/web/src/lib/mcp-apps/` registry maps hints → React components.
- **CopilotKit** (inline Q&A): sidebar across all routes, bridges to `answer_with_rag` via `/api/copilotkit` Azure runtime.

### Web ↔ Server transport

Next.js Route Handler at `apps/web/src/app/api/learnflow/[tool]/route.ts` shells out to the Python tool functions. Falls back to sample fixtures (`apps/web/src/lib/learnflow-sample.ts`) on error.

## Environment

Server (`apps/server`):
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT_CHAT`
- `AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS`

Web (`apps/web`): same vars surfaced for the CopilotKit runtime.

## Quick Start

```bash
# Server deps
cd apps/server && uv sync

# Web deps
pnpm install

# Ingest local Huberman transcripts (one-time)
cd apps/server && uv run python -m podagent_server.ingestion.cli

# Run server + web (separate terminals)
pnpm dev:server
pnpm dev:web
```

## Tests

```bash
# Server
cd apps/server && uv run pytest

# Web unit
cd apps/web && pnpm vitest run

# Web e2e (Playwright)
cd apps/web && pnpm test:e2e
```

## Docs

- `docs/podagent-srs.docx.md` — Software Requirements Specification
- `phase1.md` — System design document
- `docs/superpowers/specs/2026-05-09-learnflow-design.md` — LearnFlow spec
- `docs/superpowers/plans/2026-05-09-learnflow-implementation-plan.md` — Implementation plan
