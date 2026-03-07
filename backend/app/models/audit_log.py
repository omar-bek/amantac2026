"""
Audit Log Model for Security & Privacy
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class AuditActionType(str, enum.Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    VIEW = "view"
    EXPORT = "export"
    APPROVE = "approve"
    REJECT = "reject"
    ACCESS_DENIED = "access_denied"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for unauthenticated actions
    action_type = Column(Enum(AuditActionType), nullable=False)
    resource_type = Column(String, nullable=False)  # e.g., "student", "assignment", "message"
    resource_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True)  # Additional context (renamed from metadata to avoid SQLAlchemy conflict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User")

