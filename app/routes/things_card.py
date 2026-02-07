"""
user_thing_cards.py
------------------
Manages user "thing cards" APIs.

Endpoints:
1. POST /api/user/{user_id}/userThingzCards
    - Adds a new thing card for a user.
    - Handles duplicates via `on_conflict_do_nothing`.

2. GET /api/user/{user_id}/userThingzCards
    - Fetches all thing cards for a user.

Notes:
- Future:
    - Add update endpoint for modifying card configurations.
    - Add deletion endpoint for removing cards.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from schemas.schemas import ThingCardAdd
from models.models import ThingCard

from utils.database_utils import get_db, db_execution
from utils.jwt_utils import verify_access_token

router = APIRouter(prefix="/api/user/thingsCard", tags=["ThingCard"])


@router.post("")
async def add_thing_card_for_user(
    thing_card: ThingCardAdd,
    db: AsyncSession = Depends(get_db),
    user_id=Depends(verify_access_token),
):
    """
    Add a new user "thing card".

    Args:
        user_id (UUID): The user's unique identifier.
        thing_card (ThingCardAdd): Thing card data including:
            - thing_id: UUID of the associated thing
            - thing_config: User-defined configuration for this card
        db (AsyncSession): Async SQLAlchemy session (dependency injected)

    Raises:
        HTTPException (409): If the card already exists for the user (`user_id` + `thing_id`)

    Returns:
        dict: Success message
        Example:
            {
                "status": "ok"
            }
    """

    # Insert card safely, ignoring duplicates
    query = (
        insert(ThingCard)
        .values(
            user_id=user_id,
            thing_id=thing_card.thing_id,
            config=thing_card.thing_config,
        )
        .on_conflict_do_nothing(index_elements=["user_id", "thing_id"])
        .returning(ThingCard)
    )

    row = await db_execution(query, db)

    if row is None:
        raise HTTPException(status_code=409, detail="The card already exists")

    return {"status": "ok"}


@router.get("")
async def get_thing_card_for_user(
    db: AsyncSession = Depends(get_db),
    user_id=Depends(verify_access_token),
):
    """
    Retrieve all thing cards for a specific user.

    Args:
        user_id (UUID): The user's unique identifier.
        db (AsyncSession): Async SQLAlchemy session.

    Returns:
        list[dict]: List of thing cards with their configuration
        Example:
            [
                {"thing_id": "uuid1", "config": {...}},
                {"thing_id": "uuid2", "config": {...}}
            ]
    """

    # Select all thing cards for the user
    query = select(ThingCard.thing_id, ThingCard.config).where(
        ThingCard.user_id == user_id
    )

    rows = await db_execution(query, db, get_single_row=False)

    return rows
