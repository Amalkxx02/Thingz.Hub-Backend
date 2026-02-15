from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select,update
from app.models.token import Token
from uuid import UUID

class CRUDToken:
    """CRUD operations for Token model"""

    @staticmethod
    async def get_by_jti(db: AsyncSession, jti: UUID):
        """Get token by jti"""
        return await db.scalar(select(Token).where(Token.jti == jti))
    
    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: UUID):
        """Get token by user id"""
        return await db.scalar(select(Token).where(Token.sub == user_id))

    @staticmethod
    async def insert(db: AsyncSession,payload:dict):
        stmt = insert(Token).values(**payload)
        try:
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            await db.rollback()
            raise e
        
    async def revoke(db: AsyncSession,user_id:UUID):
        stmt = (
            update(Token)
            .where(Token.sub == user_id)
            .values(revoked=True)
        )
        try:
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def delete_all(db: AsyncSession, user_id: UUID):
        """Delete user"""
        stmt = delete(Token).where(Token.sub == user_id)
        
        try:
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            await db.rollback()
            raise e
crud_token = CRUDToken()
