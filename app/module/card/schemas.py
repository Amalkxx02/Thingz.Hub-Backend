from pydantic import BaseModel
from typing import Dict, Any


class ThingCardAdd(BaseModel):
    thing_id: int
    thing_config: Dict[str, Any]
