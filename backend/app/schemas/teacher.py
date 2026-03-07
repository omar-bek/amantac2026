"""
Teacher-specific schemas for assignments, evaluations, and messages
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.teacher import (
    AssignmentType, 
    EvaluationType,
    CommitmentLevel
)

# Assignment Schemas
class AssignmentCreate(BaseModel):
    assignment_name: str
    subject: str
    description: Optional[str] = None
    due_date: datetime
    max_grade: float = 100.0
    class_name: Optional[str] = None
    grade: Optional[str] = None
    academic_year: Optional[str] = None
    assignment_type: str = "individual"  # individual or group
    file_path: Optional[str] = None

class AssignmentResponse(BaseModel):
    id: int
    assignment_name: str
    subject: str
    description: Optional[str]
    due_date: datetime
    max_grade: float
    class_name: Optional[str]
    grade: Optional[str]
    academic_year: Optional[str]
    teacher_id: Optional[int]
    assignment_type: str
    file_path: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Assignment Submission Schemas
class AssignmentSubmissionCreate(BaseModel):
    assignment_id: int
    student_id: int
    file_path: Optional[str] = None
    comment: Optional[str] = None

class AssignmentSubmissionUpdate(BaseModel):
    teacher_comment: Optional[str] = None
    grade: Optional[float] = None
    submission_status: Optional[str] = None

class AssignmentSubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submission_status: str
    submitted_at: Optional[datetime]
    file_path: Optional[str]
    comment: Optional[str]
    teacher_comment: Optional[str]
    grade: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Student Evaluation Schemas
class StudentEvaluationCreate(BaseModel):
    student_id: int
    evaluation_type: str  # daily or monthly
    evaluation_date: datetime
    # Daily evaluation fields
    commitment_level: Optional[str] = None
    interaction_level: Optional[str] = None
    behavior_level: Optional[str] = None
    participation_level: Optional[str] = None
    # Monthly evaluation fields
    performance_trend: Optional[str] = None
    interaction_trend: Optional[str] = None
    commitment_trend: Optional[str] = None
    # Common fields
    educational_notes: Optional[str] = None
    private_notes: Optional[str] = None
    shared_notes: Optional[str] = None

class StudentEvaluationResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    evaluation_type: str
    evaluation_date: datetime
    commitment_level: Optional[str]
    interaction_level: Optional[str]
    behavior_level: Optional[str]
    participation_level: Optional[str]
    performance_trend: Optional[str]
    interaction_trend: Optional[str]
    commitment_trend: Optional[str]
    educational_notes: Optional[str]
    private_notes: Optional[str]
    shared_notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Teacher Message Schemas
class TeacherMessageCreate(BaseModel):
    student_id: int
    parent_id: int
    message: str
    attachment_path: Optional[str] = None

class TeacherMessageResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    parent_id: int
    message: str
    attachment_path: Optional[str]
    is_from_teacher: bool
    status: str
    read_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Teacher Class Schemas
class TeacherClassCreate(BaseModel):
    class_name: str
    subject: Optional[str] = None
    grade: str
    academic_year: Optional[str] = None

class TeacherClassResponse(BaseModel):
    id: int
    teacher_id: int
    class_name: str
    subject: Optional[str]
    grade: str
    academic_year: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard Stats Schema
class TeacherDashboardStats(BaseModel):
    students_today: int
    assignments_today: int
    pending_evaluations: int
    unread_messages: int

