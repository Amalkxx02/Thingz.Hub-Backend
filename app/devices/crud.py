from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, desc, select, insert, update
from app.common.schemas import PaginationParams
from app.devices.models import Device
from uuid import UUID

from app.utils.decorators import handle_db_errors


# =====================================================================
# 1. READ OPERATIONS
# =====================================================================
@handle_db_errors
async def get_device_by_id(db: AsyncSession, device_id: UUID, user_id: UUID):
    return await db.scalar(
        select(Device).where(Device.id == device_id, Device.user_id == user_id)
    )


@handle_db_errors
async def list_devices_by_user_id(
    db: AsyncSession, pagination: PaginationParams, payload: dict, user_id: UUID
):
    stmt = (
        select(
            Device.id,
            Device.name,
            Device.type,
            Device.is_revoked,
            Device.is_active,
            Device.is_registered,
        )
        .where(
            Device.user_id == user_id,
        )
        .order_by(desc(Device.created_at))
        .limit(pagination.size)
        .offset(pagination.offset)
    )

    for key, value in payload.items():
        stmt = stmt.where(getattr(Device, key) == value)

    result = await db.execute(stmt)
    return result.all()


@handle_db_errors
async def get_only_by_device_id(db: AsyncSession, device_id: UUID):
    return await db.scalar(select(Device).where(Device.id == device_id))


@handle_db_errors
async def get_device_by_api_key(db: AsyncSession, api_key: bytes):
    return await db.scalar(
        select(Device.id).where(
            Device.hashed_key == api_key,
            Device.is_revoked == False
        )
    )


@handle_db_errors
async def get_device_masked_key(db: AsyncSession, user_id: UUID):
    return await db.scalar(
        select(Device.key_hint, Device.is_revoked).where(Device.user_id == user_id)
    )


# =====================================================================
# 2. WRITE OPERATIONS (Create / Upsert)
# =====================================================================
@handle_db_errors
async def create_device(db: AsyncSession, payload: dict):
    stmt = insert(Device).values(**payload).returning(Device.id)
    device_id = await db.scalar(stmt)
    await db.commit()
    return device_id


# =====================================================================
# 3. UPDATE OPERATIONS (Revoke, Rotate key, Toggle)
# =====================================================================
@handle_db_errors
async def update_device(db: AsyncSession, payload: dict, device_id: UUID):
    stmt = update(Device).values(**payload).where(Device.id == device_id)
    await db.execute(stmt)
    await db.commit()
    


@handle_db_errors
async def revoke_device(db: AsyncSession, device_id: UUID, user_id: UUID):
    stmt = (
        update(Device)
        .where(Device.id == device_id, Device.user_id == user_id)
        .values(is_revoked=True, is_active=False)
    ).returning(Device.is_revoked)
    return await db.scalar(stmt)



@handle_db_errors
async def revoke_all_device(db: AsyncSession, user_id: UUID):
    stmt = update(Device).where(Device.user_id == user_id).values(is_revoked=True)

    await db.execute(stmt)
    await db.commit()


@handle_db_errors
async def rotate_device_api_key(
    db: AsyncSession, payload: dict, device_id: UUID, user_id: UUID
):
    stmt = (
        update(Device)
        .where(Device.id == device_id, Device.user_id == user_id)
        .values(**payload)
        .returning(Device.id)
    )

    return await db.scalar(stmt)


@handle_db_errors
async def toggle_device_state(db: AsyncSession, device_id: UUID, user_id: UUID):
    return await db.scalar(
        update(Device)
        .where(
            Device.id == device_id,
            Device.user_id == user_id,
            Device.is_revoked == False,
        )
        .values(is_active=~Device.is_active)
        .returning(Device.is_active)
    )


# =====================================================================
# 4. DELETE OPERATIONS
# =====================================================================


@handle_db_errors
async def delete_device_by_id(db: AsyncSession, device_id: UUID, user_id: UUID):
    return await db.scalar(
        delete(Device)
        .where(
            Device.id == device_id,
            Device.user_id == user_id,
        )
        .returning(Device.id)
    )
