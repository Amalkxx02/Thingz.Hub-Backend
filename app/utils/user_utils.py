"""
user_utils.py
--------------
Utility functions for managing users in the IoT Dashboard.

Functions:
- insert_user: Add a new user to the database.
- user_verify: Check if a user exists by email.
- user_check: Verify a user exists by user_id.
"""

from sqlalchemy import select, func
from fastapi import HTTPException
from models.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


async def insert_user(user_data: dict, db: AsyncSession) -> None:
    """
    Insert a new user into the database.

    Args:
        user_data (dict): Contains keys 'user_name', 'user_email', 'user_password'
        db (AsyncSession): Async SQLAlchemy session

    Notes:
        - Emails are stored in lowercase to ensure uniqueness regardless of case.
        - Assumes user_password is already hashed (e.g., using bcrypt).
        - Commit is done here; could be wrapped in transaction for multi-step registration.
    """
    new_user = User(
        user_name=user_data["user_name"],
        user_email=func.lower(user_data["user_email"]),
        user_password=user_data["user_password"],
    )
    db.add(new_user)
    await db.commit()


async def user_verify(user_email: str, db: AsyncSession) -> User | None:
    """
    Check if a user exists by email.

    Args:
        user_email (str): Email to search for
        db (AsyncSession): Async SQLAlchemy session

    Returns:
        User | None: Returns User object if found, else None
    """
    return await db.scalar(
        select(User).where(func.lower(User.user_email) == func.lower(user_email))
    )


async def user_check(user_id: UUID, db: AsyncSession) -> User:
    """
    Verify that a user exists by user_id.

    Args:
        user_id (UUID): User ID to validate
        db (AsyncSession): Async SQLAlchemy session

    Returns:
        User: User object if exists

    Raises:
        HTTPException 409: If user does not exist

    Notes:
        - Useful for endpoints requiring validated users.
        - Can be extended to integrate JWT user ID validation in the future.
    """
    user = await db.scalar(select(User).where(User.user_id == user_id))
    if user is None:
        raise HTTPException(
            status_code=409, detail="The user does not exist. This is an illegal move."
        )
    return user
