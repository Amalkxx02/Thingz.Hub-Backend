from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.users import crud as user_crud
from app.users.schemas import UserResponse


async def get_user_by_id(db: AsyncSession, user_id: UUID):
    """Get user by ID"""
    result = await user_crud.get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User profile is incomplete. Please complete onboarding first.",
        )
    return UserResponse.model_validate(result)

