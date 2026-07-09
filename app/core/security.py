import secrets
import string
import bcrypt
import hashlib
from jose import jwt

from app.core.config import settings
from app.tokens import schemas
from app.tokens import service as token_service
from app.utils.datetime_utils import get_current_utc_time, get_future_utc_time


def generate_api_key():
    alphabet = string.ascii_letters + string.digits
    entropy = "".join(secrets.choice(alphabet) for _ in range(32))
    return f"{settings.PREFIX}_{entropy}"


def mask_value(value: str):
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}{'#' * (len(value) - 8)}{value[-4:]}"


def hash_password(pwd: str) -> bytes:
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())


def verify_password(plain_pwd: str, hashed_pwd: bytes) -> bool:
    return bcrypt.checkpw(plain_pwd.encode(), hashed_pwd)


def get_fingerprint(value: str) -> bytes:
    return hashlib.sha256(value.encode()).hexdigest().encode()


def verify_fingerprint(value: str, fingerprint: bytes) -> bool:
    return secrets.compare_digest(get_fingerprint(value), fingerprint)


def encode_access_token(payload: dict) -> str:
    return jwt.encode(payload, settings.JWT_ACCESS_KEY, settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> schemas.AccessTokenResponse:
    result = jwt.decode(
        token, settings.JWT_ACCESS_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    return schemas.AccessTokenResponse(**result)


def encode_refresh_token(payload: dict) -> str:
    return jwt.encode(payload, settings.JWT_REFRESH_KEY, settings.JWT_ALGORITHM)


def decode_refresh_token(token: str) -> schemas.RefreshTokenResponse:
    result = jwt.decode(
        token, settings.JWT_REFRESH_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    return schemas.RefreshTokenResponse(**result)
