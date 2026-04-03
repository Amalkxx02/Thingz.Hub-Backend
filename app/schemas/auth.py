from pydantic import BaseModel, EmailStr, AfterValidator, HttpUrl
from typing import Annotated

from .utils import email_formalize, is_strong_password


class AuthIn(BaseModel):
    email: Annotated[EmailStr, AfterValidator(email_formalize)]
    password: Annotated[str, AfterValidator(is_strong_password)]

class VerificationResponse(BaseModel):
    link: HttpUrl
