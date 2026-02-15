from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.device import DeviceRequest
from app.security.jwt.dependency import get_current_user
from app.services.device import device_service
from app.database.session import get_db

router = APIRouter()

@router.post("/user")
async def user_provision_device(
    onboard: DeviceRequest,
    db: AsyncSession = Depends(get_db),
    user_id:UUID = Depends(get_current_user)  
):
    return await device_service.register(db,onboard.model_dump(),user_id)

@router.post("/edge_device")
async def device_handshake(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id:UUID = Depends(get_current_user)  
):
    return await device_service.activate(db,device_id,user_id)

@router.post("/deactivate")
async def device_handshake(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id:UUID = Depends(get_current_user)  
):
    return await device_service.deactivate(db,device_id,user_id)

