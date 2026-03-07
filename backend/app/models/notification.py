"""
Notification system model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class NotificationType(str, enum.Enum):
    ATTENDANCE = "attendance"
    PICKUP = "pickup"
    DISMISSAL = "dismissal"
    GRADE = "grade"
    BEHAVIOR = "behavior"
    ACTIVITY = "activity"
    EXAM = "exam"
    ASSIGNMENT = "assignment"
    GENERAL = "general"

class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING, index=True)
    data = Column(JSON)  # Additional data for the notification
    sent_at = Column(DateTime(timezone=True), nullable=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User")





