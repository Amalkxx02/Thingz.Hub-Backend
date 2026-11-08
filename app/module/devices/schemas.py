from datetime import datetime
from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel

from app.common.utils import IpAddress, MacAddress


class DeviceType(IntEnum):
    HUB = 0
    NODE = 1



# =====================================================================
#  Request Schemas
# =====================================================================
class DeviceRequest(BaseModel):
    name: str
    type: DeviceType


class EdgeDeviceRequest(BaseModel):
    id: UUID
    key: str
    type: DeviceType
    mac_address:MacAddress
    firmware:str
    ip_address:IpAddress

class DeviceFilter(BaseModel):
    is_revoked:bool|None = None
    is_active:bool|None = None
    is_registered:bool|None = None


# =====================================================================
#  DTO Schemas
# =====================================================================
class DeviceModel(BaseModel):
    user_id:UUID
    name:str
    type: DeviceType
    hashed_key: bytes
    key_hint:str

class EdgeDeviceModel(BaseModel):
    mac_address:MacAddress
    firmware:str
    ip_address:IpAddress

class DeviceKeyRotationModel(BaseModel):
    hashed_key: bytes
    key_hint:str
# =====================================================================
#  Response Schemas
# =====================================================================



class DeviceListResponse(BaseModel):
    """Single device response – excludes sensitive fields (hashed_key, user_id)."""

    id: UUID
    name: str
    type: int
    is_revoked: bool
    is_active: bool
    is_registered:bool

    model_config = {"from_attributes":True}

class DeviceResponse(DeviceListResponse):
    """Single device response – excludes sensitive fields (hashed_key, user_id)."""

    key_hint: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes":True}


class DeviceRegisterResponse(BaseModel):
    """Returned after successfully registering a new device."""

    device_id: UUID
    api_key: str


class DeviceToggleResponse(BaseModel):
    """Returned after toggling a device's active status."""

    is_active: bool


class DeviceVerifyResponse(BaseModel):
    """Returned after verifying an edge device."""

    session_token: str | None = None
    verified: bool = False
