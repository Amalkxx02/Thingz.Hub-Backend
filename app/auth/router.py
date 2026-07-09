from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.schemas import PasswordVerify, UserSignIn, UserSignUp, PasswordReset
from app.common.response import MessageResponse
from app.api.dependencies import get_refresh_session
from app.tokens.schemas import RefreshTokenResponse, TokenResponse
from app.auth import services as auth_service
from app.core.database import get_db
from app.core.cache import CacheDB, get_cache_db

router = APIRouter()


# =====================================================================
# 1. ONBOARDING (Register & Verify)
# =====================================================================


@router.post(
    "/sign_up",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
)
async def sign_up(
    user: UserSignUp,
    db: AsyncSession = Depends(get_db),
    cache_db: CacheDB = Depends(get_cache_db),
):
    return await auth_service.sign_up(db, cache_db, user)


@router.get(
    "/verify",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def verify_for_onboard(
    token: UUID,
    db: AsyncSession = Depends(get_db),
    cache_db: CacheDB = Depends(get_cache_db),
):
    await auth_service.verify_for_onboard(db, cache_db, token)
    html_content = """
    <html>
        <head>
            <title>IoT Dashboard | Success</title>
        </head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 100px; background-color: #f4f7f6;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 50px; color: #27ae60;">✔</div>
                <h1 style="color: #2c3e50; margin-top: 10px;">Verification Successful!</h1>
                <p style="color: #7f8c8d; font-size: 18px;">Your account has been successfully verified. You can now log in to the application.</p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# =====================================================================
# 1. 2. SESSION MANAGEMENT (Login, Refresh, Logout)
# =====================================================================


@router.post("/sign_in", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def sign_in(user: UserSignIn, db: AsyncSession = Depends(get_db)):
    return await auth_service.sign_in(db, user)


@router.get("/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def refresh_token(
    db: AsyncSession = Depends(get_db),
    token: RefreshTokenResponse = Depends(get_refresh_session),
):
    return auth_service.refresh_token(db, token)


@router.post(
    "/sign_out", status_code=status.HTTP_200_OK, response_model=MessageResponse
)
async def sign_out(
    is_all: bool,
    db: AsyncSession = Depends(get_db),
    token: RefreshTokenResponse = Depends(get_refresh_session),
):
    return await auth_service.sign_out(db, token, is_all)


# =====================================================================
# 3. ACCOUNT RECOVERY (Forgot & Reset Password)
# =====================================================================


@router.post("/reset", status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def password_reset(
    user: PasswordReset,
    db: AsyncSession = Depends(get_db),
    cache_db: CacheDB = Depends(get_cache_db),
):
    return await auth_service.password_reset(db, cache_db, user)


@router.patch(
    "/reset",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    # include_in_schema=False,
)
async def verify_for_reset(
    token: UUID,
    user:PasswordVerify,
    db: AsyncSession = Depends(get_db),
    cache_db: CacheDB = Depends(get_cache_db),
):
    await auth_service.verify_for_reset(db, cache_db, token,user)
    html_content = """
    <html>
        <head>
            <title>IoT Dashboard | Success</title>
        </head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 100px; background-color: #f4f7f6;">
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
