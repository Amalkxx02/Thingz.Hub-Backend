# Third-Party
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# Database & Core
from app.core.cache import CacheDB, get_cache_db
from app.core.database import get_db

# Schemas
from app.devices.schemas import DeviceVerifyResponse, EdgeDeviceRequest

# Services
from app.devices import service as device_service

router = APIRouter()


# =====================================================================
# 1. EDGE TELEMETRY & AUTHENTICATION (Machine-to-Machine)
# =====================================================================

@router.post("/auth/verify", response_model=DeviceVerifyResponse, status_code=status.HTTP_200_OK)
async def verify_edge_hardware_handshake(
    payload: EdgeDeviceRequest,
    cache: CacheDB = Depends(get_cache_db),
    db: AsyncSession = Depends(get_db),
):
    """Edge Unit Handshake: Authenticates physical hardware via raw API secret."""
    return await device_service.verify_device(db, cache, payload)