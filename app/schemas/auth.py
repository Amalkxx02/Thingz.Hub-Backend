from pydantic import BaseModel, EmailStr, AfterValidator, HttpUrl
from typing import Annotated

from .utils import Email,StrongPassword


class AuthIn(BaseModel):
    email: Email
    password: StrongPassword

class VerificationResponse(BaseModel):
    link: HttpUrl
