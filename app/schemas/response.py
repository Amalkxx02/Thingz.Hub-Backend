from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Generic success response with a message."""
    message: str
