from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from utils.config import get_config
from utils.db import get_session
from models import User

config = get_config()

class JWTAuthentication(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTAuthentication, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTAuthentication, self).__call__(request)
        if credentials:
            return self.get_user_id(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Must provide Authorization header.")

    def get_user_id(self, token: str) -> int:
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms="HS256")
            return payload['id']
        except JWTError as _:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


jwt_security = JWTAuthentication()


def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(days=365) # 1 year
    to_encode = {"id": user_id, "exp": expire}
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm="HS256")


def get_current_user(user_id: int = Depends(jwt_security), session: Session = Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=403, detail="Invalid authorization code.")
    return user