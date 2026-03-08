import multiprocessing
from uuid import UUID

manager = multiprocessing.Manager()

global _cache_db
_device_db: dict[UUID, str] = manager.dict()

class CacheDB:
    def __init__(self) -> None:
        self._cache_db = _device_db
        self._lock = manager.Lock()

    def get(self, id: UUID) -> str | None:
        return self._cache_db.get(id)

    def set(self, id: UUID, value: str) -> None:
        with self._lock:
            self._cache_db[id] = value

    def delete(self,id:UUID):
        with self._lock:
            self._cache_db.pop(id)

    def all(self) -> dict[UUID, str]:
        return self._cache_db

db = CacheDB()

async def get_cache_db():
    return db