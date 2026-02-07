"""
devices.py
----------
Manages User Device APIs for the IoT Dashboard.

Endpoints:
- POST /api/user/{user_id}/devices
    → Adds a new device entry for a given user.

Notes:
- Security: Authentication currently relies on raw user_id in the path.
            This is insecure and should be replaced with JWT-based authentication in production.

- Future:
    - Implement GET endpoint to fetch all devices for a user.
    - Add optional metadata for devices (e.g., location, status).
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from schemas.schemas import DeviceAdd
from models.models import Device
from utils.jwt_utils import verify_access_token
from utils.database_utils import get_db, db_execution

router = APIRouter(prefix="/api/user/devices", tags=["device"])


@router.post(
    "",
    summary="Add a device for a user",
    response_description="Device added confirmation",
)
async def add_device_for_user(
    device: DeviceAdd,
    db: AsyncSession = Depends(get_db),
    user_id=Depends(verify_access_token),
):
    """
    Add a new device under a specific user.

    Parameters:
    - user_id (UUID): Unique identifier of the user.
    - device (DeviceAdd): Device information including:
        - device_id: UUID of the device
        - device_name: Human-readable name
    - db (AsyncSession): Async database session (injected via FastAPI dependency).

    Raises:
    - HTTPException (409):
        - If user does not exist (user_check raises internally)
        - If the device already exists (duplicate device_id)

    Notes:
    - Uses `on_conflict_do_nothing` to ignore duplicate entries safely.
    - There is a database-level unique constraint on `user_id + device_id`.
    - Currently insecure: user_id in path → should switch to JWT auth.

    Returns:
        dict: Success message
        Example:
            {
                "message": "Device added successfully"
            }

    Future Improvements:
    - Replace `user_id` in path with JWT token to securely identify user.
    - Implement GET endpoint to list all devices for a user.
    """
    # Insert device safely (ignore duplicates)
    query = (
        insert(Device)
        .values(
            user_id=user_id,
            device_id=device.device_id,
            device_name=device.device_name,
        )
        .on_conflict_do_nothing(index_elements=["device_id"])
        .returning(Device)
    )

    # Execute query
    row = await db_execution(query, db)
    if row is None:
        raise HTTPException(status_code=409, detail="The device already exists")

    return {"message": "Device added successfully"}
