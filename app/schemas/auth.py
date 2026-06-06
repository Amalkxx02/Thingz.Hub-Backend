from pydantic import BaseModel, EmailStr, AfterValidator, HttpUrl
from typing import Annotated

from .utils import email_formalize, is_strong_password, StrongPassword


class AuthIn(BaseModel):
    email: Annotated[EmailStr, AfterValidator(email_formalize)]
    password: StrongPassword

class VerificationResponse(BaseModel):
    link: HttpUrl
