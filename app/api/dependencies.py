# Third-Party
from uuid import UUID

from fastapi import Depends, Header
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import ExpiredSignatureError, JWTError

from app.core import exceptions
from app.core import security
from app.core.cache import CacheDB, get_cache_db

oauth2_scheme = HTTPBearer()


async def get_current_token(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    token: str = (token.model_dump()).get("credentials")
    return token


async def get_authenticated_user_id(token: str = Depends(get_current_token)) -> UUID:
    try:
        return security.decode_access_token(token).sub

    except ExpiredSignatureError:
        raise exceptions.TOKEN_EXPIRED
    except JWTError:
        raise exceptions.INVALID_TOKEN


async def get_refresh_session(token: str = Depends(get_current_token)):
    try:
        return security.decode_refresh_token(token)

    except ExpiredSignatureError:
        raise exceptions.TOKEN_EXPIRED
    except JWTError:
        raise exceptions.INVALID_TOKEN


async def verify_device_session(
    x_device_id: UUID = Header(...),
    x_device_token: str = Header(...),
    cache: CacheDB = Depends(get_cache_db),
):
    if not await cache.get(x_device_id) == x_device_token:
        raise exceptions.INVALID_CREDENTIALS

    return x_device_id
