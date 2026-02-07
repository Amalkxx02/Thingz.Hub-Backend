"""
auth.py
-------
Manages user authentication APIs: signup, email verification, and signin.

Endpoints:
1. POST /api/auth/signup
    - Registers a new user.
    - Sends a verification link with a short-lived token (simulated with print).

2. GET /api/auth/verify_email
    - Verifies the user's email using a token.
    - Creates the user account if the token is valid.

3. POST /api/auth/signin
    - Authenticates the user with email and password.
    - Returns the user's ID on successful login.

Notes:
- Security:
    - Currently, email verification token is stored in-memory (`pending_user` dict).
      This is **not persistent** and not suitable for production.
    - Use a database or a secure cache (e.g., Redis) in production.
    - Authentication is currently basic; plain UUIDs are returned on signin. JWT tokens are recommended for secure sessions.
- Passwords are hashed before storage. Plain passwords are never stored.
- Tokens expire after 5 minutes.

Future Improvements:

- Database-backed Pending Users:
    - Store pending user entries in a dedicated database table.
    - Allows token verification across multiple app instances and ensures persistence.
- Email Delivery:
    - Replace `print` statements with actual email sending service (SMTP, SES, etc.).
- Rate Limiting / Security:
    - Limit signup attempts per IP/email to prevent abuse.
    - Implement password strength checks.
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4

from schemas.schemas import UserSignUp, UserSignIn
from utils.user_utils import user_verify, insert_user
from utils.password_utils import password_hashing, password_check
from utils.database_utils import get_db
from utils.jwt_utils import create_access_token

router = APIRouter(prefix="/api/auth", tags=["user"])

# In-memory storage for pending users awaiting email verification
pending_user = {}


@router.post("/signup")
async def signup_user(user_data: UserSignUp, db: AsyncSession = Depends(get_db)):
    """
    Initiates signup for a new user.

    Args:
        user_data (UserSignUp): Contains user's name, email, and password.
        db (AsyncSession): Async database session (dependency injected).

    Raises:
        HTTPException (401): If email already exists in the database.

    Returns:
        dict: Success message with status code.
        Example:
            {
                "status": 200,
                "message": "Verification link sent to your Email address"
            }
    """
    hashed_pwd = password_hashing(user_data.user_password)
    user = await user_verify(user_data.user_email, db)
    if user is not None:
        raise HTTPException(status_code=401, detail="Email already exists")

    token = uuid4()
    expires_at = datetime.now() + timedelta(minutes=10)

    pending_user[token] = {
        "user_name": user_data.user_name,
        "user_email": user_data.user_email.lower(),
        "user_password": hashed_pwd,
        "expires_at": expires_at,
    }

    print(
        f"Verification link: http://localhost:8000/api/auth/verify_email?token={token}"
    )

    return {"status": 200, "message": "Verification link sent to your Email address"}


@router.get("/verify_email")
async def email_verification(token: UUID, db: AsyncSession = Depends(get_db)):
    """
    Verifies the user's email and creates the account.

    Args:
        token (str): Verification token sent via email.
        db (AsyncSession): Async database session.

    Raises:
        HTTPException (400): Invalid or expired token.

    Returns:
        dict: Success message.
        Example:
            {
                "message": "Email verified. Account created."
            }
    """
    pending = pending_user.get(token)
    if not pending:
        raise HTTPException(status_code=400, detail="Invalid or Expired token")

    if datetime.now() > pending["expires_at"]:
        del pending_user[token]
        raise HTTPException(status_code=400, detail="Token Expired")

    await insert_user(pending, db)
    del pending_user[token]

    return {"message": "Email verified. Account created."}


@router.post("/signin")
async def signin_user(user_data: UserSignIn, db: AsyncSession = Depends(get_db)):
    """
    Authenticates a user using email and password.

    Args:
        user_data (UserSignIn): Contains user's email and password.
        db (AsyncSession): Async database session.

    Raises:
        HTTPException (401): If email doesn't exist or password is incorrect.

    Returns:
        dict: User identification info.
        Example:
            {
                "user_id": "<UUID>"
            }
    """
    user = await user_verify(user_data.user_email, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Email or Password doesn't match")

    pwd_check = password_check(user.user_password, user_data.user_password)

    if not pwd_check:
        raise HTTPException(status_code=401, detail="Email or Password doesn't match")

    jwt = create_access_token(user.user_id)

    return {"jwt_key": jwt}
