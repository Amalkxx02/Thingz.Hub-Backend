from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cache import CacheDB
from app.things.schemas import (
    EdgeThingzRequest,
    UpdateThingRequest,
    ThingResponse,
    ThingUpdateResponse,
    ThingToggleResponse,
)
from app.common.response import MessageResponse
from app.core.security import get_fingerprint
from app.utils.security import generate_secure_string, to_uuid_4_by_str
from app.things import crud as crud_thing


async def registration(
    db: AsyncSession, device_id: UUID, thingz: list[EdgeThingzRequest]
) -> MessageResponse:
    payload = [{**thing.model_dump(), "device_id": device_id} for thing in thingz]
    await crud_thing.add_thingz(db, payload)
    return MessageResponse(message="Things registered successfully.")


async def device_thing(
    db: AsyncSession, device_id: UUID, user_id: UUID
) -> list[ThingResponse]:
    things = await crud_thing.device_thingz(db, device_id, user_id)
    return [ThingResponse.model_validate(t) for t in things]


async def user_thing(db: AsyncSession, user_id: UUID) -> list[ThingResponse]:
    things = await crud_thing.user_thingz(db, user_id)
    return [ThingResponse.model_validate(t) for t in things]


async def toggle_thing(
    db: AsyncSession, thing_id: UUID, user_id: UUID
) -> ThingToggleResponse:
    is_active = await crud_thing.toggle_active(db, thing_id, user_id)
    return ThingToggleResponse(is_active=is_active)


async def update(
    db: AsyncSession, thing_id: UUID, user_id: UUID, thing: UpdateThingRequest
) -> ThingUpdateResponse:
    payload = thing.model_dump(exclude_none=True)
    result = await crud_thing.update_thing(db, thing_id, user_id, payload)
    return ThingUpdateResponse(name=result.name, unit=result.unit)


async def delete(db: AsyncSession, thing_id: UUID, user_id: UUID) -> MessageResponse:
    if not await crud_thing.delete_by_id(db, thing_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thing not found, or you do not have permission to delete it.",
        )
    return MessageResponse(message="Thing deleted successfully.")
