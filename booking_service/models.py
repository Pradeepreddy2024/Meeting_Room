import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from database import Base


class MeetingType(str, enum.Enum):
    TEAM = "TEAM"
    PROJECT = "PROJECT"
    CLIENT = "CLIENT"


class BookingStatus(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    AUTO_CANCELLED = "AUTO_CANCELLED"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, nullable=False)  # could be FK to meeting_rooms.id
    organizer_id = Column(Integer, nullable=False)  # user id from user_service
    organizer_role = Column(String(50), nullable=False)
    meeting_type = Column(Enum(MeetingType), nullable=False)
    title = Column(String(255), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.CONFIRMED)
    cancelled_by_booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cancelled_by_booking = relationship("Booking", remote_side=[id])
