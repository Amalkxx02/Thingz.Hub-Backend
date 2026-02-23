from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.token import crud_token
from app.schemas.token import TokenRequest
from app.security.hashing import get_fingerprint
from uuid import UUID


class TokenService:
    
    @staticmethod
    async def get_by_jti(db: AsyncSession, jti: UUID):
        return await crud_token.get_by_jti(db, jti)

    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: UUID):
        return await crud_token.get_by_user(db, user_id)

    @staticmethod
    async def insert(db: AsyncSession, payload: dict):
        payload["token"] = get_fingerprint(payload["token"])
        await crud_token.insert(db, TokenRequest(**payload).model_dump())

    @staticmethod
    async def revoke(db: AsyncSession,jti:UUID, user_id: UUID):
        return await crud_token.revoke(db, user_id)


token_service = TokenService()
