from uuid import UUID

from app.core.exceptions import INVALID_UUID

def to_uuid_4(uuid: str):
    try:
        return UUID(uuid)
    except Exception:
        raise INVALID_UUID
