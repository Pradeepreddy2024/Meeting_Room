from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import models
import schemas
from auth_dependencies import get_current_user, CurrentUser, UserRole

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booking Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_user_allowed_meeting_type(user_role: UserRole, meeting_type: schemas.MeetingType):
    if user_role == UserRole.CEO:
        if meeting_type not in (schemas.MeetingType.CLIENT, schemas.MeetingType.PROJECT):
            raise HTTPException(400, "CEO can only book CLIENT or PROJECT meetings")
    elif user_role == UserRole.MANAGER:
        if meeting_type not in (schemas.MeetingType.PROJECT, schemas.MeetingType.TEAM):
            raise HTTPException(400, "Manager can book PROJECT or TEAM meetings")
    elif user_role == UserRole.TEAM_LEAD:
        if meeting_type != schemas.MeetingType.TEAM:
            raise HTTPException(400, "Team lead can only book TEAM meetings")


def role_priority(role: UserRole) -> int:
    if role == UserRole.CEO:
        return 3
    if role == UserRole.MANAGER:
        return 2
    return 1


def find_overlapping_bookings(db: Session, room_id: int, start: datetime, end: datetime):
    return (
        db.query(models.Booking)
        .filter(
            models.Booking.room_id == room_id,
            models.Booking.status == models.BookingStatus.CONFIRMED,
            models.Booking.start_time < end,
            models.Booking.end_time > start,
        )
        .all()
    )


@app.post("/bookings", response_model=schemas.BookingRead)
def create_booking(
    booking_in: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    # validate time
    if booking_in.end_time <= booking_in.start_time:
        raise HTTPException(400, "end_time must be after start_time")

    # check allowed meeting type
    check_user_allowed_meeting_type(current_user.role, booking_in.meeting_type)

    # find overlaps
    conflicts = find_overlapping_bookings(
        db,
        room_id=booking_in.room_id,
        start=booking_in.start_time,
        end=booking_in.end_time,
    )

    new_role_priority = role_priority(current_user.role)

    # if any conflict has higher priority, reject
    for existing in conflicts:
        existing_role = UserRole(existing.organizer_role)
        existing_priority = role_priority(existing_role)

        if new_role_priority < existing_priority:
            raise HTTPException(
                status_code=409,
                detail="Existing higher-priority booking at this time",
            )

    # create new booking
    new_booking = models.Booking(
        room_id=booking_in.room_id,
        organizer_id=current_user.id,
        organizer_role=current_user.role.value,
        meeting_type=booking_in.meeting_type,
        title=booking_in.title,
        start_time=booking_in.start_time,
        end_time=booking_in.end_time,
        status=models.BookingStatus.CONFIRMED,
    )

    db.add(new_booking)
    db.flush()  # get new_booking.id

    # auto-cancel lower-priority conflicts
    for existing in conflicts:
        existing.status = models.BookingStatus.AUTO_CANCELLED
        existing.cancelled_by_booking_id = new_booking.id

    db.commit()
    db.refresh(new_booking)

    return new_booking


@app.get("/bookings", response_model=List[schemas.BookingRead])
def list_bookings(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    # For now: return all bookings (you can filter per user later)
    return db.query(models.Booking).all()


@app.get("/bookings/{booking_id}", response_model=schemas.BookingRead)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    booking = db.query(models.Booking).get(booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking


@app.delete("/bookings/{booking_id}", response_model=schemas.BookingRead)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    booking = db.query(models.Booking).get(booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")

    # only organizer or CEO can cancel
    if booking.organizer_id != current_user.id and current_user.role != UserRole.CEO:
        raise HTTPException(403, "Not authorized to cancel this booking")

    booking.status = models.BookingStatus.CANCELLED
    db.commit()
    db.refresh(booking)
    return booking
