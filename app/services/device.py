from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.device import crud_device

class DeviceService:

    @staticmethod
    async def get(db: AsyncSession, device_id: UUID):
        return await crud_device.get_by_id(db,device_id)

    @staticmethod
    async def get_all(db: AsyncSession, user_id: UUID):
        return await crud_device.get_by_id(db,user_id)

    @staticmethod
    async def register(db: AsyncSession, payload: dict,user_id: UUID):
        payload["user_id"] = user_id
        return await crud_device.register(db,payload)
    
    @staticmethod
    async def activate(db: AsyncSession, device_id: UUID,user_id: UUID):
        return await crud_device.toggle_active(db,device_id,user_id,True)
    
    @staticmethod
    async def deactivate(db: AsyncSession, device_id: UUID,user_id: UUID):
        return await crud_device.toggle_active(db,device_id,user_id,True)
    
    @staticmethod
    async def delete(db: AsyncSession, device_id: UUID):
        return await crud_device.delete(db,device_id)


device_service = DeviceService()
