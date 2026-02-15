from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    sub: UUID
    token_hash: bytes = Field(alias="token")
    jti: UUID
    exp: datetime
    iat: datetime
    revoked: bool = Field(default=False)
