# PodAgent — System Design

**Scope:** Full architectural skeleton across all three SRS phases, with **Phase 1 (MVP)** specified in implementation detail and later phases described as extension points behind stable interfaces.

**Status:** Draft for team review
**Date:** 2026-05-08
**Companion document:** `podagent-srs.docx.md` (full SRS)

---

## 1. Goals & Scope

PodAgent is an agent-based system for interactive podcast intelligence. The Phase 1 deliverable is: a user can ingest a podcast episode (from Podcast Index or by uploading a transcript file), then chat with it through a web UI that streams answers grounded in cited transcript chunks, with clickable timestamps that open the original audio.

This document is the source of truth for module boundaries and interfaces. Implementation plans for individual features are produced separately.

### Design principles

- **Modular with explicit interfaces.** Every cross-module dependency goes through a Protocol/ABC. Concrete implementations are injected at startup. Swapping a provider is a binding change, not a refactor.
- **Tools-first contract.** The MCP tool surface is the canonical contract between server and any client (web app, Claude Desktop, future CLI). Frontends are interchangeable; the contract is not.
- **Primitives over conveniences.** Server exposes low-level primitives. Higher-level behaviors (summarization, comparative analysis) are composed by the client's agent loop.
- **Server holds no LLM keys.** Hosts run their own LLM loops with their own credentials. The server stays portable across MCP hosts.

---

## 2. Architecture Overview

The system has three deploy units:

1. **MCP Server (Python)** — exposes podcast intelligence as Model Context Protocol tools. Owns ingestion, retrieval, and storage. Stateless with respect to LLM providers.
2. **Web Client (Next.js)** — chat UI plus library/episode views. Runs the LLM agent loop client-side via Vercel AI SDK, calling the MCP server's tools.
3. **Inngest (managed)** — runs ingestion jobs (transcription, chunking, embedding) asynchronously.

External managed dependencies: Supabase (Postgres + pgvector + Auth + Storage), Anthropic (LLM), OpenAI (embeddings), Deepgram (STT), Podcast Index (catalog), Stripe (Phase 2), LangSmith (tracing), Sentry (errors).

```
┌────────────────────┐         ┌─────────────────────────┐
│   Web Client       │◀───────▶│   MCP Server (Python)   │
│   (Next.js,        │  MCP    │   FastMCP, HTTP/SSE     │
│   Vercel AI SDK)   │         │                         │
└─────────┬──────────┘         └───────────┬─────────────┘
          │                                │
          ▼                                ▼
   Anthropic / OpenAI               Supabase (Postgres,
   (host-side LLM loop)             pgvector, Auth, Storage)
                                          ▲
                                          │
                              ┌───────────┴─────────────┐
                              │   Inngest workers       │
                              │   (ingestion pipeline)  │
                              └─────────────────────────┘
                                          │
                                          ▼
                          Podcast Index / Deepgram / OpenAI embeddings
```

The MCP server is the single source of truth for podcast data and the canonical contract surface. Any MCP-compatible host can drive it without code changes.

---

## 3. Data Flow

### Ingestion path

1. User submits a Podcast Index episode ID or uploads a transcript file (markdown with optional `[hh:mm:ss]` markers, or VTT/SRT).
2. Web client calls `import_episode` MCP tool; server enqueues an Inngest job and returns `{job_id}` immediately.
3. Inngest worker:
   - Resolves the source via the relevant `SourceAdapter`.
   - For audio: downloads MP3, runs Deepgram STT.
   - For uploaded transcripts: parses directly, no STT needed.
   - Chunks the transcript with overlapping windows (500–1000 tokens).
   - Embeds chunks via OpenAI `text-embedding-3-small`.
   - Writes episode + chunks + embeddings to Supabase.
4. Status is visible at any time via `get_import_status(job_id)`.

### Query path

1. User types a question in the web client.
2. Vercel AI SDK runs the agent loop with Claude Sonnet 4.6, exposing the MCP server's tools through `experimental_createMCPClient`.
3. The model calls `search_chunks` (and others as needed), receives ranked chunks with episode metadata and timestamps.
4. The model generates a streamed response with inline citations.
5. Citation components render in the UI as the response streams; clicking one opens an embedded player seeked to `ts_start`.

---

## 4. Component Boundaries — MCP Server

