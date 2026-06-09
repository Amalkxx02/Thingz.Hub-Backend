from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, id: UUID):
        await websocket.accept()
        if id not in self.active_connections:
            self.active_connections[id] = []
        self.active_connections[id].append(websocket)

    def disconnect(self, websocket: WebSocket, id: UUID):
        if id in self.active_connections:
            if websocket in self.active_connections[id]:
                self.active_connections[id].remove(websocket)
            if not self.active_connections[id]:
                del self.active_connections[id]

    async def send_data(self, data: str, id: UUID):
        if id in self.active_connections:
            for connection in self.active_connections[id]:
                await connection.send_text(data)


manager = ConnectionManager()
