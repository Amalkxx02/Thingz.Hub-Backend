"""API V1 Router"""
from fastapi import APIRouter

api_router = APIRouter()

from app.api.v1.routes import auth,user

api_router.include_router(auth.router, prefix="/auths", tags=["Auths"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
