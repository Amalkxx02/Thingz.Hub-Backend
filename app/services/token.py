from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import token as crud_token
from app.schemas.token import TokenRequest
from app.security.hashing import get_fingerprint
from uuid import UUID


async def get_by_jti(db: AsyncSession, jti: UUID):
    return await crud_token.get_by_jti(db, jti)


async def get_by_user(db: AsyncSession, user_id: UUID):
    return await crud_token.get_by_user(db, user_id)


async def insert(db: AsyncSession, payload: dict):
    payload["token"] = get_fingerprint(payload["token"])
    await crud_token.insert(db, TokenRequest(**payload).model_dump())


async def revoke(db: AsyncSession, jti: UUID, user_id: UUID):
    return await crud_token.revoke(db, user_id)
