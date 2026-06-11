from valkey.asyncio import Valkey
from .config import settings

client = Valkey(
    host=settings.VALKEY_HOST, port=settings.VALKEY_PORT, decode_responses=True
)
