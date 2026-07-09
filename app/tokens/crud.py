from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select, update
from app.tokens.models import Token
from uuid import UUID

from app.utils.decorators import handle_db_errors


# =====================================================================
# 1. READ OPERATIONS
# =====================================================================
@handle_db_errors
async def get_token_by_jti(db: AsyncSession, jti: UUID):
    return await db.scalar(select(Token).where(Token.jti == jti))


@handle_db_errors
async def list_tokens_by_user_id(db: AsyncSession, user_id: UUID):
    result = await db.scalars(select(Token).where(Token.sub == user_id))
    return result.all()


# =====================================================================
# 2. WRITE OPERATIONS (Create)
# =====================================================================
@handle_db_errors
async def create_token(db: AsyncSession, payload: dict):
    stmt = insert(Token).values(**payload)

    await db.execute(stmt)
    await db.commit()


# =====================================================================
# 3. UPDATE OPERATIONS (Revoke, Revoke all)
# ==================================================================
@handle_db_errors
async def revoke_token(db: AsyncSession, jti: UUID, user_id: UUID):
    stmt = (
        update(Token).where(Token.jti == jti, Token.sub == user_id).values(is_revoked=True)
    )

    await db.execute(stmt)
    await db.commit()


@handle_db_errors
async def revoke_all_tokens(db: AsyncSession, user_id: UUID):
    stmt = update(Token).where(Token.sub == user_id).values(is_revoked=True)

    await db.execute(stmt)
    await db.commit()


# =====================================================================
# 4. DELETE OPERATIONS (Delete all)
# =====================================================================

@handle_db_errors
async def delete_token(db: AsyncSession, user_id: UUID,jti:UUID):
    stmt = delete(Token).where(Token.jti == jti,Token.sub == user_id)

    await db.execute(stmt)
    await db.commit()


@handle_db_errors
async def delete_all_tokens(db: AsyncSession, user_id: UUID):
    stmt = delete(Token).where(Token.sub == user_id)

    await db.execute(stmt)
    await db.commit()
