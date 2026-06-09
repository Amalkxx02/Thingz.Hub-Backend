from fastapi import HTTPException, status
from pydantic import StringConstraints,Field
from typing import Annotated
import re

from pydantic import EmailStr, AfterValidator


def is_strong_password(password: str):
    STRONG_PASSWORD_REGEX = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_#-]).+$"
    )
    if not STRONG_PASSWORD_REGEX.match(password):
        raise ValueError(
            "Password must be at least 8 characters long, "
            "contain uppercase and lowercase letters, "
            "a number, and a special character."
        )
    return password


StrongPassword = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=128,
    ),
    AfterValidator(is_strong_password),
    Field(examples=["Password@123"])
]


def is_empty(value: str):
    value = value.strip()
    if value == "":
        raise ValueError("Value cannot be empty")
    return value


def is_list_not_empty_and_duplicate(value: list, thing: str):
    value = [v for v in value if v.strip()]
    if not value:
        raise ValueError(f"{thing} cannot be empty")

    lowered_value = [v.lower() for v in value if isinstance(v, str)]
    if len(lowered_value) != len(set(lowered_value)):
        raise ValueError(f"{thing} cannot be duplicated")

    return value


Email = Annotated[EmailStr, StringConstraints(strip_whitespace=True, to_lower=True)]
