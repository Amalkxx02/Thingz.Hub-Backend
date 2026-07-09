from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import service as user_service
from app.users.schemas import UserResponse

from app.api.dependencies import get_authenticated_user_id
from app.core.database import get_db

router = APIRouter()


@router.get("", response_model=UserResponse)
async def get_user(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Get user by ID"""
    return await user_service.get_user_by_id(db, user_id)
