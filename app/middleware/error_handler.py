# Third-Party Imports
from functools import wraps
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError

import logging

from app.utils.response_utils import response_helper


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
    return response_helper(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error="Internal Server Error",
        message="An unexpected error occurred.",
    )


async def custom_exception_handler(request: Request, exc: ExceptionHelper):
    content = {
        "status_code": exc.status_code,
        "error": exc.error,
        "message": exc.message,
        "data": exc.data,
    }
    return response_helper(**content)


async def custom_validation_error_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    logging.error(f"Validation error: {error}", exc_info=False)
    response_status = status.HTTP_422_UNPROCESSABLE_CONTENT
    content = {
        "status_code": response_status,
        "error": "Validation Error",
        "message": f"{error.get('loc', 'Invalid body')} {error.get('msg', 'Invalid input')}",
    }
    return response_helper(**content)


def setup_exception_handlers(app):
    app.add_exception_handler(ExceptionHelper, custom_exception_handler)
    app.add_exception_handler(RequestValidationError, custom_validation_error_handler)
    app.add_exception_handler(Exception,global_exception_handler)
