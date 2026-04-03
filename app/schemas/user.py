"""User schemas for request validation, DB representation, and API responses."""

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, AfterValidator, HttpUrl

from .utils import is_empty


# ──────────────────── Request Schemas ──────────────────── #

class Onboard(BaseModel):
    name: Annotated[str, AfterValidator(is_empty)]
    profile_image_url: HttpUrl


# ──────────────────── DB Row Schemas ──────────────────── #

class UserDB(BaseModel):
    """Full DB row representation for internal use."""
    user_id: UUID
    name: str
    email: str
    profile_image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ──────────────────── Response Schemas ──────────────────── #

class UserOut(BaseModel):
    """User response returned from GET and POST endpoints."""
    user_id: UUID
    name: str
    email: str
    profile_image_url: HttpUrl

    class Config:
        from_attributes = True
