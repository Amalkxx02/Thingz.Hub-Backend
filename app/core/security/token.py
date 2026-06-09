from uuid import uuid4
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.schemas.enums import JwtType
from app.services import token as token_service
from app.utils.datetime_utils import get_current_utc_time, get_future_utc_time


JWT_CONFIG = {
    JwtType.REFRESH: (settings.JWT_ACCESS_KEY, settings.JWT_ACCESS_TTL, "minutes"),
    JwtType.ACCESS: (settings.JWT_REFRESH_KEY, settings.JWT_REFRESH_TTL, "days"),
}


async def create_token(
    db: AsyncSession, data: dict, token_type: JwtType = JwtType.ACCESS
) -> str:
    key, ttl, unit = JWT_CONFIG[token_type]
    payload = {
        **data,
        "iat": get_current_utc_time(),
        "exp": get_future_utc_time(**{unit: ttl}),
    }

    if JwtType(token_type) == JwtType.REFRESH:
        payload.update({"jti": str(uuid4())})

    token = jwt.encode(payload, key, settings.JWT_ALGORITHM)

    if JwtType(token_type) == JwtType.REFRESH:
        payload["token"] = token
        await token_service.insert(db, payload)

    return token


def decode_token(token: str, token_type: JwtType = JwtType.ACCESS) -> dict:
    key = JWT_CONFIG[token_type][0]
    return jwt.decode(token, key, algorithms=[settings.JWT_ALGORITHM])