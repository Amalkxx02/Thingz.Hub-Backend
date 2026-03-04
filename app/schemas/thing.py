from typing import Optional

from pydantic import BaseModel
from app.schemas.enums import DataType, ThingType

class EdgeThingzRequest(BaseModel):
    slug:str
    hardware_address:Optional[str] = "0"
    data_type:DataType
    thing_type:ThingType

class UpdateThingRequest(BaseModel):
    name:Optional[str] = None
    unit:Optional[str] = None