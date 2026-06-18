# Third-Party
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Database & Core
from app.database.session import get_db
from app.database.cache_db import CacheDB, get_cache_db
from app.core.jwt.dependency import verify_device_session, get_verified_user_id

# Schemas
from app.schemas.device import (
    DeviceRequest,
    EdgeDeviceRequest,
    DeviceResponse,
    DeviceRegisterResponse,
    DeviceToggleResponse,
    DeviceVerifyResponse,
)
from app.schemas.response import MessageResponse

# Services
from app.services import device as device_service

router = APIRouter()


# =====================================================================
# 👤 USER MANAGEMENT ENDPOINTS
# =====================================================================

@router.post("", response_model=DeviceRegisterResponse, status_code=201)
async def add_a_device(
    onboard: DeviceRequest,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await device_service.register(db, onboard.model_dump(), user_id)


@router.get("", response_model=list[DeviceResponse])
async def get_all_devices(
    db: AsyncSession = Depends(get_db), 
    user_id: UUID = Depends(get_verified_user_id)
):
    return await device_service.get_all(db, user_id)

@router.patch("/revoke", response_model=MessageResponse)
async def revoke_all_devices(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await device_service.revoke_key(db, user_id)


@router.get("/{device_id}", response_model=DeviceResponse | None)
async def get_a_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await device_service.get(db, device_id, user_id)


@router.patch("/{device_id}/status", response_model=DeviceToggleResponse)
async def toggle_a_device_status(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await device_service.toggle_device(db, device_id, user_id)


@router.patch("/{device_id}/key", response_model=DeviceRegisterResponse)
async def rotate_a_device_key(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await device_service.rotate_key(db, device_id, user_id)


@router.patch("/{device_id}/revoke", response_model=MessageResponse)
async def revoke_a_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await device_service.revoke_key(db, user_id, device_id)


@router.delete("/{device_id}", response_model=MessageResponse)
async def delete_a_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await device_service.delete(db, device_id, user_id)


# =====================================================================
#  EDGE DEVICE/SERVER INTERACTION ENDPOINTS
# =====================================================================

@router.post("/verify", response_model=DeviceVerifyResponse)
async def verify_device(
    device: EdgeDeviceRequest,
    cache: CacheDB = Depends(get_cache_db),
    db: AsyncSession = Depends(get_db),
):
    return await device_service.verify_device(db, cache, device)