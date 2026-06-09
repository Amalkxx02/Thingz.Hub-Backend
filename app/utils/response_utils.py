from fastapi.responses import JSONResponse
from fastapi import status


def response_helper(
    status_code: int = status.HTTP_200_OK,
    message: str = "Success",
    error: str = None,
    data: dict = None,
    **kwargs
):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": message,
            "error": error,
            "data": data or {},
            **kwargs,
        },
    )
