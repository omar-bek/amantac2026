"""
Academic performance router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app import models
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/grades/{student_id}")
def get_student_grades(
    student_id: int,
    subject: Optional[str] = None,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get student grades"""
    query = db.query(models.Grade).filter(models.Grade.student_id == student_id)
    
    if subject:
        query = query.filter(models.Grade.subject == subject)
    if semester:
        query = query.filter(models.Grade.semester == semester)
    
    grades = query.order_by(models.Grade.created_at.desc()).all()
    return grades

@router.get("/exams")
def get_exams(
    class_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get exam schedule"""
    query = db.query(models.Exam)
    if class_name:
        query = query.filter(models.Exam.class_name == class_name)
    
    exams = query.order_by(models.Exam.exam_date).all()
    return exams

@router.get("/assignments")
def get_assignments(
    class_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get assignments"""
    query = db.query(models.Assignment).filter(models.Assignment.is_active == True)
    if class_name:
        query = query.filter(models.Assignment.class_name == class_name)
    
    assignments = query.order_by(models.Assignment.due_date).all()
    return assignments

@router.get("/quizzes")
def get_quizzes(
    class_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get quizzes"""
    query = db.query(models.Quiz)
    if class_name:
        query = query.filter(models.Quiz.class_name == class_name)
    
    quizzes = query.order_by(models.Quiz.quiz_date).all()
    return quizzes

@router.post("/grade")
def add_grade(
    student_id: int,
    subject: str,
    grade_value: float,
    max_grade: float = 100.0,
    exam_id: Optional[int] = None,
    assignment_id: Optional[int] = None,
    quiz_id: Optional[int] = None,
    semester: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Add grade (Teacher only)"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can add grades")
    
    grade = models.Grade(
        student_id=student_id,
        teacher_id=current_user.id,
        subject=subject,
        grade_value=grade_value,
        max_grade=max_grade,
        exam_id=exam_id,
        assignment_id=assignment_id,
        quiz_id=quiz_id,
        semester=semester,
        notes=notes
    )
    db.add(grade)
    db.commit()
    db.refresh(grade)
    
    return grade





