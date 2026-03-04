from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import crud_user
from app.schemas.user import Onboard
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
            raise ValueError("User already onboarded")

        auth = await auth_service.get_user(db, user_id)
        if not auth:
            raise ValueError("User not verified")

        payload["user_id"] = user_id
        payload["profile_image_url"] = str(onboard.profile_image_url)
        payload["email"] = auth.email

        return await crud_user.onboard(db, payload)


user_service = UserService()
