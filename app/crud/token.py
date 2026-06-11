from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select, update
from app.models.token import Token
from uuid import UUID

from app.utils.decorators import handle_db_errors

@handle_db_errors
async def get_by_jti(db: AsyncSession, jti: UUID):
    return await db.scalar(select(Token).where(Token.jti == jti))

@handle_db_errors
async def get_by_user(db: AsyncSession, user_id: UUID):
    return await db.scalar(select(Token).where(Token.sub == user_id))

@handle_db_errors
async def insert_token(db: AsyncSession, payload: dict):
    stmt = insert(Token).values(**payload)

    await db.execute(stmt)
    await db.commit()

@handle_db_errors
async def revoke(db: AsyncSession, jti: UUID, user_id: UUID):
    stmt = (
        update(Token).where(Token.jti == jti, Token.sub == user_id).values(revoked=True)
    )

    await db.execute(stmt)
    await db.commit()

@handle_db_errors
async def revoke_all(db: AsyncSession, user_id: UUID):
    stmt = update(Token).where(Token.sub == user_id).values(revoked=True)

    await db.execute(stmt)
    await db.commit()

@handle_db_errors
async def delete_all(db: AsyncSession, user_id: UUID):
    stmt = delete(Token).where(Token.sub == user_id)

    await db.execute(stmt)
    await db.commit()
