SHELL := /bin/bash
.SILENT:

.PHONY: help setup dev dev-server dev-web test lint format build clean

help: ## Show this help
	@echo "PodAgent Makefile targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup: ## Install all deps (uv sync + pnpm install)
	echo "Setting up PodAgent monorepo..."
	cd apps/server && uv sync --all-extras
	pnpm install
	echo "Done. Run 'make dev' to start."

dev: ## Start server + web in parallel
	@echo "Starting both dev servers..."
	trap 'kill %1 %2' EXIT; \
		make dev-server & \
		make dev-web & \
		wait

dev-server: ## Start Python MCP server only
	cd apps/server && uv run python -m podagent_server.mcp.server

dev-web: ## Start Next.js dev server only
	cd apps/web && pnpm dev

test: ## Run pytest + vitest
	cd apps/server && uv run pytest
	cd apps/web && pnpm test

lint: ## Run ruff, mypy, eslint
	cd apps/server && uv run ruff check src tests && uv run mypy src
	cd apps/web && pnpm lint

format: ## Run ruff format (prettier TBD)
	cd apps/server && uv run ruff format src tests
	cd apps/web && echo "Add prettier write here when configured"

build: ## Build Next.js for production
	cd apps/web && pnpm build

clean: ## Remove caches, venvs, node_modules
	rm -rf apps/server/.venv apps/web/node_modules node_modules
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .next -exec rm -rf {} + 2>/dev/null || true
