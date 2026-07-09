from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.schemas import PaginationParams
from app.devices import crud as device_crud

from app.core.cache import CacheDB
from app.devices.schemas import (
    DeviceFilter,
    DeviceKeyRotationModel,
    DeviceListResponse,
    DeviceModel,
    DeviceRequest,
    EdgeDeviceModel,
    EdgeDeviceRequest,
    DeviceResponse,
    DeviceRegisterResponse,
    DeviceToggleResponse,
    DeviceVerifyResponse,
)
from app.common.response import MessageResponse
from app.core.security import generate_api_key, mask_value
from app.core.security import get_fingerprint
from app.utils.security import generate_secure_string, to_uuid_4_by_str


# =====================================================================
# 0. READ SERVICE
# =====================================================================
async def get_device_by_id(
    db: AsyncSession, device_id: UUID, user_id: UUID
) -> DeviceResponse:
    device = await device_crud.get_device_by_id(db, device_id, user_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found or unauthorized access",
        )

    return DeviceResponse.model_validate(device)


async def list_devices_by_user_id(
    db: AsyncSession, pagination: PaginationParams, filter: DeviceFilter, user_id: UUID
) -> list[DeviceResponse | None]:
    filters = filter.model_dump(exclude_none=True)
    devices = await device_crud.list_devices_by_user_id(
        db, pagination, filters, user_id
    )
    return [DeviceListResponse.model_validate(d) for d in devices] if devices else []


# async def revoke_status(db: AsyncSession, device_id: UUID, user_id: UUID) -> bool:
#     device = await device_crud.get_device_by_id(db, device_id, user_id)
#     if not device:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Devices not found or unauthorized access",
#         )
#     return device.is_revoked

# =====================================================================
# 1. CREATE SERVICE (Sign_up -> Verify)
# =====================================================================


async def create_device(
    db: AsyncSession, device: DeviceRequest, user_id: UUID
) -> DeviceRegisterResponse:
    api_key = generate_api_key()
    masked_key = mask_value(api_key)
    hashed_key = get_fingerprint(api_key)
    device_data = DeviceModel(
        user_id=user_id,
        name=device.name,
        type=device.type,
        hashed_key=hashed_key,
        key_hint=masked_key,
    ).model_dump()

    device_id = await device_crud.create_device(db, device_data)
    return DeviceRegisterResponse(device_id=device_id, api_key=api_key)


# =====================================================================
# 1. UPDATE SERVICE (Sign_up -> Verify)
# =====================================================================


async def rotate_key_by_id(
    db: AsyncSession, device_id: UUID, user_id: UUID
) -> DeviceRegisterResponse:
    api_key = generate_api_key()
    masked_key = mask_value(api_key)
    hashed_key = get_fingerprint(api_key)

    device_data = DeviceKeyRotationModel(
        hashed_key=hashed_key, key_hint=masked_key
    ).model_dump()

    if not await device_crud.rotate_device_api_key(db, device_data, device_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found, or you do not have permission to rotate key of device",
        )
    return DeviceRegisterResponse(device_id=device_id, api_key=api_key)


async def revoke_key(
    db: AsyncSession, user_id: UUID, device_id: UUID = None
) -> MessageResponse:
    if device_id:
        result = await device_crud.revoke_device(db, device_id, user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found, or you do not have permission to revoke this device",
            )
        return MessageResponse(
            message="Device is_revoked successfully, or already is_revoked."
        )
    else:
        await device_crud.revoke_all_device(db, user_id)
        return MessageResponse(message="All devices is_revoked successfully.")


async def toggle_device_by_id(
    db: AsyncSession, device_id: UUID, user_id: UUID
) -> DeviceToggleResponse:
    is_active = await device_crud.toggle_device_state(db, device_id, user_id)
    if is_active is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Device is is_revoked or Not Found. Please contact support.",
        )
    return DeviceToggleResponse(is_active=is_active)


# =====================================================================
# 1. PURGE SERVICE
# =====================================================================


async def delete_device_by_id(
    db: AsyncSession, device_id: UUID, user_id: UUID
) -> MessageResponse:
    if not await device_crud.delete_device_by_id(db, device_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devices not found or unauthorized access",
        )
    return MessageResponse(message="Device deleted successfully.")


# =====================================================================
# 1. EDGE DEVICE SERVICE
# =====================================================================
async def verify_api_key(db: AsyncSession, api_key: str):
    hashed_key = get_fingerprint(api_key)
    device_id = await device_crud.get_device_by_api_key(db, hashed_key)
    if not device_id:
        return False
    return device_id


async def verify_device(
    db: AsyncSession, cache: CacheDB, device: EdgeDeviceRequest
) -> DeviceVerifyResponse:

    device_id = await verify_api_key(db, device.key)

    if not device_id:
        return DeviceVerifyResponse(verified=False)

    if not device.id == device_id:
        return DeviceVerifyResponse(verified=False)

    session_token = generate_secure_string()
    await cache.set(device_id, session_token)

    device_data = EdgeDeviceModel(
        mac_address=device.mac_address,
        firmware=device.firmware,
        ip_address=device.ip_address,
    ).model_dump()

    await device_crud.update_device(db, device_data, device_id)

    return DeviceVerifyResponse(session_token=session_token, verified=True)
