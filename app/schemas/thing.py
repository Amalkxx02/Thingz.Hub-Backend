from pydantic import BaseModel, field_validator
from typing import List, Union

from .utils import is_list_not_empty_and_duplicate


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
