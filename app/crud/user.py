"""Example User CRUD Operations"""
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete,insert,update
from uuid import UUID

from app.models.user import User


class CRUDUser:
    @staticmethod
    async def get_user(db: AsyncSession, user_id: UUID):
        """Get user by ID"""
        return await db.scalar(select(User).where(User.user_id == user_id))
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email:EmailStr):
        """Get user by email"""
        return await db.scalar(select(User).where(User.email == email))

#     @staticmethod
#     def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100):
#         """Get multiple users with pagination"""
#         return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    async def onboard(db: AsyncSession, payload:dict):
        stmt = insert(User).values(**payload)
        try:
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            await db.rollback()
            raise e

#     @staticmethod
#     def update(db: AsyncSession, db_obj: User, obj_in: UserUpdate):
#         """Update user"""
#         update_data = obj_in.dict(exclude_unset=True)
#         if "password" in update_data:
#             hashed_password = get_password_hash(update_data.pop("password"))
#             update_data["hashed_password"] = hashed_password
        
#         for field, value in update_data.items():
#             setattr(db_obj, field, value)
        
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

    @staticmethod
    async def delete(db: AsyncSession, user_id: UUID):
        """Delete user"""
        stmt = delete(User).where(User.user_id == user_id)
        try:
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            raise e
            


crud_user = CRUDUser()
