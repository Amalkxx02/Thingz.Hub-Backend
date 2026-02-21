import re

from pydantic import EmailStr


def is_strong_password(password: str):
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


def email_formalize(email: EmailStr) -> EmailStr:
    return email.lower()
