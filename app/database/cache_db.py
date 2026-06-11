from app.core import valkey
from uuid import UUID

class CacheDB:
    def __init__(self) -> None:
        self._cache_db = valkey.client

    async def get(self, id: UUID) -> str | None:
        value = await self._cache_db.get(str(id))
        return value
    
    async def set(self, id: UUID, value: str) -> None:
        self._cache_db.set(str(id),value)

    async def delete(self, id: UUID):
        self._cache_db.delete(str(id))

    # def all(self) -> dict[UUID, str]:
    #     return self._cache_db

db = CacheDB()


def get_cache_db():
    return db
