# """
# user_utils.py
# --------------
# Utility functions for managing users in the IoT Dashboard.

# Functions:
# - insert_user: Add a new user to the database.
# - user_verify: Check if a user exists by email.
# - user_check: Verify a user exists by user_id.
# """

# from sqlalchemy import select, func
# from fastapi import HTTPException
# from models.models import User
# from sqlalchemy.ext.asyncio import AsyncSession
# from uuid import UUID


# async def insert_user(user_data: dict, db: AsyncSession) -> None:
#     new_user = User(
#         user_name=user_data["user_name"],
#         user_email=func.lower(user_data["user_email"]),
#         user_password=user_data["user_password"],
#     )
#     db.add(new_user)
#     await db.commit()


# async def user_verify(user_email: str, db: AsyncSession) -> User | None:
#     return await db.scalar(
#         select(User).where(func.lower(User.user_email) == func.lower(user_email))
#     )


# async def user_check(user_id: UUID, db: AsyncSession) -> User:
#     user = await db.scalar(select(User).where(User.user_id == user_id))
#     if user is None:
#         raise HTTPException(
#             status_code=409, detail="The user does not exist. This is an illegal move."
#         )
#     return user
