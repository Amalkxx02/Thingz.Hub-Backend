from uuid import UUID, uuid4
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import CacheDB
from app.core import security

# cruds
from app.auth import crud as auth_crud
from app.users import crud as user_crud
from app.tokens import crud as token_crud

# services
from app.users import service as user_service
from app.tokens import service as token_service

# models
from app.auth.models import Auth
from app.users.models import User

# schemas
from app.auth.schemas import AuthModel, PasswordVerify, UserSignIn, UserSignUp, PasswordReset
from app.common.response import MessageResponse
from app.tokens.schemas import RefreshTokenResponse, TokenResponse

# utils
from app.users.schemas import UserModel
from app.utils import datetime_utils

# =====================================================================
# 0. READ SERVICE (ID & EMAIL)
# =====================================================================

# async def get_auth_by_id(db: AsyncSession, user_id: UUID):
#     """Get user by ID"""
#     return await auth_crud.get_auth_by_id(db, user_id)


# async def get_auth_by_email(db: AsyncSession, email: str):
#     """Get user by email"""
#     return await auth_crud.get_auth_by_email(db, email)


# =====================================================================
# 1. ONBOARD SERVICE (Sign_up -> Verify)
# =====================================================================


async def sign_up(db: AsyncSession, cache_db: CacheDB, user: UserSignUp) -> str:

    email = user.email
    auth_data: Auth = await auth_crud.get_auth_by_email(db, email)

    if auth_data:
        if auth_data.verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered and verified. Please login.",
            )
        elif not (
            datetime_utils.add_time(auth_data.created_at, 1)
            < datetime_utils.get_current_utc_time()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered but not verified. Check your inbox.",
            )

    hashed_password = security.hash_password(user.password)

    auth_db_data = AuthModel(email=user.email,password=hashed_password).model_dump()

    auth_data: Auth = await auth_crud.upsert_auth(
        db, auth_db_data
    )

    user_model = UserModel(
        user_id=auth_data.id,
        name=user.name,
        profile=str(user.profile),
    ).model_dump()
    
    await user_crud.create_user(db, user_model)

    await _send_verification(cache_db, email)

    return MessageResponse(message="Verification link sent to your email.")


async def verify_for_onboard(db: AsyncSession, cache_db: CacheDB, token: UUID):
    email: str = await cache_db.get(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired token"
        )

    await auth_crud.update_verify_by_email(db, email)

    await cache_db.delete(token)

    return MessageResponse(message="Email verified. Account created.")


# =====================================================================
# 2. SESSION SERVICE (Sign_in, Sign_out)
# =====================================================================


async def sign_in(db: AsyncSession, user: UserSignIn):

    auth_user: Auth = await auth_crud.get_auth_by_email(db, user.email)
    if not auth_user or not security.verify_password(user.password, auth_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not auth_user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not verified. Please check your email for the verification link.",
        )

    user: User = await user_crud.get_user_by_id(db, auth_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Complete your profile.",
        )

    return await token_service.issue_auth_token(db, user.user_id)


async def refresh_token(db: AsyncSession, token: RefreshTokenResponse):
    await token_service.validate_refresh_token(db, token.jti)

    access_token = token_service.generate_access_token(token.sub)

    return TokenResponse(access_token)


async def sign_out(
    db: AsyncSession, token: RefreshTokenResponse, is_all: bool
) -> MessageResponse:
    if is_all:
        await token_crud.revoke_all_tokens(db, token.sub)
        return MessageResponse(message="All sessions signed out successfully.")
    else:
        await token_crud.revoke_token(db, token.jti, token.sub)
        return MessageResponse(message="Signed out successfully.")


# =====================================================================
# 3. RECOVERY SERVICE (Forgot -> Send -> Reset)
# =====================================================================


async def password_reset(db: AsyncSession, cache_db: CacheDB, email: PasswordReset):

    if not await auth_crud.get_auth_by_email(db, email.email):
        return MessageResponse(message="Email Sent.")

    await _send_password_reset(cache_db, email.email)
    return MessageResponse(message="Email Sent.")


async def verify_for_reset(
    db: AsyncSession, cache_db: CacheDB, token: UUID, user: PasswordVerify
):
    email: str = await cache_db.get(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or Expired token")

    hashed_password: bytes = security.hash_password(user.password)
    await auth_crud.update_password_by_email(db, email, hashed_password)

    await cache_db.delete(token)

    return MessageResponse(message="Email verified. Password Updated.")


# =====================================================================
# 4. PRIVATE SERVICES
# =====================================================================


async def _create_and_cache_token(cache_db: CacheDB, email: EmailStr, endpoint: str):
    token = uuid4()

    await cache_db.set(token, email, 600)

    link = f"http://127.0.0.1:8000/api/v1/auths/{endpoint}?token={token}"
    print(link)


async def _send_verification(cache_db: CacheDB, email: EmailStr):
    await _create_and_cache_token(cache_db, email, "verify")


async def _send_password_reset(cache_db: CacheDB, email: EmailStr):
    await _create_and_cache_token(cache_db, email, "reset")
