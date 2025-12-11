from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, SessionLocal
import models
import schemas
from auth_dependencies import get_current_user, CurrentUser, UserRole

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Room Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/rooms", response_model=List[schemas.MeetingRoomRead])
def list_rooms(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return db.query(models.MeetingRoom).all()


@app.post("/rooms", response_model=schemas.MeetingRoomRead)
def create_room(
    room_in: schemas.MeetingRoomCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    # Only MANAGER or CEO can create rooms
    if current_user.role not in (UserRole.MANAGER, UserRole.CEO):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    room = models.MeetingRoom(**room_in.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@app.get("/rooms/{room_id}", response_model=schemas.MeetingRoomRead)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    room = db.query(models.MeetingRoom).get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@app.put("/rooms/{room_id}", response_model=schemas.MeetingRoomRead)
def update_room(
    room_id: int,
    room_in: schemas.MeetingRoomUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role not in (UserRole.MANAGER, UserRole.CEO):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    room = db.query(models.MeetingRoom).get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    for field, value in room_in.dict().items():
        setattr(room, field, value)
    db.commit()
    db.refresh(room)
    return room


@app.delete("/rooms/{room_id}", response_model=schemas.MeetingRoomRead)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role not in (UserRole.MANAGER, UserRole.CEO):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    room = db.query(models.MeetingRoom).get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return room
