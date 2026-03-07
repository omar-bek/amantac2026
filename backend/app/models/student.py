"""
Student model and related devices
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class DeviceType(str, enum.Enum):
    RFID = "rfid"
    SMARTWATCH = "smartwatch"
    NFC = "nfc"
    BLUETOOTH = "bluetooth"

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False)  # School ID
    full_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    grade = Column(String)
    class_name = Column(String)
    parent_id = Column(Integer, ForeignKey("users.id"))
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    parent = relationship("User", back_populates="students", foreign_keys=[parent_id])
    bus = relationship("Bus", back_populates="students")
    devices = relationship("StudentDevice", back_populates="student", cascade="all, delete-orphan")
    attendance_logs = relationship("AttendanceLog", back_populates="student")
    pickup_requests = relationship("PickupRequest", back_populates="student")
    dismissal_requests = relationship("DismissalRequest", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    behavior_logs = relationship("BehaviorLog", back_populates="student")
    activity_participations = relationship("ActivityParticipation", back_populates="student")
    assignment_submissions = relationship("AssignmentSubmission", back_populates="student", cascade="all, delete-orphan")
    evaluations = relationship("StudentEvaluation", back_populates="student", cascade="all, delete-orphan")
    teacher_messages = relationship("TeacherMessage", back_populates="student", cascade="all, delete-orphan")

class StudentDevice(Base):
    __tablename__ = "student_devices"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    device_type = Column(Enum(DeviceType), nullable=False)
    device_id = Column(String, unique=True, nullable=False)  # RFID tag ID, Smartwatch ID, etc.
    device_name = Column(String)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    last_sync = Column(DateTime(timezone=True))

    # Relationships
    student = relationship("Student", back_populates="devices")

