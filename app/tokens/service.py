from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4, UUID

from app.tokens import crud as token_crud
from app.tokens.schemas import AccessTokenModel, RefreshTokenModel, TokenResponse

from app.utils import datetime_utils

from app.core.config import settings
from app.core import security
from app.core import exceptions

# =====================================================================
# 1. TOKEN GENERATION SERVICE
# =====================================================================


async def issue_auth_token(db: AsyncSession, user_id: UUID):
    raw_refresh = await generate_refresh_token(db, user_id)
    raw_access = generate_access_token(user_id)
    return TokenResponse(access_token=raw_access, refresh_token=raw_refresh)


def generate_access_token(user_id: UUID):
    token_model = AccessTokenModel(
        sub=user_id,
        exp=datetime_utils.get_future_utc_time(minutes=settings.JWT_ACCESS_TTL),
    ).model_dump()
    token_model["sub"] = str(token_model["sub"])
    return security.encode_access_token(token_model)


async def generate_refresh_token(db: AsyncSession, user_id: UUID):
    token_model = RefreshTokenModel(
        jti=uuid4(),
        sub=user_id,
        exp=datetime_utils.get_future_utc_time(days=settings.JWT_REFRESH_TTL),
    ).model_dump()
    await token_crud.create_token(db, token_model)
    token_model["jti"] = str(token_model["jti"])
    token_model["sub"] = str(token_model["sub"])
    return security.encode_refresh_token(token_model)


# =====================================================================
# 2. TOKEN VERIFICATION SERVICE
# =====================================================================


async def validate_refresh_token(db: AsyncSession, jti: UUID):

    record = await token_crud.get_token_by_jti(db, jti)

    if not record or record.is_revoked:
        raise exceptions.INVALID_TOKEN


# =====================================================================
# 3. REVOCATION SERVICE
# =====================================================================


async def revoke_single_token(db: AsyncSession, user_id: UUID, jti: UUID):
    """Terminates a single specific device session."""
    await token_crud.delete_token(db, jti=jti, user_id=user_id)


async def revoke_all_user_tokens(db: AsyncSession, user_id: UUID):
    """Emergency cut-off: Terminates all active sessions for a user."""
    await token_crud.delete_all_tokens(db, user_id=user_id)

