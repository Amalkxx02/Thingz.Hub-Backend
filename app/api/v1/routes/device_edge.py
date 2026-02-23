from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.device import DeviceRequest
from app.core.security.dependency import get_current_user
from app.services.device import device_service
from app.database.session import get_db

router = APIRouter()


# @router.post("/{device_id}")
# async def add_thing_for_user(
#     device_id: UUID, thing: ThingAdd, db: AsyncSession = Depends(get_db)
# ):
#     """
#     Add things (sensors/actuators) to a device.

#     Args:
#         device_id (UUID): UUID of the target device.
#         thing (ThingAdd): ThingAdd schema containing sensors and actuators.
#         db (AsyncSession): Async SQLAlchemy session (injected via dependency).

#     Returns:
#         dict: {"status": "ok"} on success.

#     Raises:
#         HTTPException:
#             400 → Device not found
#             409 → Duplicate thing (already registered)
#     """
#     # Validate device existence
#     await device_check(device_id, db)

#     # Prepare batch insert values
#     values = []
#     for items in thing.things:
#         if isinstance(items, Sensor):
#             for sensor_name in items.sensors:
#                 values.append(
#                     {
#                         "device_id": device_id,
#                         "thing_type": "sensor",
#                         "thing_name": sensor_name,
#                     }
#                 )
#         elif isinstance(items, Actuator):
#             for actuator_name in items.actuators:
#                 values.append(
#                     {
#                         "device_id": device_id,
#                         "thing_type": "actuator",
#                         "thing_name": actuator_name,
#                     }
#                 )

#     # Batch insert with conflict handling (ignore duplicates)
#     query = (
#         insert(Thing)
#         .values(values)
#         .on_conflict_do_nothing(index_elements=["device_id", "thing_name"])
#         .returning(Thing)
#     )

#     await db_execution(query, db)

#     return {"status": "ok"}


# @router.get("")
# async def list_thing_for_user(
#     db: AsyncSession = Depends(get_db),
#     user_id=Depends(verify_access_token),
# ):
#     """
#     List all things for a user's devices.

#     Args:
#         user_id (UUID): UUID of the user.
#         db (AsyncSession): Async SQLAlchemy session.

#     Returns:
#         list[dict]: List of devices with structured 'things' object:
#             {
#                 "device_name": "Device1",
#                 "things": {
#                     "sensors": [{"thing_id": ..., "thing_name": ...}, ...],
#                     "actuators": [{"thing_id": ..., "thing_name": ...}, ...]
#                 }
#             }
#         - Returns empty list if user has no devices/things.

#     Raises:
#         HTTPException:
#             404 → User does not exist.
#     """
#     # Validate user existence

#     # Query devices and their associated things grouped by type
#     query = (
#         select(
#             Device.device_name,
#             func.json_build_object(
#                 "sensors",
#                 func.json_agg(
#                     func.json_build_object(
#                         "thing_id",
#                         Thing.thing_id,
#                         "thing_name",
#                         Thing.thing_name,
#                     )
#                 ).filter(Thing.thing_type == "sensor"),
#                 "actuators",
#                 func.json_agg(
#                     func.json_build_object(
#                         "thing_id",
#                         Thing.thing_id,
#                         "thing_name",
#                         Thing.thing_name,
#                     )
#                 ).filter(Thing.thing_type == "actuator"),
#             ).label("things"),
#         )
#         .group_by(Device.device_id)
#         .join(Thing, Thing.device_id == Device.device_id)
#         .where(Device.user_id == user_id)
#     )

#     rows = await db_execution(query, db, get_single_row=False)
#     return rows
