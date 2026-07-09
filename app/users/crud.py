from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from uuid import UUID

from app.users.models import User
from app.utils.decorators import handle_db_errors

# =====================================================================
# 1. READ OPERATIONS
# =====================================================================

@handle_db_errors
async def get_user_by_id(db: AsyncSession, user_id: UUID):
    return await db.scalar(select(User).where(User.user_id == user_id))

# =====================================================================
# 2. WRITE OPERATIONS (Create)
# =====================================================================

@handle_db_errors
async def create_user(db: AsyncSession, payload: dict):
    stmt = insert(User).values(**payload)
    stmt = stmt.on_conflict_do_update(
        index_elements=["user_id"],
        set_={
            "name": stmt.excluded.name,
            "profile":stmt.excluded.profile,
            "created_at": stmt.excluded.created_at,
        },
    ).returning(User)

    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()

# =====================================================================
# 3. UPDATE OPERATIONS ()
# ==================================================================

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

# =====================================================================
# 4. DELETE OPERATIONS
# =====================================================================

@handle_db_errors
async def delete_user(db: AsyncSession, user_id: UUID):
    stmt = delete(User).where(User.user_id == user_id)
    
    await db.execute(stmt)
    await db.commit()
