"""
User model for authentication and authorization
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"  # School Admin
    PARENT = "parent"
    TEACHER = "teacher"
    STAFF = "staff"
    DRIVER = "driver"
    STUDENT = "student"  # Optional student portal
    SUPER_ADMIN = "super_admin"  # Ministry/Super Admin
    GOVERNMENT_ADMIN = "government_admin"  # Government/Authority Admin
    AUTHORITY_ADMIN = "authority_admin"  # Authority Admin (alternative)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    students = relationship("Student", back_populates="parent", foreign_keys="Student.parent_id")
    created_pickup_requests = relationship("PickupRequest", back_populates="parent", foreign_keys="PickupRequest.parent_id")
    dismissal_requests = relationship("DismissalRequest", back_populates="parent", foreign_keys="DismissalRequest.parent_id")
    behavior_notes = relationship("BehaviorNote", back_populates="teacher", foreign_keys="BehaviorNote.teacher_id")
    grades = relationship("Grade", back_populates="teacher", foreign_keys="Grade.teacher_id")

