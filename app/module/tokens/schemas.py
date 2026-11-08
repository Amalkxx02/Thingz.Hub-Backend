from datetime import datetime

from uuid import UUID

from pydantic import BaseModel, Field
from app.utils import datetime_utils

# =====================================================================
#  DTO Schemas
# =====================================================================


class AccessTokenModel(BaseModel):
    """Full DB row representation for internal use (read from DB)."""

    sub: UUID
    exp: datetime
    iat: datetime = Field(default_factory=datetime_utils.get_current_utc_time)


class RefreshTokenModel(AccessTokenModel):
    """Full DB row representation for internal use (read from DB)."""

    jti: UUID


# =====================================================================
#  Response Schemas
# =====================================================================


class TokenResponse(BaseModel):
    """Returned after sign-in and token refresh."""

    access_token: str
    refresh_token: str | None = None


class AccessTokenResponse(BaseModel):
    sub: UUID


class RefreshTokenResponse(AccessTokenResponse):
    jti: UUID
