from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select, update
from app.models.token import Token
from uuid import UUID


async def get_by_jti(db: AsyncSession, jti: UUID):
    return await db.scalar(select(Token).where(Token.jti == jti))


async def get_by_user(db: AsyncSession, user_id: UUID):
    return await db.scalar(select(Token).where(Token.sub == user_id))


async def insert(db: AsyncSession, payload: dict):
    stmt = insert(Token).values(**payload)
    try:
        result = await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def revoke(db: AsyncSession, jti: UUID, user_id: UUID):
    stmt = (
        update(Token).where(Token.jti == jti, Token.sub == user_id).values(revoked=True)
    )
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def revoke_all(db: AsyncSession, user_id: UUID):
    stmt = update(Token).where(Token.sub == user_id).values(revoked=True)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def delete_all(db: AsyncSession, user_id: UUID):
    stmt = delete(Token).where(Token.sub == user_id)
    try:
        result = await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
