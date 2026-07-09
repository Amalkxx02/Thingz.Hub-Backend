from pydantic import BaseModel, HttpUrl

from ..common.utils import Email, StrongPassword

# =====================================================================
#  Request Schemas
# =====================================================================


class UserSignIn(BaseModel):
    email: Email
    password: StrongPassword


class UserSignUp(UserSignIn):
    name: str
    profile: HttpUrl


class PasswordReset(BaseModel):
    email: Email


class PasswordVerify(BaseModel):
    password: StrongPassword


# =====================================================================
#  DTO Schemas
# =====================================================================


class AuthModel(BaseModel):
    """Full DB row representation for internal use."""

    email: Email
    password: bytes


# =====================================================================
#  Response Schemas
# =====================================================================


class VerificationResponse(BaseModel):
    link: HttpUrl
