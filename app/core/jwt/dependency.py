# Third-Party
from uuid import UUID
from fastapi import Depends, Header
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.database.cache_db import CacheDB, get_cache_db
from app.schemas.enums import JwtType

from app.security.hashing import verify_fingerprint
from app.utils.security import to_uuid_4_by_str

from .token import create_token, decode_token
from .oauth import get_current_token

from app.services import token as token_service


from app.core.exceptions import (
    INVALID_CREDENTIALS,
    INVALID_TOKEN,
    TOKEN_EXPIRED,
    PROFILE_INCOMPLETE,
)


async def _validate_access_token(token: str, require_onboarding: bool) -> UUID:
    try:
        payload: dict = decode_token(token)
        user_id = payload.get("sub")

        if require_onboarding and not payload.get("is_onboarded"):
            raise PROFILE_INCOMPLETE

        if not user_id:
            raise INVALID_CREDENTIALS

        return to_uuid_4_by_str(user_id)

    except ExpiredSignatureError:
        raise TOKEN_EXPIRED
    except JWTError:
        raise INVALID_TOKEN


async def get_authenticated_user_id(token: str = Depends(get_current_token)) -> UUID:
    return await _validate_access_token(token, False)


async def get_verified_user_id(token: str = Depends(get_current_token)) -> UUID:
    return await _validate_access_token(token, True)


async def verify_device_session(
    x_device_id: UUID = Header(...),
    x_device_token: str = Header(...),
    cache: CacheDB = Depends(get_cache_db),
):
    if not await cache.get(x_device_id) == x_device_token:
        raise INVALID_CREDENTIALS

    return x_device_id


async def _validate_refresh_token(
    db: AsyncSession, token: str, require_token: bool
) -> dict | UUID:
    try:
        payload: dict = decode_token(token, JwtType.REFRESH)

        user_id = to_uuid_4_by_str(payload.get("sub"))
        jti = to_uuid_4_by_str(payload.get("jti"))

        if not all([user_id, jti]):
            raise INVALID_CREDENTIALS

        record = await token_service.get_by_jti(db, jti)

        if not record:
            raise INVALID_TOKEN

        if record.revoked:
            raise INVALID_TOKEN

        if not verify_fingerprint(token, record.token_hash):
            await token_service.revoke(db, user_id)
            raise INVALID_TOKEN

        if require_token:
            data = {"is_onboarded": payload.get("is_onboarded"), "sub": str(user_id)}
            new_token = await create_token(db, data)
            return new_token

        return {"jti": jti, "user_id": user_id}

    except ExpiredSignatureError:
        raise TOKEN_EXPIRED
    except JWTError:
        raise INVALID_TOKEN


async def get_refresh_session(db: AsyncSession = Depends(get_db),token: str = Depends(get_current_token)) -> str:
    return await _validate_refresh_token(db, token, True)


async def get_revocation_context(db: AsyncSession = Depends(get_db),token: str = Depends(get_current_token)) -> dict:
    return await _validate_refresh_token(db, token, False)
