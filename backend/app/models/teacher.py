"""
Teacher-specific models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class AssignmentType(str, enum.Enum):
    INDIVIDUAL = "individual"
    GROUP = "group"

class EvaluationType(str, enum.Enum):
    DAILY = "daily"
    MONTHLY = "monthly"

class CommitmentLevel(str, enum.Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_SUPPORT = "needs_support"

class TrendLevel(str, enum.Enum):
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    grade = Column(Integer, nullable=True)

    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="assignment_submissions")

class StudentEvaluation(Base):
    __tablename__ = "student_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    evaluation_type = Column(Enum(EvaluationType), nullable=False)
    evaluation_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Daily evaluation fields
    commitment_level = Column(Enum(CommitmentLevel), nullable=True)
    interaction_level = Column(Enum(CommitmentLevel), nullable=True)
    behavior_level = Column(Enum(CommitmentLevel), nullable=True)
    participation_level = Column(Enum(CommitmentLevel), nullable=True)
    
    # Monthly evaluation fields
    performance_trend = Column(Enum(TrendLevel), nullable=True)
    interaction_trend = Column(Enum(TrendLevel), nullable=True)
    commitment_trend = Column(Enum(TrendLevel), nullable=True)
    
    # Notes
    educational_notes = Column(Text, nullable=True)  # Shared with parents
    private_notes = Column(Text, nullable=True)  # Teacher only
    shared_notes = Column(Text, nullable=True)  # Additional shared notes
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("Student", back_populates="evaluations")
    teacher = relationship("User")

class TeacherMessage(Base):
    __tablename__ = "teacher_messages"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    message = Column(Text, nullable=False)
    attachment_path = Column(String, nullable=True)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    teacher = relationship("User", foreign_keys=[teacher_id])
    parent = relationship("User", foreign_keys=[parent_id])
    student = relationship("Student", back_populates="teacher_messages")

class TeacherClass(Base):
    __tablename__ = "teacher_classes"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_name = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    academic_year = Column(String, nullable=True)

    # Relationships
    teacher = relationship("User")

class AnnouncementPriority(str, enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

class TeacherAnnouncement(Base):
    __tablename__ = "teacher_announcements"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    target_class = Column(String, nullable=True)  # Class name or "all"
    priority = Column(Enum(AnnouncementPriority), default=AnnouncementPriority.NORMAL)
    send_notification = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    teacher = relationship("User")
