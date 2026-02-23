from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import AuthIn
from app.core.security.dependency import get_refresh
from app.services.auth import auth_service
from app.database.session import get_db

router = APIRouter()


@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def sign_up(
    user_in: AuthIn,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.register(db, user_in.model_dump())


@router.post("/sign_in", status_code=status.HTTP_200_OK)
async def sign_in(user_in: AuthIn, db: AsyncSession = Depends(get_db)):
    return await auth_service.authenticate(db, user_in.model_dump())


@router.get("/verify", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def verify(token: UUID, db: AsyncSession = Depends(get_db)):
    await auth_service.verify(db, token)
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


@router.post("/sign_out/{is_all}", status_code=status.HTTP_200_OK)
async def sign_out(
    is_all:bool,db: AsyncSession = Depends(get_db),token_info:dict = Depends(get_refresh)
):
    await auth_service.sign_out(db,token_info,is_all)


@router.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(token_info: dict = Depends(get_refresh)):
    return token_info["token"]
