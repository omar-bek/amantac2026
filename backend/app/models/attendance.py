"""
Attendance tracking models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class AttendanceType(str, enum.Enum):
    BOARD_BUS = "board_bus"
    ENTER_SCHOOL = "enter_school"
    EXIT_SCHOOL = "exit_school"
    ARRIVE_HOME = "arrive_home"

class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(Enum(AttendanceStatus), nullable=False)
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    logs = relationship("AttendanceLog", back_populates="attendance")

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    attendance_id = Column(Integer, ForeignKey("attendance.id"), nullable=True)
    attendance_type = Column(Enum(AttendanceType), nullable=False)
    device_id = Column(String)  # RFID tag, Smartwatch ID, etc.
    location = Column(String)  # GPS coordinates or location name
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    verified = Column(Boolean, default=False)

    # Relationships
    student = relationship("Student", back_populates="attendance_logs")
    attendance = relationship("Attendance", back_populates="logs")





