# oauth2.py
import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .schemas import auth_schemas
from . import database
from .models import user_models as user_model

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "youwillneverguessmysecretkeyuntilyoutryininmycode")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# This should match the real login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException) -> auth_schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return auth_schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception


def get_token_from_request(
    request: Request,
    token_from_header: Optional[str] = Depends(oauth2_scheme),
) -> str:
    # 1. Prefer Authorization header
    if token_from_header:
        return token_from_header

    # 2. Fallback to cookie "access_token"
    cookie_val = request.cookies.get("access_token")
    if cookie_val:
        return cookie_val.removeprefix("Bearer ").strip() if cookie_val.startswith("Bearer ") else cookie_val

    # 3. If neither present, not authenticated
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    token: str = Depends(get_token_from_request),
    db: Session = Depends(database.get_db),
) -> user_model.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(user_model.User).filter(user_model.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user
