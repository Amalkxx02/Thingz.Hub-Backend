from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, update
from uuid import UUID

from app.models.user import User
from app.utils.decorators import handle_db_errors


@handle_db_errors
async def get_user(db: AsyncSession, user_id: UUID):
    return await db.scalar(select(User).where(User.user_id == user_id))


@handle_db_errors
async def get_by_email(db: AsyncSession, email: EmailStr):
    return await db.scalar(select(User).where(User.email == email))


@handle_db_errors
async def onboard(db: AsyncSession, payload: dict):
    stmt = insert(User).values(**payload).returning(User)

    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()


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


@handle_db_errors
async def delete(db: AsyncSession, user_id: UUID):
    stmt = delete(User).where(User.user_id == user_id)
    
    await db.execute(stmt)
    await db.commit()
