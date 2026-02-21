from pydantic import BaseModel, AfterValidator
from typing import Annotated
from uuid import UUID

from app.schemas.utils import is_empty


class DeviceRequest(BaseModel):
    name: Annotated[str, AfterValidator(is_empty)]
