"""CLI for local transcript ingestion."""

from __future__ import annotations

import argparse
import asyncio
import logging
from pathlib import Path

from podagent_server.ingestion.pipeline import run_ingestion_pipeline

logger = logging.getLogger(__name__)


def build_default_path() -> Path:
    repo_root = Path(__file__).resolve().parents[5]
    return repo_root / "podcasts" / "Huberman"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest local transcript files into the vector store."
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=build_default_path(),
        help="Path to a transcript file or directory of .md files.",
    )
    return parser.parse_args()


async def ingest_paths(paths: list[Path]) -> list[str]:
    job_ids: list[str] = []
    for path in paths:
        job_id = await run_ingestion_pipeline(source="upload", ref=str(path))
        job_ids.append(job_id)
    return job_ids


def resolve_paths(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(target.glob("*.md"))


async def run() -> int:
    args = parse_args()
    paths = resolve_paths(args.path)

    if not paths:
        logger.error("No transcript files found at %s", args.path)
        return 1

    logger.info("Ingesting %s transcript file(s)", len(paths))
    await ingest_paths(paths)
    logger.info("Ingestion complete")
    return 0


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    return asyncio.run(run())


if __name__ == "__main__":
    raise SystemExit(main())
