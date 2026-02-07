"""
thing_utils.py
---------------
Utility functions for managing and validating Things and Devices.
"""

from sqlalchemy import select
from fastapi import HTTPException
from models.models import Device
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


async def device_check(device_id: UUID, db: AsyncSession) -> Device:
    """
    Validate that a device exists in the database.

    Args:
        device_id (UUID): The device identifier to check
        db (AsyncSession): Async SQLAlchemy session

    Returns:
        Device: The Device object from the database

    Raises:
        HTTPException 400: If the device does not exist

    Notes:
        - Can be reused in any endpoint that requires device validation.
        - Returns the full Device object for further operations.
    """
    device = await db.scalar(select(Device).where(Device.device_id == device_id))
    if device is None:
        raise HTTPException(status_code=400, detail="The Device does not exist")
    return device
