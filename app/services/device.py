from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import device as crud_device

from app.database.cache_db import CacheDB
from app.schemas.device import (
    EdgeDeviceRequest,
    DeviceResponse,
    DeviceRegisterResponse,
    DeviceToggleResponse,
    DeviceVerifyResponse,
)
from app.schemas.response import MessageResponse
from app.security.generators import generate_api_key, mask_value
from app.security.hashing import get_fingerprint
from app.utils.security import generate_secure_string, to_uuid_4_by_str


async def get(db: AsyncSession, device_id: UUID, user_id: UUID) -> DeviceResponse:
    device = await crud_device.get_by_id(db, device_id, user_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found or unauthorized access",
        )

    return DeviceResponse.model_validate(device)


async def get_all(db: AsyncSession, user_id: UUID) -> list[DeviceResponse]:
    devices = await crud_device.get_by_user(db, user_id)
    if not devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devices not found or unauthorized access",
        )
    return [DeviceResponse.model_validate(d) for d in devices]


async def revoke_status(db: AsyncSession, device_id: UUID, user_id: UUID) -> bool:
    device = await crud_device.get_by_id(db, device_id, user_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devices not found or unauthorized access",
        )
    return device.revoked


async def register(
    db: AsyncSession, payload: dict, user_id: UUID
) -> DeviceRegisterResponse:
    api_key = generate_api_key()
    masked_key = mask_value(api_key)
    hashed_key = get_fingerprint(api_key)
    payload.update(
        {"user_id": user_id, "hashed_key": hashed_key, "key_hint": masked_key}
    )
    device_id = await crud_device.register(db, payload)
    return DeviceRegisterResponse(device_id=device_id, api_key=api_key)


async def rotate_key(
    db: AsyncSession, device_id: UUID, user_id: UUID
) -> DeviceRegisterResponse:
    api_key = generate_api_key()
    masked_key = mask_value(api_key)
    hashed_key = get_fingerprint(api_key)
    payload = {
        "hashed_key": hashed_key,
        "key_hint": masked_key,
        "revoked": False,
        "is_active": True,
    }

    if not await crud_device.rotate_key(db, payload, device_id, user_id):
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found, or you do not have permission to rotate key of device",
            )
    return DeviceRegisterResponse(device_id=device_id, api_key=api_key)


async def revoke_key(
    db: AsyncSession, user_id: UUID, device_id: UUID = None
) -> MessageResponse:
    if device_id:
        result = await crud_device.revoke(db, device_id, user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found, or you do not have permission to revoke this device",
            )
        return MessageResponse(
            message="Device revoked successfully, or already revoked."
        )
    else:
        await crud_device.revoke_all(db, user_id)
        return MessageResponse(message="All devices revoked successfully.")


async def toggle_device(
    db: AsyncSession, device_id: UUID, user_id: UUID
) -> DeviceToggleResponse:
    is_active = await crud_device.toggle_active(db, device_id, user_id)
    if await revoke_status(db, device_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Device is revoked. Please contact support.",
        )
    return DeviceToggleResponse(is_active=is_active)


async def delete(db: AsyncSession, device_id: UUID, user_id: UUID) -> MessageResponse:
    if not await crud_device.delete_by_id(db, device_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devices not found or unauthorized access",
        )
    return MessageResponse(message="Device deleted successfully.")


# -------------------------------------------------------------- #
async def verify_api_key(db: AsyncSession, api_key: str):
    hashed_key = get_fingerprint(api_key)
    result = await crud_device.verify_key(db, hashed_key)
    if not result:
        return False
    return result.id


async def verify_device(
    db: AsyncSession, cache: CacheDB, device: EdgeDeviceRequest
) -> DeviceVerifyResponse:

    device_id_from_db = await verify_api_key(db, device.key)

    if not device_id_from_db:
        return DeviceVerifyResponse(verified=False)

    if not device.id == device_id_from_db:
        return DeviceVerifyResponse(verified=False)

    await cache.set(device_id_from_db, generate_secure_string())
    session_token = await cache.get(device_id_from_db)

    return DeviceVerifyResponse(session_token, True)
