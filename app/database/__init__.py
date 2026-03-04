import multiprocessing
from uuid import UUID

from fastapi import WebSocket

manager = multiprocessing.Manager()

global _cache_db
_device_db: dict[UUID, str|WebSocket] = manager.dict()

class CacheDB:
    def __init__(self) -> None:
        self._cache_db = _device_db
        self._lock = manager.Lock()

    def get(self, id: UUID) -> str | WebSocket | None:
        return self._cache_db.get(id)

    def set(self, id: UUID, value: str | WebSocket) -> None:
        with self._lock:
            self._cache_db[id] = value

    def delete(self,id:UUID):
        with self._lock:
            self._cache_db.pop(id)

    def all(self) -> dict[UUID, str | WebSocket]:
        return self._cache_db

db = CacheDB()

async def get_cache_db():
    return db