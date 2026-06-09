from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import Onboard, UserOut
from app.core.security.dependency import get_current_user
from app.services import user as user_service
from app.database.session import get_db

router = APIRouter()


@router.post("", response_model=UserOut)
async def onboard(
    onboard: Onboard,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return await user_service.onboard(db, onboard, user_id)


@router.get("", response_model=UserOut)
async def get_user(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    """Get user by ID"""
    return await user_service.get_user(db, user_id)
