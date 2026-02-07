from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Request
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("TOKEN_EXP", "1"))


def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with standard claims.

    - `sub` claim holds the user id
    - `exp` is a UTC timestamp for expiry
    """
    now = datetime.utcnow()
    if expires_delta is None:
        expires = now + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    else:
        expires = now + expires_delta

    to_encode = {"sub": str(user_id), "iat": now, "exp": expires}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    """Decode and validate a JWT, returning the payload or raising HTTPException."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_id_from_request(rq: Request) -> str:
    """Extract the bearer token from `Authorization` header and return `sub` (user id)."""
    header = rq.headers.get("Authorization")
    if not header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    parts = header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = parts[1]
    payload = decode_token(token)
    user_id = payload.get("sub") or payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token payload missing subject")
    return str(user_id)


def get_user_id_from_ws(token: str) -> str:
    """Decode a token received over WebSocket and return `sub` (user id)."""
    payload = decode_token(token)
    user_id = payload.get("sub") or payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token payload missing subject")
    return str(user_id)
