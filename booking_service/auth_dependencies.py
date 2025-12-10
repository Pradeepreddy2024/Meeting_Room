import os
from enum import Enum
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class UserRole(str, Enum):
    TEAM_LEAD = "TEAM_LEAD"
    MANAGER = "MANAGER"
    CEO = "CEO"


class CurrentUser(BaseModel):
    id: int
    email: str
    role: UserRole


async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        email = payload.get("email")
        role = payload.get("role")
        if user_id is None or email is None or role is None:
            raise credentials_exception
        return CurrentUser(id=int(user_id), email=email, role=UserRole(role))
    except JWTError:
        raise credentials_exception
