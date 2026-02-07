from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select, and_

from models.models import Thing
from app.database import async_session_local

from utils.jwt_utils import verify_access_token_ws
from utils.thing_utils import device_check
from typing import Dict
from uuid import UUID
import json

router = APIRouter(prefix="/ws", tags=["websocket"])

connected_client: Dict[UUID, WebSocket] = {}
connected_devices: Dict[UUID, WebSocket] = {}
thing: Dict[str, int] = {}


@router.websocket("/client")
async def data_handle_client(jwt_key:bytes,ws: WebSocket):
    
    user_id = UUID(verify_access_token_ws(jwt_key))

    if user_id is None:
        await ws.close()  # status_code=404, detail="The user does not exist. It is a illegal move"
        return

    await ws.accept()
    connected_client[user_id] = ws

    try:
        while True:
            thing_data = await connected_client[user_id].receive_json()

    except WebSocketDisconnect:
        print("client disconnect")
        connected_client.pop(user_id, None)


@router.websocket("/device/{device_id}")
async def data_handle_thing(device_id: UUID, ws: WebSocket):
    async with async_session_local() as db:
        device = await device_check(device_id, db)
        if device is None:
            await ws.close()  # status_code=400, detail="The Device does not exist"
            return

    user_id = device.user_id
    print(type(user_id))
    await ws.accept()
    connected_devices[device_id] = ws

    try:
        while True:
            row_data = await connected_devices[device_id].receive_text()
            

            if user_id in connected_client:

                thing_data = json.loads(row_data)
                async with async_session_local() as db:

                    for key, value in thing_data.items():

                        thing_crypt = str(device_id) + "_" + str(key)

                        thing_id = thing.setdefault(thing_crypt, 0)

                        if not thing_id:

                            thing_id = await db.scalar(
                                select(Thing.thing_id).where(
                                    and_(
                                        Thing.device_id == device_id,
                                        Thing.thing_name == key,
                                    )
                                )
                            )
                            thing[thing_crypt] = thing_id

                            thing_id = thing[thing_crypt]

                        thing_payload = {str(thing_id): value}
                

                await connected_client[user_id].send_json(thing_payload)

    except WebSocketDisconnect:
        print("device disconnect")
        connected_devices.pop(device_id, None)
