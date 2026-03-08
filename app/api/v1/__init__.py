from fastapi import APIRouter

api_router = APIRouter()

from app.api.v1.routes import auth, device, user, thing, data_handle

api_router.include_router(auth.router, prefix="/auths", tags=["Auths"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(device.router, prefix="/devices", tags=["Devices"])
api_router.include_router(thing.router, prefix="/thingz", tags=["Thingz"])
api_router.include_router(data_handle.router,prefix="/websocket",tags=["WS"])
