"""
Behavior monitoring models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class BehaviorType(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class BehaviorLog(Base):
    __tablename__ = "behavior_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    behavior_date = Column(DateTime(timezone=True), nullable=False, index=True)
    behavior_type = Column(Enum(BehaviorType), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String)  # classroom, playground, etc.
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("Student", back_populates="behavior_logs")
    creator = relationship("User", foreign_keys=[created_by])

class BehaviorNote(Base):
    __tablename__ = "behavior_notes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    note_date = Column(DateTime(timezone=True), nullable=False, index=True)
    behavior_type = Column(Enum(BehaviorType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    is_notified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("Student")
    teacher = relationship("User", back_populates="behavior_notes", foreign_keys=[teacher_id])





