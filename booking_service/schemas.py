from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class MeetingType(str, Enum):
    TEAM = "TEAM"
    PROJECT = "PROJECT"
    CLIENT = "CLIENT"


class BookingStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    AUTO_CANCELLED = "AUTO_CANCELLED"


class BookingBase(BaseModel):
    room_id: int
    title: str
    meeting_type: MeetingType
    start_time: datetime = Field(..., description="ISO datetime")
    end_time: datetime = Field(..., description="ISO datetime")


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    id: int
    organizer_id: int
    organizer_role: str
    status: BookingStatus
    cancelled_by_booking_id: Optional[int] = None

    class Config:
        orm_mode = True
