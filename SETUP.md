# PodAgent — Developer Setup

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | [uv](https://docs.astral.sh/uv/getting-started/installation/) manages Python automatically |
| Node.js | 22 | [nvm](https://github.com/nvm-sh/nvm) or [fnm](https://github.com/Schniz/fnm) |
| pnpm | 10 | `corepack enable` or `npm i -g pnpm` |
| uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

## Quick Start

### Option 1: Dev Container (Recommended)

Open in VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers):

```bash
code .
# Command Palette → "Dev Containers: Reopen in Container"
```

The container auto-runs `make setup` on first open.

### Option 2: Local Machine

```bash
# 1. Clone
git clone <repo-url>
cd podagent

# 2. Install everything
make setup

# 3. Start dev servers
make dev          # both server + web
# or separately:
make dev-server   # Python MCP server
make dev-web      # Next.js on http://localhost:3000
```

## Makefile Targets

| Target | What it does |
|--------|-------------|
| `make setup` | `uv sync` + `pnpm install` |
| `make dev` | Server + web in parallel |
| `make dev-server` | Run MCP server only |
| `make dev-web` | Run Next.js dev only |
| `make test` | pytest + vitest |
| `make lint` | ruff + mypy + eslint |
| `make format` | ruff format |
| `make build` | Next.js production build |
| `make clean` | Remove all caches, node_modules, .venv |

## Project Structure

```
apps/server    # Python MCP server (uv)
apps/web       # Next.js client (pnpm)
packages/shared-types   # TS contract types
```

## Environment Variables

Copy `.env.example` to `.env` at the repo root and fill in keys:

```bash
cp .env.example .env
```

Required for Phase 1:
- `OPENAI_API_KEY` — embeddings
- `DATABASE_URL` — Postgres/pgvector (optional, defaults to local)

## Adding Dependencies

```bash
# Python (server)
cd apps/server
uv add package-name

# TypeScript (web)
pnpm --filter web add package-name
```

## Common Issues

### `uv: command not found`
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### `pnpm: command not found`
```bash
npm install -g pnpm
```

### Port 3000 in use
```bash
# Web runs on 3000 by default. Override:
cd apps/web && pnpm dev --port 3001
```
