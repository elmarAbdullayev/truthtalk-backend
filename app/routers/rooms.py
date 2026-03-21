from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.room import RoomCreate, RoomResponse, RoomDetailResponse, ParticipantResponse
from app.models.user import User
from app.models.room import Room, RoomStatus
from app.models.participant import Participant
import uuid

router = APIRouter(prefix="/rooms", tags=["Rooms"])


# ===== PUBLIC ENDPOINTS (Guest can view) =====

@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    """Get all active rooms - PUBLIC (no auth required)"""
    rooms = db.query(Room).filter(
        Room.status == RoomStatus.ACTIVE,
        Room.is_public == True
    ).all()

    # Add participant count
    room_list = []
    for room in rooms:
        room_dict = {
            "id": room.id,
            "title": room.title,
            "topic": room.topic,
            "language": room.language,
            "max_participants": room.max_participants,
            "is_public": room.is_public,
            "status": room.status.value,
            "agora_channel_name": room.agora_channel_name,
            "creator_id": room.creator_id,
            "created_at": room.created_at,
            "participant_count": len([p for p in room.participants if p.left_at is None])
        }
        room_list.append(room_dict)

    return room_list


@router.get("/{room_id}", response_model=RoomDetailResponse)
def get_room_detail(room_id: int, db: Session = Depends(get_db)):
    """Get room details - PUBLIC"""
    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Get active participants
    active_participants = [
        ParticipantResponse(
            id=p.user.id,
            username=p.user.username,
            is_muted=p.is_muted
        )
        for p in room.participants if p.left_at is None and not p.is_banned
    ]

    return RoomDetailResponse(
        id=room.id,
        title=room.title,
        topic=room.topic,
        language=room.language,
        max_participants=room.max_participants,
        is_public=room.is_public,
        status=room.status.value,
        agora_channel_name=room.agora_channel_name,
        creator_id=room.creator_id,
        created_at=room.created_at,
        participants=active_participants
    )


# ===== PROTECTED ENDPOINTS (Auth required) =====

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
        room_data: RoomCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Create a new room - AUTH REQUIRED"""

    # Generate unique Agora channel name
    channel_name = f"room_{uuid.uuid4().hex[:12]}"

    # Create room
    new_room = Room(
        title=room_data.title,
        topic=room_data.topic,
        language=room_data.language,
        max_participants=room_data.max_participants,
        is_public=room_data.is_public,
        agora_channel_name=channel_name,
        creator_id=current_user.id
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    # Creator automatically joins as participant
    creator_participant = Participant(
        user_id=current_user.id,
        room_id=new_room.id
    )
    db.add(creator_participant)
    db.commit()

    return RoomResponse(
        id=new_room.id,
        title=new_room.title,
        topic=new_room.topic,
        language=new_room.language,
        max_participants=new_room.max_participants,
        is_public=new_room.is_public,
        status=new_room.status.value,
        agora_channel_name=new_room.agora_channel_name,
        creator_id=new_room.creator_id,
        created_at=new_room.created_at,
        participant_count=1
    )


@router.post("/{room_id}/join", status_code=status.HTTP_200_OK)
def join_room(
        room_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Join a room - AUTH REQUIRED"""

    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.status != RoomStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Room is closed")

    # ✅ Check if ALREADY in room (any participant record, not just active)
    existing = db.query(Participant).filter(
        Participant.room_id == room_id,
        Participant.user_id == current_user.id
    ).first()

    if existing:
        # ✅ Already in room - just return success (idempotent)
        return {"message": "Already in room"}

    # Check if banned
    banned = db.query(Participant).filter(
        Participant.room_id == room_id,
        Participant.user_id == current_user.id,
        Participant.is_banned == True
    ).first()

    if banned:
        raise HTTPException(status_code=403, detail="You are banned from this room")

    # Check capacity (only count active participants)
    active_count = db.query(Participant).filter(
        Participant.room_id == room_id
    ).count()

    if active_count >= room.max_participants:
        raise HTTPException(status_code=400, detail="Room is full")

    # Join room
    participant = Participant(
        user_id=current_user.id,
        room_id=room_id
    )
    db.add(participant)
    db.commit()

    return {"message": "Joined room successfully"}


@router.post("/{room_id}/leave", status_code=status.HTTP_200_OK)
def leave_room(
        room_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Leave a room - AUTH REQUIRED"""

    participant = db.query(Participant).filter(
        Participant.room_id == room_id,
        Participant.user_id == current_user.id
    ).first()

    if not participant:
        raise HTTPException(status_code=400, detail="Not in room")

    # ✅ DELETE participant
    db.delete(participant)
    db.commit()

    # ✅ Check remaining participants
    active_count = db.query(Participant).filter(
        Participant.room_id == room_id
    ).count()

    print(f"🔍 Active participants after leave: {active_count}")  # ← Debug

    # ✅ If empty, DELETE room
    if active_count == 0:
        room = db.query(Room).filter(Room.id == room_id).first()
        if room:
            print(f"🗑️ Deleting room {room_id}")  # ← Debug
            db.delete(room)
            db.commit()
            return {"message": "Left room successfully", "room_deleted": True}

    return {"message": "Left room successfully", "room_deleted": False}

@router.post("/{room_id}/close", status_code=status.HTTP_200_OK)
def close_room(
        room_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Close room - ONLY CREATOR"""

    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only room creator can close room")

    from datetime import datetime
    room.status = RoomStatus.CLOSED
    room.closed_at = datetime.utcnow()
    db.commit()

    return {"message": "Room closed successfully"}


@router.post("/{room_id}/kick/{user_id}", status_code=status.HTTP_200_OK)
def kick_user(
        room_id: int,
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Kick user from room - ONLY CREATOR"""

    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only room creator can kick users")

    participant = db.query(Participant).filter(
        Participant.room_id == room_id,
        Participant.user_id == user_id
    ).first()

    if not participant:
        raise HTTPException(status_code=400, detail="User not in room")

    # ✅ DELETE participant (not just set left_at or banned!)
    print(f"🚫 Kicking user {user_id} from room {room_id}")
    db.delete(participant)
    db.commit()

    return {"message": "User kicked successfully"}


@router.post("/{room_id}/mute/{user_id}", status_code=status.HTTP_200_OK)
def mute_user(
        room_id: int,
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Mute user in room - ONLY CREATOR"""

    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only room creator can mute users")

    participant = db.query(Participant).filter(
        Participant.room_id == room_id,
        Participant.user_id == user_id,
        Participant.left_at == None
    ).first()

    if not participant:
        raise HTTPException(status_code=400, detail="User not in room")

    participant.is_muted = not participant.is_muted
    db.commit()

    return {"message": f"User {'muted' if participant.is_muted else 'unmuted'} successfully"}


from app.schemas.room import AgoraTokenResponse
from app.services.agora_service import generate_agora_token


@router.get("/{room_id}/token", response_model=AgoraTokenResponse)
def get_agora_token(
        room_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get Agora token for joining room - AUTH REQUIRED"""

    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    participant = db.query(Participant).filter(
        Participant.room_id == room_id,
        Participant.user_id == current_user.id
    ).first()

    if not participant:
        raise HTTPException(status_code=403, detail="Not in room")

    # ✅ Generate RANDOM UID (0 = Agora auto-generates)
    import random
    random_uid = random.randint(1000, 999999)

    try:
        token = generate_agora_token(
            channel_name=room.agora_channel_name,
            uid=random_uid,  # ← Random UID!
            role=1
        )

        return AgoraTokenResponse(
            token=token,
            channel_name=room.agora_channel_name,
            uid=random_uid  # ← Return random UID
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate token: {str(e)}")