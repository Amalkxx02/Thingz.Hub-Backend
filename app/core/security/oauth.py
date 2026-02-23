# Third-Party
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials, HTTPBearer
import secrets

from app.core.exceptions import INVALID_CREDENTIALS

oauth2_scheme = HTTPBearer()
swagger_security = HTTPBasic()

async def swagger_auth(cred:HTTPBasicCredentials = Depends(swagger_security)):
    correct_user = secrets.compare_digest(cred.username,"admin")
    correct_pwd = secrets.compare_digest(cred.password,"admin123")
    if not (correct_user and correct_pwd):
        raise INVALID_CREDENTIALS
    
async def get_current_token(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token: str = (token.model_dump()).get("credentials")
    return token