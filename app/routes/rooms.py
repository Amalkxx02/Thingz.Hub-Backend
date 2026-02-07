"""
rooms.py
---------
Manages user rooms APIs.

Endpoints:
1. POST /api/user/{user_id}/rooms
   - Adds a new room for a specific user.
   - Ensures room names are unique per user.
2. GET /api/user/{user_id}/rooms
   - Lists all rooms of a specific user.

Notes:
- Security: Currently relies on raw user_id in path, which is insecure.
            Should be replaced with JWT-based authentication in production.
- Future:
    - Add update/delete room endpoints.
    - Integrate with user dashboard to link Things to rooms.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from uuid import UUID

from schemas.schemas import Room as RoomSchema
from models.models import Room
from utils.user_utils import user_check
from utils.database_utils import get_db, db_execution

router = APIRouter(prefix="/api/user/{user_id}/rooms", tags=["room"])


@router.post("")
async def add_room_for_user(
    user_id: UUID, room: RoomSchema, db: AsyncSession = Depends(get_db)
):
    """
    Add a new room for a specific user.

    Args:
        user_id (UUID): User identifier
        room (RoomSchema): Room data (name, color)
        db (AsyncSession): Database session

    Raises:
        HTTPException 409:
            - User does not exist
            - Room with the same name already exists

    Returns:
        dict: Success message
    """
    # Validate user existence
    await user_check(user_id, db)

    # Prepare insert query with conflict handling
    query = (
        insert(Room)
        .values(user_id=user_id, room_name=room.room_name, room_color=room.room_color)
        .on_conflict_do_nothing(index_elements=["user_id", "room_name"])
        .returning(Room.room_name)
    )

    result = await db.execute(query)
    row = result.scalar()

    if row is None:
        raise HTTPException(status_code=409, detail="The room already exists")

    await db.commit()
    return {"message": "Room added successfully"}


@router.get("")
async def get_room_for_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    List all rooms for a specific user.

    Args:
        user_id (UUID): User identifier
        db (AsyncSession): Database session

    Returns:
        list[dict]: List of rooms with id, name, and color.
    """
    # Validate user existence
    await user_check(user_id, db)

    query = select(Room.room_id, Room.room_name, Room.room_color).where(
        Room.user_id == user_id
    )
    result = await db.execute(query)
    rows = result.mappings().all()

    return rows
