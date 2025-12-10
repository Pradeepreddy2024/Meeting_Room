from pydantic import BaseModel
from typing import Optional


class MeetingRoomBase(BaseModel):
    name: str
    location: Optional[str] = None
    capacity: Optional[int] = None
    is_active: bool = True


class MeetingRoomCreate(MeetingRoomBase):
    pass


class MeetingRoomUpdate(MeetingRoomBase):
    pass


class MeetingRoomRead(MeetingRoomBase):
    id: int

    class Config:
        orm_mode = True
