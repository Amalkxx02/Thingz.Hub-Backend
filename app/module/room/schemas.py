from pydantic import BaseModel, AfterValidator
from typing import Annotated

from .utils import is_empty


class RoomAdd(BaseModel):
    room_name: Annotated[str, AfterValidator(is_empty)]
    room_color: str
