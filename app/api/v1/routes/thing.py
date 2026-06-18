from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.thing import (
    EdgeThingzRequest,
    UpdateThingRequest,
    ThingResponse,
    ThingUpdateResponse,
    ThingToggleResponse,
)
from app.schemas.response import MessageResponse
from app.core.jwt.dependency import verify_device_session, get_verified_user_id
from app.services import thing as thingz_service
from app.database.session import get_db

router = APIRouter()


@router.post("", response_model=MessageResponse)
async def registration(
    thingz: list[EdgeThingzRequest],
    device_id: UUID = Depends(verify_device_session),
    db: AsyncSession = Depends(get_db),
):
    return await thingz_service.registration(db, device_id, thingz)


@router.get("", response_model=list[ThingResponse])
async def get_by_user(
    db: AsyncSession = Depends(get_db), user_id: UUID = Depends(get_verified_user_id)
):
    return await thingz_service.user_thing(db, user_id)


@router.get("/{device_id}", response_model=list[ThingResponse])
async def get_by_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await thingz_service.device_thing(db, device_id, user_id)


@router.patch("/{thing_id}", response_model=ThingUpdateResponse)
async def update_a_thing(
    thing_id: UUID,
    thing: UpdateThingRequest,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await thingz_service.update(db, thing_id, user_id, thing)


@router.patch("/{thing_id}/status", response_model=ThingToggleResponse)
async def toggle_a_thing_status(
    thing_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await thingz_service.toggle_thing(db, thing_id, user_id)


@router.delete("/{thing_id}", response_model=MessageResponse)
async def delete_a_thing(
    thing_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_verified_user_id),
):
    return await thingz_service.delete(db, thing_id, user_id)
