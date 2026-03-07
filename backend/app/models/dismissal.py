"""
Early Dismissal system models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class DismissalStatus(str, enum.Enum):
    PENDING = "pending"
    TEACHER_APPROVED = "teacher_approved"
    ADMIN_APPROVED = "admin_approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class DismissalReason(str, enum.Enum):
    MEDICAL = "medical"
    FAMILY = "family"
    EMERGENCY = "emergency"
    OTHER = "other"

class DismissalRequest(Base):
    __tablename__ = "dismissal_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dismissal_date = Column(DateTime(timezone=True), nullable=False)
    dismissal_time = Column(DateTime(timezone=True), nullable=False)
    reason_type = Column(Enum(DismissalReason), nullable=False)
    reason_details = Column(Text)
    status = Column(Enum(DismissalStatus), default=DismissalStatus.PENDING, index=True)
    teacher_approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    teacher_approved_at = Column(DateTime(timezone=True), nullable=True)
    admin_approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    admin_approved_at = Column(DateTime(timezone=True), nullable=True)
    rejected_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    rejection_reason = Column(Text)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("Student", back_populates="dismissal_requests")
    parent = relationship("User", back_populates="dismissal_requests", foreign_keys=[parent_id])
    teacher_approver = relationship("User", foreign_keys=[teacher_approved_by])
    admin_approver = relationship("User", foreign_keys=[admin_approved_by])
    rejector = relationship("User", foreign_keys=[rejected_by])





