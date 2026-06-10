from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select, and_

from app.core.jwt.dependency import get_current_device, get_current_user
from app.database.session import get_db
from app.database.cache_db import CacheDB, get_cache_db
from app.models.thing import Thing
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter()

connected_client: dict[UUID, WebSocket] = {}
connected_devices: dict[UUID, WebSocket] = {}
thing: dict[str, int] = {}


@router.websocket("/client")
async def data_handle_client(ws: WebSocket, jwt_key: str):

    user_id = await get_current_user(jwt_key)
    await ws.accept()

    connected_client[user_id] = ws

    try:
        while True:
            thing_data = await connected_client[user_id].receive_json()

    except WebSocketDisconnect:
        print("client disconnect")
        connected_client.pop(user_id, None)


@router.websocket("/device")
async def data_handle_thing(
    ws: WebSocket,
    device_id: UUID = Depends(get_current_device),
    db: AsyncSession = Depends(get_db),
):
    pass


#     user_id = device.user_id
#     print(type(user_id))
#     await ws.accept()
#     connected_devices[device_id] = ws

#     try:
#         while True:
#             row_data = await connected_devices[device_id].receive_text()


#             if user_id in connected_client:

#                 thing_data = json.loads(row_data)
#                 async with async_session_local() as db:

#                     for key, value in thing_data.items():

#                         thing_crypt = str(device_id) + "_" + str(key)

#                         thing_id = thing.setdefault(thing_crypt, 0)

#                         if not thing_id:

#                             thing_id = await db.scalar(
#                                 select(Thing.thing_id).where(
#                                     and_(
#                                         Thing.device_id == device_id,
#                                         Thing.thing_name == key,
#                                     )
#                                 )
#                             )
#                             thing[thing_crypt] = thing_id

#                             thing_id = thing[thing_crypt]

#                         thing_payload = {str(thing_id): value}


#                 await connected_client[user_id].send_json(thing_payload)

#     except WebSocketDisconnect:
#         print("device disconnect")
#         connected_devices.pop(device_id, None)
