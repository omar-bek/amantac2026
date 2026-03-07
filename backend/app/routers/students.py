"""
Students router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/")
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all students"""
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get student by ID"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/parent/{parent_id}")
def get_students_by_parent(
    parent_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all students for a parent"""
    students = db.query(models.Student).filter(models.Student.parent_id == parent_id).all()
    return students





