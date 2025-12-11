from pydantic import BaseModel
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    TEAM_LEAD = "TEAM_LEAD"
    MANAGER = "MANAGER"
    CEO = "CEO"
    DEVELOPER = "DEVELOPER"
    TESTER = "TESTER"


class UserBase(BaseModel):
    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str
    role: UserRole


class UserRead(UserBase):
    id: int
    role: UserRole

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
