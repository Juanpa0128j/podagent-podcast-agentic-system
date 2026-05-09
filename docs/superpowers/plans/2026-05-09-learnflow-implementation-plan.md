# LearnFlow — Parallel Implementation Plan (Local + Azure OpenAI)

**Date:** 2026-05-09  
**Source spec:** `docs/superpowers/specs/2026-05-09-learnflow-design.md`  
**Goal:** Ship an MVP locally in ~30 minutes using subagent-driven development + TDD.  
**Non-goals:** Auth, persistence, multi-podcast sources, payments.

---

## 0) Working Agreement (5 minutes max)

### Single source of truth
- UX + routes + UI elements must match the spec exactly.
- Avoid adding new pages/modals/filters/animations.

### Local-first
- Unit tests must not call Azure.
- One optional manual “smoke” call to Azure is allowed at the end.

### Shared contract freeze (do this first)
All devs align on these schema contracts and IDs:
- `Plan` JSON shape
- `SectionContent` JSON shape
- `section_id` format (must match ingestion/retrieval IDs)

> Output parsing requirement: tool outputs must be valid JSON matching schema; failures must be handled (retry / validation error).

---

## 1) Local Run Commands

### Server (Python MCP)
```bash
cd apps/server
uv sync
uv run python -m podagent_server.mcp.server
```

### Web (Next.js)
```bash
pnpm install
pnpm dev:web
```

### One-time ingestion (if needed)
- Provide a single command/script to ingest `podcasts/Huberman/*.md` into the vector store.

---

## 2) Azure OpenAI Environment Contract

Define and document the env vars used by the server (final names chosen by Dev A, but must be consistent):

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT_CHAT`
- `AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS` (only if embeddings via Azure)

Rules:
- Fail fast on startup if required vars are missing.
- No secrets committed.

---

## 3) Work Split (3 devs in parallel)

### Dev A — Backend MCP tools + Azure LLM wrapper

**Objective:** Implement MCP tools for LearnFlow using RAG-grounded structured output.

**Deliverables**
- MCP tools:
  - `generate_plan(goal: str) -> Plan`
  - `generate_section_content(section_id: str, goal: str) -> SectionContent`
  - Keep/verify existing `answer_with_rag(question: str, context?: str) -> Answer`
  - `get_episode(episode_id: str) -> Episode` (static lookup)
- Azure OpenAI client wrapper usable via dependency injection and stubbable in tests.
- Pydantic models that mirror the spec schemas.

**TDD checklist (pytest)**
1. **Contract tests (RED):**
   - `generate_plan` returns a Pydantic `Plan` that serializes to the exact JSON shape.
   - `generate_section_content` returns a Pydantic `SectionContent` with `flashcards[]` non-empty.
2. **LLM wrapper unit tests (RED):**
   - Given a fake LLM response (string), parse + validate to model.
   - Invalid JSON triggers retry/validation failure path.
3. **Implementation (GREEN):**
   - Retrieval: embed goal/question → top-K chunks.
   - Prompt: render from templates.
   - Call Azure chat deployment.
   - Parse + validate structured output.

**Subagent prompts**
- “Find existing MCP tool registration pattern + where to add new tools.”
- “Find existing OpenAI/embeddings code and how to swap to Azure OpenAI.”

**Acceptance**
- Running the server locally exposes the tools.
- Unit tests pass without Azure calls.

---

### Dev B — Web routes + UI screens (exact spec)

**Objective:** Replace chat UX with LearnFlow flow across 5 routes.

**Routes to implement**
- `/` GoalInput
- `/plan` PlanView
- `/section/[id]` SectionView
- `/flashcards` FlashcardSession
- `/progress` ProgressDashboard

**Data flow**
- GoalInput “Generar mi plan” → call `generate_plan(goal)` → store in local state → navigate `/plan`.
- SectionView loads `generate_section_content(section_id, goal)` → renders accordions.
- “Iniciar estudio” → navigates to `/flashcards` seeded with flashcards.

**TDD checklist (vitest + RTL)**
1. Route smoke tests (RED): each route renders its required headline + primary CTA.
2. Navigation tests (RED): GoalInput → PlanView.
3. Component tests (RED):
   - PlanView renders phases + DO/DON’T cards.
   - SectionView renders Resumen/Glosario/Flashcards accordions.
   - FlashcardSession shows progress counter + buttons.
4. Implementation (GREEN): build minimal components to satisfy tests.

**Subagent prompts**
- “Find existing Next.js app structure and any existing MCP client helper.”
- “Find Tailwind tokens / design primitives already present; avoid inventing new tokens.”

**Acceptance**
- All 5 routes render and navigate.
- No extra UX beyond the spec.

---

### Dev C — Ingestion/retrieval readiness + local progress + flashcards logic

**Objective:** Ensure local transcripts are ingested and retrievable; implement local-only progress store and flashcard session behavior.

**Deliverables**
- A one-command ingestion entrypoint for `podcasts/Huberman/`.
- Local progress store (React state or Zustand) matching `UserProgress` in spec.
- Flashcard session logic:
  - flip card
  - next card
  - record known/unknown results
  - progress bar state

**TDD checklist**
1. Store tests (RED): actions update immutable state correctly.
2. Flashcard reducer/unit tests (RED):
   - marking known/unknown records result
   - advancing increments index
3. Optional integration test: ingest 1 fixture transcript → retrieval returns at least 1 chunk.

**Subagent prompts**
- “Find ingestion entrypoints and current vector store configuration for local dev.”
- “Find existing state management patterns in web app; match conventions.”

**Acceptance**
- Ingestion can be run locally (documented command).
- Flashcard session updates progress locally (no backend persistence).

---

## 4) Cross-team Interfaces / Handoffs

### Backend → Web
- Tool names + parameter names must match exactly:
  - `generate_plan(goal)`
  - `generate_section_content(section_id, goal)`
- Error envelope: decide one pattern (throw vs `{success:false}`) and keep consistent.

### IDs
- `section_id` must be stable and derivable from ingestion.
- Web must treat IDs as opaque.

---

## 5) Definition of Done (Local)

**Minimum shippable**
- `/` accepts a goal and produces a non-empty plan on `/plan`.
- `/section/[id]` shows summary, glossary, and at least 5 flashcards.
- `/flashcards` runs end-to-end and records known/unknown.
- `/progress` renders using local store data.

**Testing**
- `apps/server`: pytest green; unit tests do not call Azure.
- `apps/web`: vitest green.

**Manual smoke (optional, end-only)**
- One real Azure call to verify deployment/env wiring.

---

## 6) Suggested Execution Order (Fastest path)

1. Dev A defines schemas + tool signatures, pushes contract file/models.
2. Dev B scaffolds routes + placeholder components and wires MCP client calls.
3. Dev C ensures `section_id` scheme + ingestion command exist and implements progress store.
4. Everyone runs local smoke: start server + web, generate plan, open section, run flashcards.
