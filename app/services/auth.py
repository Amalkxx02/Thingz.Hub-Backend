from uuid import UUID, uuid4
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.auth import crud_auth
from app.crud.token import crud_token
from app.models.auth import Auth
from app.schemas.enums import JwtType
from app.security.hashing import hash_password, verify_password
from app.core.security.token import create_token
from app.utils.datetime_utils import get_current_utc_time, get_future_utc_time

pending_user = {}


class AuthService:

    @staticmethod
    async def get_user(db: AsyncSession, user_id: UUID):
        """Get user by ID"""
        return await crud_auth.get_user(db, user_id)

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        """Get user by email"""
        return await crud_auth.get_by_email(db, email)

    @staticmethod
    async def register(db: AsyncSession, payload: dict) -> str:

        email = payload["email"]
        user: Auth = await crud_auth.get_by_email(db, email)

        if user:
            if user.verified:
                return {
                    "status": "error",
                    "message": "User is already verified. Please login.",
                }
            else:
                return {
                    "status": "pending",
                    "message": "Email already registered but not verified. Check your inbox.",
                }

        password = hash_password(payload["password"])
        payload["password"] = password

        await crud_auth.insert(db, payload)

        token = uuid4()
        expires_at = get_future_utc_time(minutes=10)
        pending_user[token] = {
            "email": payload["email"],
            "expires_at": expires_at,
        }

        verification_link = f"Verification link: http://127.0.0.1:8000/api/v1/auths/verify?token={token}"

        return verification_link

    @staticmethod
    async def verify(db: AsyncSession, token: UUID):
        pending: dict = pending_user.get(token)
        if not pending:
            raise HTTPException(status_code=400, detail="Invalid or Expired token")

        if get_current_utc_time() > pending["expires_at"]:
            del pending_user[token]
            raise HTTPException(status_code=400, detail="Token Expired")

        email = pending.get("email")

        await crud_auth.verify(db, email)

        del pending_user[token]

        return {"message": "Email verified. Account created."}

    @staticmethod
    async def authenticate(db: AsyncSession, payload: dict):

        user: Auth = await crud_auth.get_by_email(db, payload["email"])

        if not user or not verify_password(payload["password"], user.password):
            return {"status": "error", "message": "Invalid email or password."}

        if not user.verified:
            return {
                "status": "pending",
                "message": "Your account is not verified. Please check your email for the link.",
            }

        data = {"email": user.email, "sub": str(user.id)}
        return {
            "status": "success",
            "access": await create_token(db, data),
            "refresh": await create_token(db, data, JwtType.REFRESH),
        }

    @staticmethod
    async def sign_out(db: AsyncSession, token_info: dict, is_all: bool):
        jti = token_info["jti"]
        user_id = token_info["user_id"]
        if is_all:
            await crud_token.revoke_all(db, user_id)
        else:
            await crud_token.revoke(db, jti, user_id)


auth_service = AuthService()
