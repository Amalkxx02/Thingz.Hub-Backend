import secrets
import string
from app.core.config import settings


def generate_api_key():
    alphabet = string.ascii_letters + string.digits
    entropy = "".join(secrets.choice(alphabet) for _ in range(32))
    return f"{settings.PREFIX}_{entropy}"


def mask_value(value: str):
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}{'#' * (len(value) - 8)}{value[-4:]}"
