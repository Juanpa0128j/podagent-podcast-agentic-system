# LearnFlow — Design Document

**Date:** 2026-05-09  
**Status:** Approved  
**Scope:** Pivot from PodAgent (RAG chat) to LearnFlow (goal-driven learning plans from podcasts)

---

## 1. Product Overview

LearnFlow is a goal-driven web application that generates personalized, actionable learning plans from scientific podcast content (Huberman Lab as Phase 1 source). The user defines a learning goal, and the system generates a complete plan — phases, DO's, DON'Ts, timeline, and mapped podcast episodes — using RAG-grounded LLM structured output.

**Core value proposition:** Turn passive podcast consumption into active, structured learning with flashcards, progress tracking, and check-ins.

**What stays from PodAgent:**
- Python MCP server (FastMCP, Pydantic, SQLAlchemy)
- RAG pipeline (ingestion, chunking, embedding, vector store)
- Next.js 15 + TypeScript + Tailwind frontend
- Monorepo structure (uv + pnpm)

**What changes:**
- Product experience: chat → structured learning flow
- New MCP tools for structured LLM output (`generate_plan`, `generate_section_content`)
- New screens: GoalInput, PlanView, SectionView, FlashcardSession, ProgressDashboard
- Design system: Serene Intellect (from Stitch)

---

## 2. Screen Flow & Navigation

| Route | Screen | Key Elements |
|---|---|---|
| `/` | **GoalInput** | Centered textarea, "METAS POPULARES" chips (Concentracion, Dormir mejor, Mas energia, Reducir estres), "Generar mi plan" button |
| `/plan` | **PlanView** | Timeline with phases (locked/unlocked), DO's card (green border), DON'Ts card (red border), Material cards, "Comenzar plan" button |
| `/section/[id]` | **SectionView** | Episode header, Resumen (collapsible accordion), Glosario, Flashcards preview grid, "Iniciar estudio" button, "Marcar como completada" |
| `/flashcards` | **FlashcardSession** | Full-screen centered card with 3D flip, progress bar (12/50), "Lo sabia" (green) / "No lo sabia" (red) buttons |
| `/progress` | **ProgressDashboard** | Progress bar (42%), streak counter (14 dias), plan steps checklist, knowledge stats (Dominados/Por Repasar), Check-in Rapido |

**Navigation:**
- Top nav tabs: Plan | Estudio | Progreso
- Logo "LearnFlow" top-left
- Notification bell + avatar top-right
- Bottom CTA buttons on Plan and Section screens

---

## 3. Design System — Serene Intellect

Reference: `docs/ui-reference/serene_intellect/DESIGN.md`

### Colors
| Token | Hex | Usage |
|---|---|---|
| Primary | `#00288e` | Buttons, active states, nav |
| Primary container | `#1e40af` | Button backgrounds |
| Secondary | `#006c4a` | Success, completion, "Lo sabia" |
| Tertiary | `#611e00` | Warning, "No lo sabia", review chips |
| Error | `#ba1a1a` | Errors |
| Surface | `#f8f9ff` | Page background |
| On-surface | `#0b1c30` | Primary text |
| Surface container | `#ffffff` | Cards |

### Typography
- Font: Inter
- Headlines: bold, tight tracking (-0.02em to -0.01em)
- Body: 400 weight, 1.5-1.6 line height
- Labels: medium weight, increased letter spacing

### Spacing
- Base: 8px
- Mobile margins: 20px
- Section gap: 32px
- Gutter: 16px
- Button height: 56px (mobile accessibility)

### Shapes
- Cards: 16px radius (`rounded-lg`)
- Buttons/inputs: 8px radius (`rounded-md`)
- Chips/badges: full pill

### Elevation
- Cards: subtle shadow (2px blur)
- Flashcards: pronounced shadow (`0 10px 20px rgba(0,0,0,0.04)`) for floating feel
- Nav: 4px backdrop blur

---

## 4. Architecture

### Stack
| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Backend | Python MCP server (FastMCP, Pydantic) |
| LLM | OpenAI GPT-4o (structured output) |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector Store | PgVector (existing) |
| Data | 82 Huberman transcripts (local markdown) |
| Agentic UI | MCP Apps (primary) |

