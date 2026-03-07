"""
School activities and events models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    activity_name = Column(String, nullable=False)
    activity_type = Column(String)  # sports, arts, academic, etc.
    description = Column(Text)
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    location = Column(String)
    organizer = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    participations = relationship("ActivityParticipation", back_populates="activity")

class ActivityParticipation(Base):
    __tablename__ = "activity_participations"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    participation_type = Column(String)  # participant, winner, organizer, etc.
    achievement = Column(Text)
    photos = Column(Text)  # JSON array of photo URLs
    evaluation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    activity = relationship("Activity", back_populates="participations")
    student = relationship("Student", back_populates="activity_participations")





