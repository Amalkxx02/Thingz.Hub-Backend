from valkey.asyncio import Valkey
from uuid import UUID
from .config import settings

client = Valkey(
    host=settings.VALKEY_HOST, port=settings.VALKEY_PORT, decode_responses=True
)


class CacheDB:
    def __init__(self) -> None:
        self._cache_db = client

    async def get(self, id: UUID) -> str | dict | None:
        value = await self._cache_db.get(str(id))
        return value

    async def set(
        self, id: UUID, value: str | dict, expire_seconds: int | None = None
    ) -> None:
        await self._cache_db.set(str(id), value, ex=expire_seconds)

    async def delete(self, id: UUID):
        await self._cache_db.delete(str(id))

    # def all(self) -> dict[UUID, str]:
    #     return self._cache_db


db = CacheDB()


def get_cache_db():
    return db
