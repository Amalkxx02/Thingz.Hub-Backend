import functools
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    DataError,
    ProgrammingError,
    OperationalError,
)
from fastapi import HTTPException, status

logger = logging.getLogger("root")


def handle_db_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        db: AsyncSession = kwargs.get("db") or next(
            (arg for arg in args if hasattr(arg, "rollback")), None
        )
        try:
            return await func(*args, **kwargs)

        except IntegrityError as e:
            if db:
                await db.rollback()
            error_msg = str(e.orig).lower()

            if "foreign key" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Related record not found (Foreign key violation).",
                )
            elif "duplicate key" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This record already exists (Unique constraint violation).",
                )
            elif "not-null" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A required field was left empty.",
                )
            elif "check constraint" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Provided data violates database validation rules.",
                )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database integrity error.",
            )

        except NoResultFound:
            if db:
                await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The requested resource does not exist.",
            )

        except DataError as e:
            if db:
                await db.rollback()
            logger.warning(f"DataError mismatch in {func.__name__}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data format provided (e.g., malformed UUID or invalid values).",
            )

        except (ProgrammingError, OperationalError) as e:
            # ProgrammingError: Bad SQL syntax, column doesn't exist (migrations missing)
            # OperationalError: Database connection lost, timed out, or disk full
            if db:
                await db.rollback()

            # CRITICAL: Log this as an ERROR because your code or infrastructure is broken.
            logger.error(
                f"Database infrastructure failure in {func.__name__}: {e}",
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal database service error.",
            )

        except Exception as e:
            # Catch-all safety net for unexpected non-SQL python errors inside your CRUD
            if db:
                await db.rollback()
            logger.error(
                f"Unexpected system exception in {func.__name__}: {e}", exc_info=True
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected server error occurred.",
            )

    return wrapper
