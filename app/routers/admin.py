from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.models.user import User
from app.models.room import Room, RoomStatus
from app.models.participant import Participant
from app.schemas.admin import UserAdmin, RoomAdmin, AdminStats

router = APIRouter(prefix="/admin", tags=["Admin"])


# ===== STATISTICS =====

@router.get("/stats", response_model=AdminStats)
def get_admin_stats(
        admin: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Get platform statistics - ADMIN ONLY"""

    total_users = db.query(User).count()
    total_rooms = db.query(Room).count()
    active_rooms = db.query(Room).filter(Room.status == RoomStatus.ACTIVE).count()
    banned_users = db.query(User).filter(User.is_banned == True).count()

    return AdminStats(
        total_users=total_users,
        total_rooms=total_rooms,
        active_rooms=active_rooms,
        banned_users=banned_users
    )


# ===== USER MANAGEMENT =====

@router.get("/users", response_model=List[UserAdmin])
def get_all_users(
        admin: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Get all users - ADMIN ONLY"""
    users = db.query(User).all()
    return users


@router.post("/users/{user_id}/ban")
def ban_user(
        user_id: int,
        admin: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Ban a user - ADMIN ONLY"""

    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot ban yourself")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_banned = True
    db.commit()

    # Kick from all rooms
    participants = db.query(Participant).filter(
        Participant.user_id == user_id
    ).all()

    for p in participants:
        db.delete(p)

    db.commit()

    return {"message": f"User {user.username} banned successfully"}


@router.post("/users/{user_id}/unban")
def unban_user(
        user_id: int,
        admin: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Unban a user - ADMIN ONLY"""

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_banned = False
    db.commit()

    return {"message": f"User {user.username} unbanned successfully"}


# ===== ROOM MANAGEMENT =====

@router.get("/rooms", response_model=List[RoomAdmin])
def get_all_rooms(
        admin: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Get all rooms - ADMIN ONLY"""

    rooms = db.query(Room).all()

    room_list = []
    for room in rooms:
        participant_count = db.query(Participant).filter(
            Participant.room_id == room.id
        ).count()

        room_dict = RoomAdmin(
            id=room.id,
            title=room.title,
            topic=room.topic,
            language=room.language,
            max_participants=room.max_participants,
            is_public=room.is_public,
            status=room.status.value,
            creator_id=room.creator_id,
            created_at=room.created_at,
            participant_count=participant_count
        )
        room_list.append(room_dict)

    return room_list


@router.post("/rooms/{room_id}/close")
def admin_close_room(
        room_id: int,
        admin: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Close any room - ADMIN ONLY"""

    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    from datetime import datetime
    room.status = RoomStatus.CLOSED
    room.closed_at = datetime.utcnow()
    db.commit()

    return {"message": f"Room '{room.title}' closed successfully"}


@router.post("/rooms/{room_id}/kick/{user_id}")
def admin_kick_user(
        room_id: int,
        user_id: int,
        admin: User = Depends(get_admin_user),
        db: Session = Depends(get_db)
):
    """Kick user from any room - ADMIN ONLY"""

    participant = db.query(Participant).filter(
        Participant.room_id == room_id,
        Participant.user_id == user_id
    ).first()

    if not participant:
        raise HTTPException(status_code=400, detail="User not in room")

    db.delete(participant)
    db.commit()

    return {"message": "User kicked successfully"}