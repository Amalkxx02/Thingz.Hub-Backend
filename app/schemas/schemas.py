"""
schemas.py
----------
Defines Pydantic models for user authentication, devices, rooms, and things.

Includes:
- Validation rules for passwords, non-empty fields, and list uniqueness.
- Models used in API endpoints across auth, devices, things, and userThingCards.
"""

from pydantic import BaseModel, EmailStr, field_validator, AfterValidator
from typing import Dict, Any, List, Union, Annotated
from uuid import UUID
import re

# --------------------------
# Helper Validation Functions
# --------------------------

def is_strong_password(password: str):
    """
    Ensures password has:
    - At least 1 lowercase
    - At least 1 uppercase
    - At least 1 digit
    - At least 1 special symbol (@$!%*?&_#-)
    - Minimum length of 8
    """
    pattern = (
        r"^(?=.*[a-z])"
        r"(?=.*[A-Z])"
        r"(?=.*\d)"
        r"(?=.*[@$!%*?&_#-])"
        r"[A-Za-z\d@$!%*?&_#-]{8,}$"
    )
    if re.search(pattern, password):
        return password
    raise ValueError("Password is not strong")


def is_empty(value: str):
    """
    Ensures string is not empty or whitespace only.
    """
    value = value.strip()
    if value == "":
        raise ValueError("Value cannot be empty")
    return value


def is_list_not_empty_and_duplicate(value: list, thing: str):
    """
    Ensures a list:
    - is not empty
    - contains no duplicates (case-insensitive)
    """
    value = [v for v in value if v.strip()]
    if not value:
        raise ValueError(f"{thing} cannot be empty")
    
    lowered_value = [v.lower() for v in value if isinstance(v, str)]
    if len(lowered_value) != len(set(lowered_value)):
        raise ValueError(f"{thing} cannot be duplicated")
    
    return value

# --------------------------
# Authentication Models
# --------------------------

class UserSignIn(BaseModel):
    user_email: EmailStr
    user_password: str


class UserSignUp(BaseModel):
    user_name: Annotated[str, AfterValidator(is_empty)]
    user_email: EmailStr
    user_password: Annotated[str, AfterValidator(is_strong_password)]

# --------------------------
# Other Domain Models
# --------------------------

class RoomAdd(BaseModel):
    room_name: Annotated[str, AfterValidator(is_empty)]
    room_color: str


class ThingCardAdd(BaseModel):
    thing_id: int
    thing_config: Dict[str, Any]


class DeviceAdd(BaseModel):
    device_id: UUID
    device_name: Annotated[str, AfterValidator(is_empty)]

# --------------------------
# Things Models
# --------------------------

class Sensor(BaseModel):
    sensors: List[str]

    @field_validator("sensors")
    def is_list_not_empty(cls, value: list):
        return is_list_not_empty_and_duplicate(value, thing="Sensors")


class Actuator(BaseModel):
    actuators: List[str]

    @field_validator("actuators")
    def is_list_not_empty(cls, value: list):
        return is_list_not_empty_and_duplicate(value, thing="Actuators")


class ThingAdd(BaseModel):
    things: List[Union[Sensor, Actuator]] = []

    @field_validator("things")
    def is_list_not_empty(cls, value: list):
        if not value:
            raise ValueError("Things cannot be empty")
        return value
