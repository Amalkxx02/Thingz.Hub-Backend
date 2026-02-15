# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.dialects.postgresql import insert

# from schemas.schemas import DeviceAdd
# from app.models.device import Device
# router = APIRouter(prefix="/api/user/devices", tags=["device"])


# @router.post(
#     "",
#     summary="Add a device for a user",
#     response_description="Device added confirmation",
# )
# async def add_device_for_user(
#     device: DeviceAdd,
#     db: AsyncSession = Depends(get_db),
#     user_id=Depends(verify_access_token),
# ):

#     query = (
#         insert(Device)
#         .values(
#             user_id=user_id,
#             device_id=device.device_id,
#             device_name=device.device_name,
#         )
#         .on_conflict_do_nothing(index_elements=["device_id"])
#         .returning(Device)
#     )

#     # Execute query
#     row = await db_execution(query, db)
#     if row is None:
#         raise HTTPException(status_code=409, detail="The device already exists")

#     return {"message": "Device added successfully"}
