from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import CacheDB, get_cache_db
from app.schemas.device import DeviceRequest,EdgeDeviceRequest
from app.core.security.dependency import get_current_device, get_current_user
from app.services.device import device_service
from app.database.session import get_db

router = APIRouter()


@router.post("")
async def add_a_device(
    onboard: DeviceRequest,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return await device_service.register(db, onboard.model_dump(), user_id)


@router.get("/{device_id}")
async def get_a_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return await device_service.get(db, device_id, user_id)


@router.get("")
async def get_all_device(
    db: AsyncSession = Depends(get_db), user_id: UUID = Depends(get_current_user)
):
    return await device_service.get_all(db, user_id)


@router.patch("/{device_id}/status")
async def toggle_a_device_status(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return await device_service.toggle_device(db, device_id, user_id)


@router.patch("/{device_id}/key")
async def rotate_a_device_key(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return await device_service.rotate_key(db, device_id, user_id)


@router.patch("/{device_id}/revoked")
async def revoke_a_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return await device_service.revoke_key(db, user_id, device_id)


@router.patch("/revoked")
async def revoke_all_device(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return await device_service.revoke_key(db, user_id)


@router.delete("/{device_id}")
async def delete_a_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user),
):
    return await device_service.delete(db, device_id, user_id)



# ------------------Device Server--------------------#
@router.post("/verify")
async def verify_device(
    device: EdgeDeviceRequest,
    cache:CacheDB = Depends(get_cache_db),
    db: AsyncSession = Depends(get_db)
):
    return await device_service.verify_device(db,cache,device)
