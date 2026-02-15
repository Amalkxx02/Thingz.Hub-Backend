from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update
from app.models.device import Device
from uuid import UUID


class CRUDDevice:

    @staticmethod
    async def get_by_id(db: AsyncSession, device_id: UUID):
        return await db.scalar(select(Device).where(Device.id == device_id))

    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: UUID):
        return await db.scalar(select(Device).where(Device.user_id == user_id))

    @staticmethod
    async def register(db: AsyncSession, payload: dict):
        stmt = insert(Device).values(**payload)
        try:
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def toggle_active(db: AsyncSession, device_id: UUID, user_id: UUID,active:bool):
        stmt = (
            update(Device)
            .where(
                Device.id == device_id,
                Device.user_id == user_id,
                Device.active == (not active)
            )
            .values(active=active)
        )
        try:
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def delete(db: AsyncSession, device_id: UUID):
        stmt = delete(Device).where(Device.id == device_id)

        try:
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            await db.rollback()
            raise e


crud_device = CRUDDevice()
