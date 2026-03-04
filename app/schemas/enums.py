from enum import Enum, IntEnum


class JwtType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class DataType(IntEnum):
    INT = 0
    FLOAT = 1
    BOOL = 2
    VECTOR3 = 3

class ThingType(IntEnum):
    SENSOR = 0
    ACTUATOR = 1
    HYBRID = 2

class DeviceType(IntEnum):
    HUB = 0
    NODE = 1
