"""Token schemas for request validation, DB representation, and API responses."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ──────────────────── DB Insert Schema ──────────────────── #


class TokenRequest(BaseModel):
    """Shape used when inserting a new token row."""

    sub: UUID
    token_hash: bytes = Field(alias="token")
    jti: UUID
    exp: datetime
    iat: datetime
    revoked: bool = False


# ──────────────────── DB Row Schema ──────────────────── #


class TokenDB(BaseModel):
    """Full DB row representation for internal use (read from DB)."""

    jti: UUID
    sub: UUID
    exp: datetime
    iat: datetime
    token_hash: bytes
    revoked: bool
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# ──────────────────── Response Schemas ──────────────────── #


class TokenResponse(BaseModel):
    """Returned after sign-in and token refresh."""
    is_onboarded: bool = False
    access_token: str | None = None
    refresh_token: str
