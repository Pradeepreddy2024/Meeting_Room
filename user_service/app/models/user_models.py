from sqlalchemy import Column, Integer, String, Enum, DateTime, func
import enum

from ..database import Base


class UserRole(str, enum.Enum):
    TEAM_LEAD = "TEAM_LEAD"
    MANAGER = "MANAGER"
    CEO = "CEO"
    DEVELOPER = "DEVELOPER"
    TESTER = "TESTER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.DEVELOPER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