### Architecture Diagram
```
┌──────────────────┐      MCP      ┌──────────────────────────┐
│   Next.js Web    │◄─────────────►│   Python MCP Server      │
│   (LearnFlow)    │   tools       │   - generate_plan        │
│                  │               │   - generate_section_    │
│  /  /plan        │               │     content              │
│  /section/[id]   │               │   - answer_with_rag      │
│  /flashcards     │               │   - get_episode          │
│  /progress       │               │                          │
└──────────────────┘               └──────────┬───────────────┘
                                              │
                                     ┌────────▼────────┐
                                     │   RAG Pipeline  │
                                     │  - Ingestion    │
                                     │  - Chunking     │
                                     │  - Embedding    │
                                     │  - Vector Store │
                                     └─────────────────┘
```

### MCP Tool Design

**`generate_plan(goal: string) -> Plan`**
1. Embed the user's goal
2. Retrieve top-K relevant podcast episodes/sections from vector store
3. Call LLM with goal + retrieved chunks + structured output schema
4. Return `Plan` JSON

**`generate_section_content(section_id: string, goal: string) -> SectionContent`**
1. Retrieve specific section transcript from vector store
2. Call LLM with section text + user goal + structured output schema
3. Return `SectionContent` JSON (summary, glossary, flashcards)

**`answer_with_rag(question: string, context?: string) -> Answer`**
1. Embed question
2. Retrieve top-K chunks
3. Call LLM with question + chunks
4. Return answer with citations

**`get_episode(episode_id: string) -> Episode`**
- Static lookup from ingested podcast metadata

---

## 5. Data Models

### Podcast (pre-ingested)
```typescript
interface Podcast {
  id: string;
  title: string;
  description: string;
  duration: string;
  sections: Section[];
}

interface Section {
  id: string;
  title: string;
  order: number;
  transcript: string;
  key_concepts: string[];
}
```

### Plan (generated by LLM)
```typescript
interface Plan {
  goal: string;
  estimated_duration: string;
  phases: Phase[];
  dos: ActionItem[];
  donts: ActionItem[];
  relevant_content: ContentMapping[];
}

interface Phase {
  name: string;
  duration: string;
  steps: Step[];
}

interface Step {
  action: string;
  when: string;
  duration: string;
  why: string;
}

interface ActionItem {
  action: string;
  when?: string;
  why: string;
}

interface ContentMapping {
  section_id: string;
  reason: string;
}
```

### SectionContent (generated by LLM)
```typescript
interface SectionContent {
  section_id: string;
  summary: string;
  key_points: string[];
  glossary: GlossaryTerm[];
  flashcards: Flashcard[];
}

interface GlossaryTerm {
  term: string;
  definition: string;
}

interface Flashcard {
  id: string;
  question: string;
  answer: string;
}
```

### UserProgress (local state — MVP only)
Stored in React state or Zustand. Not persisted to backend in MVP.

```typescript
interface UserProgress {
  goal: string;
  plan_id: string;
  completed_steps: string[];
  completed_sections: string[];
  flashcard_results: Record<string, "known" | "unknown">;
  checkin_responses: CheckinResponse[];
  streak: number;
}

interface CheckinResponse {
  date: string;
  question: string;
  answer: boolean;
}
```

---

## 6. UI Components

### GoalInput (`/`)
- Centered layout with sparkle icon above headline
- Headline: "Cual es tu meta?" (headline-lg)
- Subtitle: body text explaining the system
- Textarea: large, rounded-lg, placeholder with example goal
- Primary button: full-width, 56px height, "Generar mi plan" with sparkle icon
- Chip group: "METAS POPULARES" label + 4 pill chips
- Footer: LearnFlow logo, Support/Privacy/Terms links

### PlanView (`/plan`)
- Badge: "Generado para ti"
- Headline: Plan title (e.g., "Mejorar Concentracion")
- Description: plan subtitle
- **Timeline:** vertical with dots, phase names, descriptions. Locked phases show lock icon + "Se desbloquea al completar fases previas"
- **DO's card:** green left border, checkmark icon, action + when + why
- **DON'Ts card:** red left border, X icon, action + why
- **Material cards:** image thumbnail, title, subtitle, duration badge
- Bottom CTA: "Comenzar plan" with arrow icon

