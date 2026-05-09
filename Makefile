SHELL := /bin/bash
.SILENT:

.PHONY: setup dev dev-server dev-web test lint format build clean

setup:
	echo "Setting up PodAgent monorepo..."
	# Python server deps
	cd apps/server && uv sync --all-extras
	# Node deps
	pnpm install
	echo "Done. Run 'make dev' to start."

dev:
	@echo "Starting both dev servers..."
	trap 'kill %1 %2' EXIT; \
		make dev-server & \
		make dev-web & \
		wait

dev-server:
	cd apps/server && uv run python -m podagent_server.mcp.server

dev-web:
	cd apps/web && pnpm dev

test:
	cd apps/server && uv run pytest
	cd apps/web && pnpm test

lint:
	cd apps/server && uv run ruff check src tests && uv run mypy src
	cd apps/web && pnpm lint

format:
	cd apps/server && uv run ruff format src tests
	cd apps/web && echo "Add prettier write here when configured"

build:
	cd apps/web && pnpm build

clean:
	rm -rf apps/server/.venv apps/web/node_modules node_modules
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .next -exec rm -rf {} + 2>/dev/null || true
