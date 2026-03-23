from pydantic import BaseModel
from datetime import datetime
from typing import List


class UserAdmin(BaseModel):
    id: int
    username: str
    email: str
    is_verified: bool
    is_admin: bool
    is_banned: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class RoomAdmin(BaseModel):
    id: int
    title: str
    topic: str
    language: str
    max_participants: int
    is_public: bool
    status: str
    creator_id: int
    created_at: datetime
    participant_count: int

    model_config = {"from_attributes": True}


class AdminStats(BaseModel):
    total_users: int
    total_rooms: int
    active_rooms: int
    banned_users: int