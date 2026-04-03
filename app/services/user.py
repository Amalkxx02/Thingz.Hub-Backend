from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import crud_user
from app.schemas.user import Onboard, UserOut
from app.services.auth import auth_service

pending_user = {}


class UserService:

    @staticmethod
    async def get_user(db: AsyncSession, user_id: UUID):
        """Get user by ID"""
        return await crud_user.get_user(db, user_id)
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        """Get user by email"""
        return await crud_user.get_by_email(db, email)

    @staticmethod
    async def onboard(db: AsyncSession, onboard: Onboard, user_id: UUID):
        payload = onboard.model_dump()
        user = await crud_user.get_user(db, user_id)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already onboarded.",
            )

        auth = await auth_service.get_user(db, user_id)
        if not auth:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User not verified.",
                )

        payload["user_id"] = user_id
        payload["profile_image_url"] = str(onboard.profile_image_url)
        payload["email"] = auth.email
        payload["is_onboarded"] = True
        user = await crud_user.onboard(db, payload)
        return UserOut(**user.__dict__)



user_service = UserService()
