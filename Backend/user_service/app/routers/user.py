from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models import user_models as models
from ..database import get_db
from .. import utils
from ..schemas import user_schemas as schemas
from ..oauth2 import create_access_token, get_current_user

router = APIRouter(
    prefix="",
    tags=['User']
)

@router.post("/", response_model=schemas.UserRead)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    hash_password = utils.hash(user_in.password)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        username=user_in.username,
        full_name=user_in.full_name,
        email=user_in.email,
        password=hash_password,
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# @router.post("/users/login", response_model=schemas.Token)
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db),
# ):
#     # OAuth2PasswordRequestForm has username / password
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#         )
#     token = create_access_token(
#         {
#             "sub": str(user.id),
#             "email": user.email,
#             "role": user.role.value,
#         }
#     )
#     return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserRead)
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user