```
apps/server/podagent_server/
├── mcp/                    # MCP protocol surface, tool registration, transport
│   └── tools/              # ingestion.py, library.py, retrieval.py
├── ingestion/
│   ├── sources/            # SourceAdapter interface + podcastindex/, local_upload/
│   ├── transcription/      # Transcriber interface + deepgram/, whisper/, assemblyai/
│   ├── chunking/           # Chunker interface + token_window/
│   └── pipeline.py         # source → transcript → chunks → embed → store
├── retrieval/
│   ├── embeddings/         # Embedder interface + openai/, voyage/
│   ├── vector_store/       # VectorStore interface + pgvector/
│   └── search.py           # vector + metadata hybrid search
├── storage/
│   ├── repositories/       # EpisodeRepo, ChunkRepo, JobRepo, UserRepo, UsageRepo
│   └── models.py           # Pydantic + SQLAlchemy
├── jobs/                   # Inngest function definitions
├── ui_resources/           # MCP-UI renderers (citation_card, import_progress)
├── auth/                   # Supabase JWT verification, tier middleware
└── config.py
```

### Key interfaces

All interfaces are Python `Protocol` or `ABC`. Implementations live in subpackages and are wired in `config.py`.

| Interface | Methods | Phase 1 impls | Future impls |
|-----------|---------|---------------|--------------|
| `SourceAdapter` | `fetch_metadata(ref)`, `fetch_audio_or_transcript(episode)` | `PodcastIndexAdapter`, `LocalUploadAdapter` | `YouTubeAdapter` (when proxy available), `RSSAdapter` |
| `Transcriber` | `transcribe(audio_url) → TranscriptSegments` | `DeepgramTranscriber` | `WhisperTranscriber`, `AssemblyAITranscriber` |
| `Chunker` | `chunk(transcript) → list[Chunk]` | `TokenWindowChunker` | semantic chunkers |
| `Embedder` | `embed(texts) → list[vector]` | `OpenAIEmbedder` | `VoyageEmbedder` |
| `VectorStore` | `upsert(chunks)`, `search(query_vec, filters, k)` | `PgVectorStore` | `PineconeStore`, `WeaviateStore` |
| Repos | standard CRUD | `Supabase*Repo` | — |

Adding a new ingestion source, STT provider, embedding model, or vector store is a new implementation of one interface and one binding change. No call sites change.

---

## 5. Tool Surface (MCP)

Tools are primitives. The web client (and any MCP host) compose them into higher-level behaviors. Generation tools (summarize, extract highlights) deliberately do **not** exist server-side — the client composes them from `get_transcript_window` plus its own LLM.

### Phase 1 tools

**Ingestion**
- `import_episode(source: "podcastindex" | "upload", ref: string) → {job_id}`
- `get_import_status(job_id) → {state, progress, episode_id?, error?}` — returns `_ui` hint for progress widget.

**Library**
- `list_library() → [Episode]`
- `get_episode(episode_id) → {metadata, transcript_url}`
- `get_transcript_window(episode_id, start_ts, end_ts) → [Chunk]`

**Retrieval**
- `search_chunks(query, scope, k=8, filters?) → [{chunk, episode_id, ts_start, ts_end, score}]` — returns `_ui` hint for citation card.

`scope` selects the search universe: `{type: "episode", id}`, `{type: "podcast", id}`, or `{type: "library"}`.

### Phase 2 tools (declared, implemented later)

- `import_series(podcast_id) → {job_id}`
- `search_catalog(query) → [{podcast, episodes}]`
- `search_topics(query, scope) → [{topic, episodes, occurrences}]`
- `generate_clip(episode_id, ts_range) → {share_url}`

### Phase 3 extension points (interfaces declared, no implementation)

- `build_timeline(topic, scope)`
- `query_knowledge_graph(entity)`
- `compare_speakers(speakers, topic)`
- `subscribe_briefing(podcast_id, cadence)`

### Auth & tier context

All tools accept an implicit auth context — the Supabase JWT is sent on the MCP transport headers. A middleware in `auth/` validates the token, loads the user, and applies tier limits before dispatching to the tool body.

### UI resource hints (`_ui`)

Phase 1 ships UI hints on two tools: `search_chunks` (citation card) and `get_import_status` (progress widget). All tools return structured JSON regardless. Hosts that ignore `_ui` (programmatic consumers) work on the JSON; hosts that render it (Claude Desktop, web client) get rich widgets. Additional hints can be added later without breaking consumers.

---

