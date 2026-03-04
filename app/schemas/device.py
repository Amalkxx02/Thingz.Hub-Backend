from uuid import UUID

from pydantic import BaseModel, AfterValidator
from typing import Annotated

from app.schemas.enums import DeviceType
from app.schemas.utils import is_empty


    
class DeviceRequest(BaseModel):
    name: Annotated[str, AfterValidator(is_empty)]
    type: DeviceType

class EdgeDeviceRequest(BaseModel):
    id: UUID
    key: Annotated[str, AfterValidator(is_empty)]
    type:DeviceType
