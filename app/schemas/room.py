from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RoomCreate(BaseModel):
    title: str
    topic: str
    language: str
    max_participants: int = 10
    is_public: bool = True


class RoomUpdate(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    max_participants: Optional[int] = None


class ParticipantResponse(BaseModel):
    id: int
    username: str
    is_muted: bool

    model_config = {"from_attributes": True}


class RoomResponse(BaseModel):
    id: int
    title: str
    topic: str
    language: str
    max_participants: int
    is_public: bool
    status: str
    agora_channel_name: str
    creator_id: int
    created_at: datetime
    participant_count: int = 0

    model_config = {"from_attributes": True}


class RoomDetailResponse(BaseModel):
    id: int
    title: str
    topic: str
    language: str
    max_participants: int
    is_public: bool
    status: str
    agora_channel_name: str
    creator_id: int
    created_at: datetime
    participants: list[ParticipantResponse] = []

    model_config = {"from_attributes": True}


class AgoraTokenResponse(BaseModel):
    token: str
    channel_name: str
    uid: int