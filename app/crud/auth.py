"""Example Auth CRUD Operations"""
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete,insert,update
from uuid import UUID

from app.models.auth import Auth


class CRUDAuth:
    @staticmethod
    async def get_user(db: AsyncSession, user_id: UUID):
        """Get user by ID"""
        return await db.scalar(select(Auth).where(Auth.id == user_id))
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email:EmailStr):
        """Get user by email"""
        return await db.scalar(select(Auth).where(Auth.email == email))

#     @staticmethod
#     def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100):
#         """Get multiple users with pagination"""
#         return db.query(Auth).offset(skip).limit(limit).all()

    @staticmethod
    async def insert(db: AsyncSession, payload:dict):
        stmt = insert(Auth).values(**payload)
        try:
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def verify(db: AsyncSession, email:EmailStr):
        stmt = update(Auth).where(Auth.email == email).values(verified = True)
        try:
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        
    staticmethod
    async def update_password(db:AsyncSession,user_id:UUID,password:bytes):
        stmt = update(Auth).where(Auth.id == user_id).values(password = password)
        try:
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        
#     @staticmethod
#     def update(db: AsyncSession, db_obj: Auth, obj_in: UserUpdate):
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
        stmt = delete(Auth).where(Auth.id == user_id)
        try:
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            raise e
            


crud_auth = CRUDAuth()
