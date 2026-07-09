# Third-Party
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# Database & Core
from app.api.dependencies import get_authenticated_user_id
from app.core.database import get_db

# Schemas
from app.common.response import MessageResponse
from app.devices.schemas import (
    DeviceListResponse,
    DeviceRegisterResponse,
    DeviceRequest,
    DeviceResponse,
    DeviceToggleResponse,
)

# Services
from app.devices import service as device_service

router = APIRouter()


# =====================================================================
# 1. COLLECTION FLEET MANAGEMENT (Dashboard Views & Global Actions)
# =====================================================================

@router.post("", response_model=DeviceRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_new_device(
    payload: DeviceRequest,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Pairs a new hardware unit to the user's dashboard account."""
    return await device_service.create_device(db, payload, user_id)


@router.get("", response_model=list[DeviceListResponse], status_code=status.HTTP_200_OK)
async def list_registered_devices(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Retrieves the full fleet of devices owned by the user."""
    return await device_service.list_devices_by_user_id(db, user_id)


@router.patch("/revoke-all", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def emergency_fleet_cutoff(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Emergency action: Instantly revokes API keys for all owned devices."""
    return await device_service.revoke_all_user_keys(db, user_id)


# =====================================================================
# 2. SINGLE UNIT CONTROLS (Individual Device Actions)
# =====================================================================

@router.get("/{device_id}", response_model=DeviceResponse, status_code=status.HTTP_200_OK)
async def get_device_details(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Fetches telemetry and status for a single unit. Raises 404 if missing."""
    return await device_service.get(db, device_id, user_id)


@router.patch("/{device_id}/status", response_model=DeviceToggleResponse, status_code=status.HTTP_200_OK)
async def toggle_device_power_switch(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Flips the active/inactive software kill-switch on a single unit."""
    return await device_service.toggle_device(db, device_id, user_id)


@router.patch("/{device_id}/rotate-key", response_model=DeviceRegisterResponse, status_code=status.HTTP_200_OK)
async def rotate_device_secret(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Issues a fresh hardware API key, immediately invalidating the old one."""
    return await device_service.rotate_key(db, device_id, user_id)


@router.patch("/{device_id}/revoke", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def revoke_single_device_access(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Revokes a single unit's API key without deleting its dashboard history."""
    return await device_service.revoke_single_key(db, device_id, user_id)


@router.delete("/{device_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def decommission_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_authenticated_user_id),
):
    """Permanently deletes a device and purges its mappings from the system."""
    return await device_service.delete(db, device_id, user_id)