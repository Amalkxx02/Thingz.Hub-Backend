from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import StatementError
from app.things.models import Thing
from app.devices.models import Device
from uuid import UUID

from app.utils.decorators import handle_db_errors


@handle_db_errors
async def add_thingz(db: AsyncSession, payload: list):
    stmt = (
        insert(Thing)
        .values(payload)
        .on_conflict_do_nothing(
            index_elements=["device_id", "hardware_address", "slug"]
        )
    )

    await db.execute(stmt)
    await db.commit()


@handle_db_errors
async def device_thingz(db: AsyncSession, device_id: UUID, user_id: UUID):
    result = await db.execute(
        select(Thing)
        .join(Device, Thing.device_id == Device.id)
        .where(Thing.device_id == device_id, Device.user_id == user_id)
    )
    return result.scalars().all()


@handle_db_errors
async def user_thingz(db: AsyncSession, user_id: UUID):
    result = await db.execute(
        select(Thing).where(
            Thing.device_id.in_(select(Device.id).where(Device.user_id == user_id))
        )
    )
    return result.scalars().all()


# messy code need to fix
@handle_db_errors
async def update_thing(db: AsyncSession, thing_id: UUID, user_id: UUID, payload: dict):
    stmt = (
        update(Thing)
        .where(
            Thing.id == thing_id,
            Thing.device_id.in_(select(Device.id).where(Device.user_id == user_id)),
        )
        .values(**payload)
        .returning(Thing.name, Thing.unit)
    )
    try:
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            await db.rollback()
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No thing found to update")
        await db.commit()
        return result.scalar_one()
    except StatementError as e:
        await db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid input: {str(e)}")


@handle_db_errors
async def toggle_active(db: AsyncSession, thing_id: UUID, user_id: UUID):
    stmt = (
        update(Thing)
        .where(
            Thing.id == thing_id,
            Thing.device_id.in_(select(Device.id).where(Device.user_id == user_id)),
        )
        .values(is_active=~Thing.is_active)
        .returning(Thing.is_active)
    )

    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()


@handle_db_errors
async def delete_by_id(db: AsyncSession, thing_id: UUID, user_id: UUID):
    stmt = delete(Thing).where(
        Thing.id == thing_id,
        Thing.device_id.in_(select(Device.id).where(Device.user_id == user_id))
    ).returning(Thing.id)

    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()
