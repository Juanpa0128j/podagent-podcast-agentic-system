"""Auth middleware — JWT validation and tier enforcement.

Phase 1: stubbed with unlimited limits.
Phase 2: wire Supabase JWKS validation + Stripe tier enforcement.
"""

from __future__ import annotations

from typing import Any, Callable


class AuthContext:
    """Parsed auth context for a single request."""

    def __init__(self, user_id: str | None = None, tier: str = "free") -> None:
        self.user_id = user_id
        self.tier = tier


async def validate_jwt(token: str) -> AuthContext:
    """Validate a Supabase JWT and return auth context."""
    # TODO: implement JWKS validation
    return AuthContext(user_id=None, tier="free")


class TierLimitExceeded(Exception):
    """Raised when a user exceeds their tier limit."""

    def __init__(self, limit: int, used: int, upgrade_url: str = "") -> None:
        self.limit = limit
        self.used = used
        self.upgrade_url = upgrade_url


def require_tier(capability: str) -> Callable:
    """Decorator to enforce tier limits on MCP tools.

    Phase 1: no-op (unlimited).
    """

    def decorator(func: Callable) -> Callable:
        return func

    return decorator
