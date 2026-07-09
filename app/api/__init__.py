from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.users.router import router as user_router
from app.devices.router import router as device_router
from app.things.router import router as thing_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auths", tags=["Auths"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(device_router, prefix="/devices", tags=["Devices"])
api_router.include_router(thing_router, prefix="/things", tags=["Things"])
# api_router.include_router(data_handle.router, prefix="/websocket", tags=["WS"])
