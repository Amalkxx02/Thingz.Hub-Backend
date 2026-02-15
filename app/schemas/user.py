from uuid import UUID
from pydantic import BaseModel, AfterValidator,HttpUrl
from typing import Annotated

from .utils import is_empty

class Onboard(BaseModel):
    name: Annotated[str, AfterValidator(is_empty)] 
    profile_image_url: HttpUrl