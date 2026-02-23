# Third-Party
from uuid import UUID
from fastapi import Depends
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.enums import JwtType

from app.security.hashing import verify_fingerprint
from app.utils.security import to_uuid_4

from .token import create_token, decode_token
from .oauth import get_current_token

from app.services.token import token_service
from app.services.device import device_service


from app.core.exceptions import INVALID_CREDENTIALS, INVALID_TOKEN, TOKEN_EXPIRED


async def _verify_and_get_user(token: str) -> UUID:
    try:
        payload: dict = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise INVALID_CREDENTIALS
        return to_uuid_4(user_id)

    except ExpiredSignatureError:
        raise TOKEN_EXPIRED
    except JWTError:
        raise INVALID_TOKEN


async def get_current_user(token: str = Depends(get_current_token)) -> UUID:
    return await _verify_and_get_user(token)


async def get_current_device(
    db: AsyncSession = Depends(get_db), token: str = Depends(get_current_token)
):

    device = await device_service.verify_api_key(db, token)
    if not device:
        print(f"wrong api key : {token}")
    
    return device


async def get_refresh(
    db: AsyncSession = Depends(get_db), token: str = Depends(get_current_token)
) -> dict:
    try:
        payload: dict = decode_token(token, JwtType.REFRESH)

        user_id = to_uuid_4(payload.get("sub"))
        jti = to_uuid_4(payload.get("jti"))

        if not all([user_id, jti]):
            raise INVALID_CREDENTIALS

        record = await token_service.get_by_jti(db, jti)

        if not record:
            raise INVALID_TOKEN
        if record["revoked"]:
            raise INVALID_TOKEN
        if not verify_fingerprint(token, record["token_hash"]):
            await token_service.revoke(db, user_id)
            raise INVALID_TOKEN

        data = {"email": payload["email"], "sub": str(user_id)}

        new_token = await create_token(db, data)

        return {"token": new_token, "jti": jti, "user_id": user_id}

    except ExpiredSignatureError:
        raise TOKEN_EXPIRED
    except JWTError:
        raise INVALID_TOKEN
