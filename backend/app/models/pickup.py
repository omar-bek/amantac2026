"""
Smart Private Pickup system models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class PickupStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class VerificationMethod(str, enum.Enum):
    QR_CODE = "qr_code"
    NFC = "nfc"
    BLUETOOTH = "bluetooth"
    MANUAL = "manual"

class PickupRequest(Base):
    __tablename__ = "pickup_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_name = Column(String, nullable=False)
    recipient_phone = Column(String)
    recipient_relation = Column(String)  # father, mother, relative, etc.
    pickup_date = Column(DateTime(timezone=True), nullable=False)
    pickup_time = Column(DateTime(timezone=True), nullable=False)
    reason = Column(Text)
    status = Column(Enum(PickupStatus), default=PickupStatus.PENDING, index=True)
    qr_code = Column(String, unique=True)  # Generated QR code for verification
    verification_method = Column(Enum(VerificationMethod))
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("Student", back_populates="pickup_requests")
    parent = relationship("User", back_populates="created_pickup_requests", foreign_keys=[parent_id])
    approver = relationship("User", foreign_keys=[approved_by])
    authorizations = relationship("PickupAuthorization", back_populates="pickup_request")

class PickupAuthorization(Base):
    __tablename__ = "pickup_authorizations"

    id = Column(Integer, primary_key=True, index=True)
    pickup_request_id = Column(Integer, ForeignKey("pickup_requests.id"), nullable=False)
    authorized_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Teacher/Staff
    verification_code = Column(String, unique=True)  # QR/NFC/Bluetooth code
    verified_at = Column(DateTime(timezone=True), nullable=True)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    pickup_request = relationship("PickupRequest", back_populates="authorizations")
    authorizer = relationship("User", foreign_keys=[authorized_by])