## 6. Storage Schema (Supabase)

All tables are RLS-protected on `user_id = auth.uid()`.

| Table | Purpose |
|-------|---------|
| `users` | Synced from `auth.users`. |
| `subscriptions` | Stripe subscription state, current tier. *(Phase 2 wiring)* |
| `usage_daily` | Query counts, episodes-indexed counts (for tier enforcement). |
| `podcasts` | Podcast-level metadata (title, source, external IDs). |
| `episodes` | Episode metadata, status (`pending|processing|ready|failed`), transcript URL in Storage. |
| `chunks` | Chunk text, `ts_start`, `ts_end`, speaker, embedding `vector(1536)`, FK to episode. |
| `jobs` | Inngest job tracking (id, type, state, progress, error). |
| `conversations`, `messages` | Chat history for registered users. |

Vector index: `ivfflat` on `chunks.embedding`. Metadata indexes: `(user_id, episode_id)`, `(user_id, podcast_id)`.

Audio files (when downloaded for STT) live in Supabase Storage under `audio/{user_id}/{episode_id}.mp3` with a TTL cleanup job.

---

## 7. Web Client

**Stack:** Next.js 15 (App Router), TypeScript, Tailwind, shadcn/ui, Vercel AI SDK, `@modelcontextprotocol/sdk` client.

The agent loop runs in a Next.js server route handler that:

1. Authenticates the user via Supabase.
2. Creates an MCP client connected to the Python server, forwarding the user's JWT.
3. Calls `streamText` with Claude Sonnet 4.6 and the MCP tool registry.
4. Streams text + tool results to the browser via `useChat()`.

### Views

| View | Purpose |
|------|---------|
| Landing | Marketing, sign-in, "import your first podcast" entry. |
| Library | List of imported episodes with status. |
| Chat | Main view. Scope selector + chat input. Citations and player render inline. |
| Episode Detail | Metadata, full transcript with timestamp anchors, generated summary, highlights. |
| Account | Profile, subscription, usage. |

### Citations and player

Citations render as React components inline as `search_chunks` results stream in. Clicking a citation opens an embedded player (audio for Podcast Index sources, link-out for Spotify) seeked to `ts_start`. The same data, when viewed in Claude Desktop, renders via the `_ui` resource hint without any client-side code.

---

## 8. Cross-Cutting Concerns

### Authentication

Supabase Auth with anonymous sessions enabled. Anonymous users get a JWT immediately; on signup the same `user_id` carries forward, preserving library and history. RLS enforces per-user isolation at the database level. The MCP server validates JWTs via Supabase's JWKS on every request.

### Tier enforcement

A middleware in `auth/` runs before every tool dispatch:

1. Reads the `user_id` from the validated JWT.
2. Queries `usage_daily` and `subscriptions`.
3. Rejects over-limit calls with a structured error (`{code: "tier_limit_exceeded", limit, used, upgrade_url}`) which the web client maps to an upgrade CTA.

Phase 1 ships the middleware with effectively unlimited limits. Phase 2 wires Stripe webhooks and tightens limits per the SRS table.

### Observability

- **LangSmith** traces the agent loop end-to-end. Web client uses Vercel AI SDK's `AISDKExporter`; Python uses `@traceable` on tool bodies and pipeline stages. Retrieval scores, chunk IDs, and tool inputs/outputs are logged.
- **Sentry** captures unhandled exceptions on both the Next.js client (including frontend crashes) and the Python server.

### Error handling

Ingestion failures retry up to 3 times with exponential backoff (per NFR-08). After exhaustion the job is marked failed and surfaced via `get_import_status`. Tool errors return structured `{code, message, retryable}` so the agent can react appropriately rather than hallucinate.

### Hallucination guard

The chat system prompt requires the model to answer only from `search_chunks` results and to explicitly say it does not know when retrieval is empty. Citations are mandatory; the UI grays out responses without any.

### Security

- All secrets in environment variables (Render, Vercel, Inngest secret managers). None in source.
- Supabase RLS is the primary tenancy boundary.
- Rate limiting at the MCP server transport layer (per-IP and per-user).
- HTTPS/TLS everywhere.
- No user-supplied URLs are fetched without allowlist validation (Podcast Index endpoints only).

---

## 9. Repository Layout

Monorepo with pnpm + uv workspaces:

