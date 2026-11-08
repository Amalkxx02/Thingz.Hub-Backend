from uuid import UUID

from pydantic import BaseModel, HttpUrl

# =====================================================================
#  Request Schemas
# =====================================================================


class CreateRequest(BaseModel):
    name: str
    profile: HttpUrl


# =====================================================================
#  DTO Schemas
# =====================================================================


class UserModel(BaseModel):
    """Full DB row representation for internal use."""

    user_id: UUID
    name: str
    profile: str | None = None


# =====================================================================
#  Response Schemas
# =====================================================================


class UserResponse(BaseModel):
    """User response returned from GET and POST endpoints."""

    user_id: UUID
    name: str
    profile: HttpUrl | None

    class Config:
        from_attributes = True
