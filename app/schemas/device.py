"""Device schemas for request validation, DB representation, and API responses."""

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, AfterValidator

from app.schemas.enums import DeviceType
from app.schemas.utils import is_empty


# ──────────────────── Request Schemas ──────────────────── #

class DeviceRequest(BaseModel):
    name: Annotated[str, AfterValidator(is_empty)]
    type: DeviceType


class EdgeDeviceRequest(BaseModel):
    id: UUID
    key: Annotated[str, AfterValidator(is_empty)]
    type: DeviceType

# ──────────────────── Response Schemas ──────────────────── #

class DeviceResponse(BaseModel):
    """Single device response – excludes sensitive fields (hashed_key, user_id)."""
    id: UUID
    name: str
    type: int
    key_hint: str
    revoked: bool
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class DeviceRegisterResponse(BaseModel):
    """Returned after successfully registering a new device."""
    device_id: UUID
    api_key: str

class DeviceToggleResponse(BaseModel):
    """Returned after toggling a device's active status."""
    is_active: bool


class DeviceVerifyResponse(BaseModel):
    """Returned after verifying an edge device."""
    session_token: str | None = None
    verified: bool = False
