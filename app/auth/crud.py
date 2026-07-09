from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert
from uuid import UUID

from app.auth.models import Auth
from app.utils.decorators import handle_db_errors

# =====================================================================
# 1. READ OPERATIONS
# =====================================================================


@handle_db_errors
async def get_auth_by_id(db: AsyncSession, user_id: UUID):
    """Get user by ID"""
    return await db.scalar(select(Auth).where(Auth.id == user_id))


@handle_db_errors
async def get_auth_by_email(db: AsyncSession, email: EmailStr):
    """Get user by email"""
    return await db.scalar(select(Auth).where(Auth.email == email))


# =====================================================================
# 2. WRITE OPERATIONS (Create / Upsert)
# =====================================================================


@handle_db_errors
async def upsert_auth(db: AsyncSession, payload: dict):
    stmt = insert(Auth).values(**payload)

    stmt = stmt.on_conflict_do_update(
        index_elements=["email"],
        set_={
            "password": stmt.excluded.password,
            "created_at": stmt.excluded.created_at,
        },
    ).returning(Auth)

    result = await db.execute(stmt)
    await db.commit()

    return result.scalar_one_or_none()


# =====================================================================
# 3. UPDATE OPERATIONS (Verify, Passwords)
# =====================================================================


@handle_db_errors
async def update_verify_by_email(db: AsyncSession, email: EmailStr):
    stmt = update(Auth).where(Auth.email == email).values(verified=True)

    await db.execute(stmt)
    await db.commit()


@handle_db_errors
async def update_password_by_id(db: AsyncSession, user_id: UUID, password: bytes):
    stmt = update(Auth).where(Auth.id == user_id).values(password=password)

    await db.execute(stmt)
    await db.commit()


@handle_db_errors
async def update_password_by_email(db: AsyncSession, email: EmailStr, password: bytes):
    stmt = update(Auth).where(Auth.email == email).values(password=password)

    await db.execute(stmt)
    await db.commit()


# =====================================================================
# 4. DELETE OPERATIONS
# =====================================================================


@handle_db_errors
async def delete_auth_by_id(db: AsyncSession, user_id: UUID):
    stmt = delete(Auth).where(Auth.id == user_id)

    await db.execute(stmt)
    await db.commit()
