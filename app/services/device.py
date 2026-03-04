from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.device import crud_device
from app.database import CacheDB
from app.schemas.device import EdgeDeviceRequest
from app.security.generators import generate_api_key, mask_value
from app.security.hashing import get_fingerprint
from app.utils.security import generate_secure_string, to_uuid_4_by_str


class DeviceService:

    @staticmethod
    async def get(db: AsyncSession, device_id: UUID, user_id: UUID):
        return await crud_device.get_by_id(db, device_id, user_id)

    @staticmethod
    async def get_all(db: AsyncSession, user_id: UUID):
        return await crud_device.get_by_user(db, user_id)

    @staticmethod
    async def register(db: AsyncSession, payload: dict, user_id: UUID):

        api_key = generate_api_key()
        masked_key = mask_value(api_key)
        hashed_key = get_fingerprint(api_key)
        payload.update(
            {"user_id": user_id, "hashed_key": hashed_key, "key_hint": masked_key}
        )
        device_id = await crud_device.register(db, payload)
        return {"device_id": device_id, "api_key": api_key}

    @staticmethod
    async def rotate_key(db: AsyncSession, device_id: UUID, user_id: UUID):

        api_key = generate_api_key()
        masked_key = mask_value(api_key)
        hashed_key = get_fingerprint(api_key)
        payload = {"hashed_key": hashed_key, "key_hint": masked_key}

        await crud_device.rotate_key(db, payload, device_id, user_id)
        return {"api_key": api_key}

    @staticmethod
    async def revoke_key(db: AsyncSession, user_id: UUID, device_id: UUID = None):
        if device_id:
            await crud_device.revoke(db, device_id, user_id)
        else:
            await crud_device.revoke_all(db, user_id)

    @staticmethod
    async def toggle_device(db: AsyncSession, device_id: UUID, user_id: UUID):
        return await crud_device.toggle_active(db, device_id, user_id)

    @staticmethod
    async def delete(db: AsyncSession, device_id: UUID):
        await crud_device.delete(db, device_id)


# -------------------------------------------------------------- #
    @staticmethod
    async def verify_api_key(db: AsyncSession, api_key: str):
        hashed_key = get_fingerprint(api_key)
        result = await crud_device.verify_key(db, hashed_key)
        if not result:
            return False
        return result.id

    @staticmethod
    async def verify_device(db: AsyncSession, cache: CacheDB, device: EdgeDeviceRequest):

        device_id_from_edge = to_uuid_4_by_str(device.id)
        device_id_from_db = await device_service.verify_api_key(db,device.key)

        if not device_id_from_db:
            return False

        if not device_id_from_edge == device_id_from_db:
            return False
        
        cache.set(device_id_from_db,generate_secure_string()) 
        
        return cache.get(device_id_from_db)


device_service = DeviceService()
