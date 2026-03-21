from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class RoomStatus(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    topic = Column(String(500), nullable=False)
    language = Column(String(50), nullable=False)  # "English", "German", "Turkish", etc.
    max_participants = Column(Integer, default=10)
    is_public = Column(Boolean, default=True)
    status = Column(Enum(RoomStatus), default=RoomStatus.ACTIVE)
    agora_channel_name = Column(String(100), unique=True, nullable=False)

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    # Relationships
    creator = relationship("User", back_populates="created_rooms")
    participants = relationship("Participant", back_populates="room", cascade="all, delete")