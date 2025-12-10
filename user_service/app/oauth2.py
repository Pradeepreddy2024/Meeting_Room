import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .schemas import auth_schemas

from . import database
from .models import user_models as user_model

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "youwillneverguessmysecretkeyuntilyoutryininmycode")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception: HTTPException) -> auth_schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return auth_schemas.TokenData(id=user_id)  # ✅ keep int
    except JWTError:
        raise credentials_exception
    

def get_token_from_request(
    request: Request,
    token_from_header: Optional[str] = Depends(oauth2_scheme)
) -> str:
    if token_from_header:
        return token_from_header

    cookie_val = request.cookies.get("access_token")
    if cookie_val:
        return cookie_val.removeprefix("Bearer ").strip() if cookie_val.startswith("Bearer ") else cookie_val

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    token: str = Depends(get_token_from_request),
    db: Session = Depends(database.get_db)
) -> user_model.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(user_model.User).filter(user_model.User.id == token_data.id).first()  # ✅ int matches DB
    if not user:
        raise credentials_exception
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
) -> user_model.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None or email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(user_model.User).filter(user_model.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user
