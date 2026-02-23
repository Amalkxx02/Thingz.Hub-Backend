from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import Onboard
from app.core.security.dependency import get_current_user
from app.services.user import user_service
from app.database.session import get_db

router = APIRouter()

@router.post("")
async def onboard(
    onboard: Onboard,
    db: AsyncSession = Depends(get_db),
    user_id:UUID = Depends(get_current_user)  
):
    user = await user_service.onboard(db, onboard.model_dump(),user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.get("")
async def get_user(
    db: AsyncSession = Depends(get_db),
    user_id:UUID = Depends(get_current_user)  
):
    """Get user by ID"""
    user = await user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
