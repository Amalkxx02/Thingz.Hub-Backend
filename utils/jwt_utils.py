from datetime import datetime, timedelta
from fastapi import HTTPException, Request
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXP = 1


def create_access_token(user_id):
    user_data = {
        "user_id": str(user_id),
        "expiry": str(datetime.now() + timedelta(hours=TOKEN_EXP)),
    }
    encoded_token = jwt.encode(user_data, SECRET_KEY, ALGORITHM)
    return encoded_token


def verify_access_token(rq: Request):
    try:
        header = rq.headers.get("Authorization")
        jwt_key = header.split()[1]
        decoded_token = jwt.decode(jwt_key, SECRET_KEY, ALGORITHM)
    except:
        raise HTTPException(status_code=404, detail="Invalid user")
    return decoded_token["user_id"]


def verify_access_token_ws(jwt_key):
    try:
        decoded_token = jwt.decode(jwt_key, SECRET_KEY, ALGORITHM)
    except:
        raise HTTPException(status_code=404, detail="Invalid user")
    return decoded_token["user_id"]
