from enum import Enum


class JwtType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
