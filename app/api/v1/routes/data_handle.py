from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select, and_

from app.core.security.dependency import get_current_device
from app.database.session import get_db
from app.database import CacheDB,get_cache_db
from app.models.thing import Thing
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter(prefix="/ws", tags=["websocket"])

connected_client: dict[UUID, WebSocket] = {}
connected_devices: dict[UUID, WebSocket] = {}
thing: dict[str, int] = {}


@router.websocket("/client")
async def data_handle_client(jwt_key:bytes,ws: WebSocket,cache:CacheDB = Depends(get_cache_db)):
    
    user_id = UUID(verify_access_token_ws(jwt_key))

    if user_id is None:
        await ws.close()  # status_code=404, detail="The user does not exist. It is a illegal move"
        return

    await ws.accept()
    cache.set[user_id] = ws

    try:
        while True:
            thing_data = await connected_client[user_id].receive_json()

    except WebSocketDisconnect:
        print("client disconnect")
        connected_client.pop(user_id, None)


@router.websocket("/device/{device_id}")
async def data_handle_thing(ws:WebSocket,device_id: UUID = Depends(get_current_device),db: AsyncSession = Depends(get_db)):
    
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