```
podagent/
├── apps/
│   ├── server/             # Python MCP server (uv)
│   └── web/                # Next.js client (pnpm)
├── packages/
│   └── shared-types/       # TS types generated from Pydantic schemas
├── research/               # existing validation scripts
├── docs/
└── phase1.md               # this document
```

A CI step generates TypeScript types from the server's Pydantic schemas and fails on drift. This keeps the MCP tool contract in sync between the two languages.

---

## 10. Hosting

| Component | Host |
|-----------|------|
| Web (Next.js) | Vercel |
| MCP Server (Python) | Render |
| Background jobs | Inngest (managed) |
| Database / Auth / Storage | Supabase (managed) |
| LLM | Anthropic API |
| Embeddings | OpenAI API |
| STT | Deepgram API |
| Catalog | Podcast Index API |
| Tracing | LangSmith |
| Errors | Sentry |
| Payments (Phase 2) | Stripe |

---

## 11. Testing Strategy

Coverage minimum **80%**, TDD for new features.

### Backend (pytest)

- **Unit tests:** every interface implementation tested against in-memory fakes for its dependencies.
- **Integration tests:** `pipeline.py` end-to-end with fakes for external APIs; one slow suite hits a real Supabase test project and real Deepgram on small audio fixtures.
- **MCP tool tests:** spin up the server in-process, drive each tool through a real MCP client, assert schema and behavior.
- **Fixtures:** golden transcript samples in `tests/fixtures/`.

### Frontend (Vitest + Playwright)

- **Unit:** components (citation card, player embed, scope selector, chat composer) — Vitest + React Testing Library.
- **Integration:** route handlers with mocked MCP client.
- **End-to-end:** Playwright covers the golden path — import episode → ask question → click citation → player seeks to timestamp.

### Contract

Generated TS types from Pydantic; CI fails on drift between the server schemas and the web client's expectations.

---

## 12. Phasing & Extension Points

### Phase 1 (MVP) — this document

- Ingestion: Podcast Index + local transcript upload.
- Q&A with citations and timestamp playback.
- Library and episode detail views.
- Anonymous sessions + Google OAuth via Supabase.
- Tier middleware (stub limits).
- UI hints: citation card, import progress.

### Phase 2

- `import_series`, `search_catalog`, `search_topics`, `generate_clip`.
- Stripe billing + real tier enforcement.
- Speaker diarization (Deepgram supports natively; turn on and propagate to schema).
- Multi-level summarization (composed client-side using `get_transcript_window` + LLM).

### Phase 3

New tool implementations behind already-declared interfaces — `build_timeline`, `query_knowledge_graph`, `compare_speakers`, `subscribe_briefing`. Each gets its own design doc.

### Adding capability later

| Capability | Change required |
|------------|-----------------|
| New ingestion source | One new `SourceAdapter` impl + binding |
| New STT provider | One new `Transcriber` impl + binding |
| New vector store | One new `VectorStore` impl + binding |
| New LLM | Host-side change only; server unchanged |
| New MCP host | None; server is host-agnostic |

---

## 13. Risks & Mitigations

| Risk | Mitigation in this design |
|------|---------------------------|
| Podcast Index / Spotify API or ToS changes | `SourceAdapter` interface; swap implementations without touching the pipeline. |
| LLM cost overruns | Tier middleware enforces per-user query caps; client uses smaller models (Haiku) for non-chat tasks like summarization. |
| Hallucination | Strict RAG prompt, mandatory citations, empty-retrieval fallback, structured tool errors. |
| Transcript quality | `Transcriber` interface allows swapping providers; users can re-run ingestion with a different transcriber. |
| Inngest or Render outage | Retries built in; status surfaced to user; degraded mode (queries still work on already-ingested content). |
| YouTube cloud-IP blocking (known issue) | Out of scope for Phase 1; revisit when paid residential proxy is justified. |
| Vendor lock-in (Supabase, Anthropic, OpenAI, Deepgram) | All accessed through interfaces or thin adapters; Phase 1 picks defaults but doesn't bake them into call sites. |

---

## 14. Open Questions / Deferred

The following are intentionally deferred to implementation planning, not architectural concerns:

- Exact chunk size and overlap tuning (start at 750 tokens / 100 token overlap; tune empirically).
- Specific Render service tier and cold-start handling.
- Email provider for podcast briefings (Phase 3).
- Final pricing tiers (TBD-05 in SRS).
- Project name (TBD-06 in SRS).