### SectionView (`/section/[id]`)
- Back link: "Volver al plan"
- Badge: "Episodio Analizado"
- Headline: section title
- Description: episode summary paragraph
- **Resumen accordion:** collapsible, bullet points with icons
- **Glosario accordion:** collapsible, term list
- **Flashcards accordion:** collapsible, preview grid of 2 cards
- CTA: "Iniciar estudio" (navigates to flashcard session)
- Secondary CTA: "Marcar como completada"

### FlashcardSession (`/flashcards`)
- Header: topic name (left), progress "12/50" + bar (center), close X (right)
- **Flashcard:** large centered card, 32px padding, headline-md typography
  - Front: question + "PREGUNTA" label
  - Tap/click → 3D flip animation → back: answer + "RESPUESTA" label
- **Action buttons:** two full-width buttons below card
  - Left: "No lo sabia" (tertiary/warning color, thumbs-down icon)
  - Right: "Lo sabia" (secondary/success color, thumbs-up icon)

### ProgressDashboard (`/progress`)
- Headline: "Tu Progreso"
- Subtitle: encouragement text
- **Plan General card:** progress bar (42% / Meta: 100%), current module
- **Streak card:** flame icon + day count + "Dias seguidos"
- **Pasos del Plan card:** checklist with radio buttons, completed items strikethrough
- **Conocimiento card:** "Dominados" count (green dot) + "Por Repasar" count (orange dot) + segmented bar
- **Check-in Rapido card:** blue background, 2 question cards with X/check buttons, "Guardar Check-in" button

---

## 7. LLM Prompts

### Plan Generation Prompt
```
You are a science-based wellness coach. The user has this goal: {goal}.
You have access to these podcast episodes/sections: {retrieved_chunks}.

Generate a structured learning plan in JSON format:
- phases: array of phases with name, duration, and steps (each step has action, when, duration, why)
- dos: array of positive actions with when and why
- donts: array of things to avoid with why
- relevant_content: array of section references with reason for relevance

The plan should be practical, science-based, and directly grounded in the provided podcast content.
```

### Section Content Prompt
```
Generate educational content for this podcast section. The user's goal is: {goal}.
The section transcript is: {transcript}.

Generate in JSON:
- summary: focused on what's relevant to the user's goal (2-3 sentences)
- key_points: 3-5 bullet points
- glossary: 3-5 difficult terms with simple definitions
- flashcards: 5-10 question/answer pairs for active recall
```

---

## 8. RAG Integration Points

1. **Plan Generation:** Goal embedding → retrieve top-K episodes/sections → LLM generates plan grounded in retrieved content
2. **Section Content:** Section ID → retrieve full section transcript → LLM generates summary, glossary, flashcards
3. **Inline Q&A:** Within any section, user asks question → embed → retrieve chunks → LLM answers with citations

All three use the existing ingestion pipeline, chunker, embedder, and vector store unchanged.

---

## 9. What to Keep vs Replace

### Keep (from PodAgent)
- `apps/server/` Python MCP server structure
- Ingestion pipeline (`ingestion/`, `chunking/`, `transcription/`)
- Retrieval layer (`retrieval/`, `embeddings/`, `vector_store/`)
- Storage models and repositories
- CI workflow
- Dev container and Makefile

### Replace
- `apps/web/src/app/` pages → new LearnFlow screens
- `apps/web/src/components/` → new LearnFlow components
- `apps/server/src/podagent_server/mcp/tools/` → add new tools, remove old ones
- `apps/server/src/podagent_server/ui_resources/` → update hints
- AGENTS.md → update to LearnFlow branding

### Add
- `apps/web/src/components/learnflow/` — new component directory
- `apps/web/src/lib/progress-store.ts` — local state for progress
- `apps/server/src/podagent_server/mcp/tools/learnflow/` — new MCP tools
- `apps/server/src/podagent_server/prompts/` — LLM prompt templates
- Podcast ingestion script for Huberman transcripts (run once to populate vector store)
- `apps/web/src/lib/mcp-apps/` — MCP Apps renderer (maps tool output JSON to React components)

---

## 10. Out of Scope (MVP)

- Authentication (anonymous usage)
- Community features
- External integrations beyond OpenAI
- Multi-source podcasts (Huberman only for Phase 1)
- Mobile app (web only)
- CopilotKit integration (MCP Apps only for MVP; CopilotKit for inline Q&A in future)
- Payments/freemium

---

*Design approved. Ready for implementation planning.*
