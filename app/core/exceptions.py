from app.middleware.error_handler import ExceptionHelper
from fastapi import status

INVALID_CREDENTIALS = ExceptionHelper(
    status_code=status.HTTP_401_UNAUTHORIZED,
    message="Invalid credentials",
    error="Invalid Credentials",
)

INVALID_TOKEN = ExceptionHelper(
    status_code=status.HTTP_401_UNAUTHORIZED,
    message="Invalid token",
    error="Invalid Token",
)

TOKEN_EXPIRED = ExceptionHelper(
    status_code=status.HTTP_401_UNAUTHORIZED,
    message="The token has expired",
    error="Token Expired",
    data={"token_expired": True},
)

TOKEN_MISMATCH = ExceptionHelper(
    status_code=status.HTTP_403_FORBIDDEN,
    message="The token type is not suitable for this endpoint",
    error="Token Mismatch",
)

INVALID_UUID = ExceptionHelper(
    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    message="Provided id is not a valid uuid",
    error=f"Invalid UUID",
)
