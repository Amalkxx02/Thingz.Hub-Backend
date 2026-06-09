from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update
from app.models.device import Device
from uuid import UUID


async def verify_key(db: AsyncSession, api_key: bytes):
    return await db.scalar(
        select(Device).where(
            Device.hashed_key == api_key,
            Device.revoked == False,
            Device.is_active == True,
        )
    )


async def get_masked_key(db: AsyncSession, user_id: UUID):
    return await db.scalar(
        select(Device.key_hint, Device.revoked).where(Device.user_id == user_id)
    )


async def get_by_id(db: AsyncSession, device_id: UUID, user_id: UUID):
    return await db.scalar(
        select(Device).where(Device.id == device_id, Device.user_id == user_id)
    )


async def get_by_user(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(Device).where(Device.user_id == user_id))
    return result.scalars().all()


async def get_only_by_device_id(db: AsyncSession, device_id: UUID):
    return await db.scalar(select(Device).where(Device.id == device_id))


async def revoke(db: AsyncSession, device_id: UUID, user_id: UUID):
    stmt = (
        update(Device)
        .where(Device.id == device_id, Device.user_id == user_id)
        .values(revoked=True, is_active=False)
    )
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def revoke_all(db: AsyncSession, user_id: UUID):
    stmt = update(Device).where(Device.user_id == user_id).values(revoked=True)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def register(db: AsyncSession, payload: dict):
    stmt = insert(Device).values(**payload).returning(Device.id)
    try:
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    except Exception as e:
        await db.rollback()
        raise e


async def rotate_key(db: AsyncSession, payload: dict, device_id: UUID, user_id: UUID):
    stmt = (
        update(Device)
        .where(Device.id == device_id, Device.user_id == user_id)
        .values(**payload)
    )
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def toggle_active(db: AsyncSession, device_id: UUID, user_id: UUID):
    stmt = (
        update(Device)
        .where(
            Device.id == device_id,
            Device.user_id == user_id,
        )
        .values(is_active=~Device.is_active)
        .returning(Device.is_active)
    )
    try:
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    except Exception as e:
        await db.rollback()
        raise e


async def delete(db: AsyncSession, device_id: UUID):
    stmt = delete(Device).where(Device.id == device_id)

    try:
        result = await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
