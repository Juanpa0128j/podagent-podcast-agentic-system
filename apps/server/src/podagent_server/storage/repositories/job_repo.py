"""Job repository (stub)."""

from __future__ import annotations

from podagent_server.storage.models import Job
from podagent_server.storage.repositories import JobRepo


class SupabaseJobRepo(JobRepo):
    """Supabase-backed job repository."""

    async def create(self, job: Job) -> Job:
        """Persist a new job."""
        # TODO: implement via Supabase/postgrest
        return job

    async def get(self, job_id: str) -> Job | None:
        """Fetch a job by id."""
        # TODO: implement
        return None

    async def update(self, job: Job) -> Job:
        """Update job state and progress."""
        # TODO: implement
        return job
