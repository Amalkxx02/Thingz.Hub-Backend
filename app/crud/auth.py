from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, update
from uuid import UUID

from app.models.auth import Auth


async def get_user(db: AsyncSession, user_id: UUID):
    """Get user by ID"""
    return await db.scalar(select(Auth).where(Auth.id == user_id))


async def get_by_email(db: AsyncSession, email: EmailStr):
    """Get user by email"""
    return await db.scalar(select(Auth).where(Auth.email == email))


async def insert_auth(db: AsyncSession, payload: dict):
    stmt = insert(Auth).values(**payload)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def verify(db: AsyncSession, email: EmailStr):
    stmt = update(Auth).where(Auth.email == email).values(verified=True)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def update_password(db: AsyncSession, user_id: UUID, password: bytes):
    stmt = update(Auth).where(Auth.id == user_id).values(password=password)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def delete(db: AsyncSession, user_id: UUID):
    stmt = delete(Auth).where(Auth.id == user_id)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        raise e
