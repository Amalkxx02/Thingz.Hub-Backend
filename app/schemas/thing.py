"""Thing schemas for request validation, DB representation, and API responses."""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel

from app.schemas.enums import DataType, ThingType


# ──────────────────── Request Schemas ──────────────────── #


class EdgeThingzRequest(BaseModel):
    slug: str
    hardware_address: str | None = "0"
    data_type: DataType
    thing_type: ThingType


class UpdateThingRequest(BaseModel):
    name: str | None = None
    unit: str | None = None


# ──────────────────── Response Schemas ──────────────────── #


class ThingResponse(BaseModel):
    """Single thing response for GET endpoints."""

    id: UUID
    device_id: UUID
    thing_type: int
    data_type: int
    name: str | None = None
    unit: str | None = None
    slug: str
    hardware_address: str | None = "0"
    is_active: bool = True
    meta: dict[str, Any] = {}
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ThingUpdateResponse(BaseModel):
    """Returned after updating a thing's name/unit."""

    name: str | None = None
    unit: str | None = None


class ThingToggleResponse(BaseModel):
    """Returned after toggling a thing's active status."""

    is_active: bool
