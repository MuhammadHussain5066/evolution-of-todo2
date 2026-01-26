# services/auth.py
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    # TODO: verify JWT token here
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
