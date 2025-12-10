# auth.py (users service)

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..import database, utils, oauth2
from ..models import user_models as user_model


router = APIRouter(tags=["User"])


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db), response: Response = None):
    user = db.query(user_model.User).filter(user_model.User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    if response is not None:
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            samesite="lax",
            secure=True,
            path="/",
        )
    return {"access_token": access_token, "token_type": "bearer" }


