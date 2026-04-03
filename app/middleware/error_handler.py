# Third-Party Imports
from fastapi import Request, status, HTTPException
from fastapi.exceptions import RequestValidationError

import logging


class ExceptionHelper(Exception):
    def __init__(
        self,
        status_code: int,
        error: str,
        message: str,
        data: dict | None = None,
        **kwargs,
    ):
        self.status_code = status_code
        self.error = error
        self.message = message
        self.data = data or {}
        self.extra = kwargs


async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled Error: {str(exc)}", exc_info=True)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred.",
    )


async def custom_exception_handler(request: Request, exc: ExceptionHelper):
    raise HTTPException(
        status_code=exc.status_code,
        detail=(exc.message),
    )


async def custom_validation_error_handler(
    request: Request, exc: RequestValidationError
):
    error = exc.errors()[0]
    logging.error(f"Validation error: {error}", exc_info=False)
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail=error.get("msg", "Invalid input"),
    )


def setup_exception_handlers(app):
    app.add_exception_handler(ExceptionHelper, custom_exception_handler)
    app.add_exception_handler(RequestValidationError, custom_validation_error_handler)
    app.add_exception_handler(Exception, global_exception_handler)
