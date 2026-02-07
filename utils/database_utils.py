"""
database_utils.py
-----------------
Database utility functions for async operations with SQLAlchemy.

Includes:
- get_db: Async session dependency generator for FastAPI.
- db_execution: Safe execution of queries with commit/rollback handling.
"""

from fastapi import HTTPException
from app.database import async_session_local


async def get_db():
    """
    Async generator for SQLAlchemy session.

    Usage:
        async with get_db() as db:
            ...

    Yields:
        AsyncSession: Async database session

    Ensures:
        - Proper closure of the session after use.
    """
    db = async_session_local()
    try:
        yield db
    finally:
        await db.close()


async def db_execution(query, db, get_single_row: bool = True):
    """
    Execute a SQLAlchemy query safely with commit/rollback.

    Args:
        query: SQLAlchemy query object (insert, select, update, delete)
        db: AsyncSession
        get_single_row (bool): If True, returns the first row; else returns all rows

    Returns:
        dict | list[dict]: Query result mapping(s)

    Raises:
        HTTPException (404): If database operation fails

    Notes:
        - Commits the transaction after successful execution.
        - Rolls back on any exception to prevent partial commits.
        - Can be extended to log errors in production.
    """
    try:
        result = await db.execute(query)

        if get_single_row:
            row = result.mappings().first()
        else:
            row = result.mappings().all()

        await db.commit()
        
        return row

    except Exception as e:
        await db.rollback()
        # Need to use logging instead of exposing raw error in production
        raise HTTPException(
            status_code=404,
            detail=f"Internal database issue: {str(e)}. Retry after some time.",
        )
