from datetime import timedelta
from uuid import UUID, uuid4
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import auth as crud_auth
from app.crud import token as crud_token
from app.crud import user as crud_user

from app.database.cache_db import CacheDB
from app.models.auth import Auth

# from app.schemas.auth import VerificationResponse
from app.models.user import User

from app.schemas.enums import JwtType
from app.schemas.response import MessageResponse
from app.schemas.token import TokenResponse

from app.security.hashing import hash_password, verify_password

from app.core.jwt.token import create_token

from app.utils.datetime_utils import add_time, get_current_utc_time, get_future_utc_time



async def get_user(db: AsyncSession, user_id: UUID):
    """Get user by ID"""
    return await crud_auth.get_user(db, user_id)


async def get_by_email(db: AsyncSession, email: str):
    """Get user by email"""
    return await crud_auth.get_by_email(db, email)


async def register(db: AsyncSession, cache_db: CacheDB, payload: dict) -> str:

    email = payload["email"]
    user: Auth = await crud_auth.get_by_email(db, email)

    if user:
        if user.verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered and verified. Please login.",
            )
        elif not (add_time(user.created_at, 10) < get_current_utc_time()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered but not verified. Check your inbox.",
            )

    password = hash_password(payload["password"])
    payload["password"] = password

    await crud_auth.insert_auth(db, payload)

    token = uuid4()

    await cache_db.set(token, payload["email"], 600)

    verification_link = f"http://127.0.0.1:8000/api/v1/auths/verify?token={token}"
    print(verification_link)
    return MessageResponse(message="Verification link sent to your email.")


async def verify(db: AsyncSession, cache_db: CacheDB, token: UUID):
    email: str = await cache_db.get(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or Expired token")

    await crud_auth.verify(db, email)

    await cache_db.delete(token)

    return {"message": "Email verified. Account created."}


async def authenticate(db: AsyncSession, payload: dict):

    auth_user: Auth = await crud_auth.get_by_email(db, payload["email"])
    if not auth_user or not verify_password(payload["password"], auth_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not auth_user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not verified. Please check your email for the verification link.",
        )
    user: User = await crud_user.get_user(db, auth_user.id)
    if user:
        onboarded = user.is_onboarded
    else:
        onboarded = False
    data = {"is_onboarded": onboarded, "sub": str(auth_user.id)}
    return TokenResponse(
        is_onboarded=onboarded,
        access_token=await create_token(JwtType.ACCESS, data),
        refresh_token=await create_token(JwtType.REFRESH, data),
    )


async def sign_out(db: AsyncSession, token_info: dict, is_all: bool) -> MessageResponse:
    jti = token_info["jti"]
    user_id = token_info["user_id"]
    if is_all:
        await crud_token.revoke_all(db, user_id)
        return MessageResponse(message="All sessions signed out successfully.")
    else:
        await crud_token.revoke(db, jti, user_id)
        return MessageResponse(message="Signed out successfully.")
