"""
Academic performance models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class ExamType(str, enum.Enum):
    MIDTERM = "midterm"
    FINAL = "final"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    PROJECT = "project"

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False)
    grade_value = Column(Float, nullable=False)
    max_grade = Column(Float, default=100.0)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=True)
    semester = Column(String)  # First, Second, etc.
    academic_year = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("Student", back_populates="grades")
    teacher = relationship("User", back_populates="grades", foreign_keys=[teacher_id])
    exam = relationship("Exam", back_populates="grades")
    assignment = relationship("Assignment", back_populates="grades")
    quiz = relationship("Quiz", back_populates="grades")

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    exam_name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    exam_type = Column(Enum(ExamType), nullable=False)
    exam_date = Column(DateTime(timezone=True), nullable=False, index=True)
    max_grade = Column(Float, default=100.0)
    duration = Column(Integer)  # in minutes
    description = Column(Text)
    class_name = Column(String)
    academic_year = Column(String)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_path = Column(String, nullable=True)  # Path to exam PDF file
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    grades = relationship("Grade", back_populates="exam")
    teacher = relationship("User", foreign_keys=[teacher_id])

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    assignment_name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text)
    due_date = Column(DateTime(timezone=True), nullable=False, index=True)
    max_grade = Column(Float, default=100.0)
    class_name = Column(String)
    grade = Column(String, nullable=True)  # Grade level (e.g., "3A", "4B")
    academic_year = Column(String)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assignment_type = Column(String, default="individual")  # individual or group
    file_path = Column(String, nullable=True)  # Path to assignment file
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    grades = relationship("Grade", back_populates="assignment")
    submissions = relationship("AssignmentSubmission", back_populates="assignment", cascade="all, delete-orphan")
    teacher = relationship("User", foreign_keys=[teacher_id])

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    quiz_name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    quiz_date = Column(DateTime(timezone=True), nullable=False, index=True)
    max_grade = Column(Float, default=100.0)
    duration = Column(Integer)  # in minutes
    class_name = Column(String)
    academic_year = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    grades = relationship("Grade", back_populates="quiz")

