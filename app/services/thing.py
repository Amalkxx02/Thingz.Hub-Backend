from uuid import UUID
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import CacheDB
from app.schemas.thing import EdgeThingzRequest, UpdateThingRequest
from app.security.hashing import get_fingerprint
from app.utils.security import generate_secure_string, to_uuid_4_by_str
from app.crud.thing import crud_thing


class ThingzService:

    @staticmethod
    async def registration(
        db: AsyncSession, device_id: UUID, thingz: list[EdgeThingzRequest]
    ):
        payload = [
            {**thing.model_dump(), "device_id": device_id}
            for thing in thingz
        ]
        print(payload)
        await crud_thing.add_thingz(db, payload)

    @staticmethod
    async def device_thing(db: AsyncSession, device_id: UUID, user_id: UUID):
        return await crud_thing.device_thingz(db, device_id, user_id)

    @staticmethod
    async def user_thing(db: AsyncSession, user_id: UUID):
        return await crud_thing.user_thingz(db, user_id)

    @staticmethod
    async def toggle_thing(db: AsyncSession, thing_id: UUID, user_id: UUID):
        return await crud_thing.toggle_active(db, thing_id, user_id)

    @staticmethod
    async def update(
        db: AsyncSession, thing_id: UUID, user_id: UUID,thing:UpdateThingRequest
    ):
        payload = thing.model_dump(exclude_none=True)
        return await crud_thing.update_thing(db, thing_id, user_id,payload)

    @staticmethod
    async def delete(db: AsyncSession, thing_id: UUID, user_id: UUID):
        await crud_thing.delete(db, thing_id, user_id)

thingz_service = ThingzService()
