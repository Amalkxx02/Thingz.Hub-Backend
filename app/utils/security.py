import os
import secrets
import string
from uuid import UUID

from app.core.exceptions import INVALID_UUID


def to_uuid_4_by_str(uuid: str):

    try:
        return UUID(uuid)
    except Exception:
        raise INVALID_UUID


def to_uuid_4_by_bytes(uuid: bytes):

    try:
        return UUID(bytes=uuid)
    except Exception:
        raise INVALID_UUID


def generate_secure_string(length=8):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))
