from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from app.utils.datetime_utils import get_current_utc_time


class TokenModel(BaseModel):
    sub: UUID
    token_hash: bytes = Field(alias="token")
    jti: UUID
    exp: datetime
    iat: datetime
    revoked: bool = Field(default=False)
