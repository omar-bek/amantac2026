"""
Behavior monitoring router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from app.models.behavior import BehaviorType

router = APIRouter()

@router.post("/log")
def log_behavior(
    student_id: int,
    behavior_type: BehaviorType,
    description: str,
    location: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Log behavior (Teacher/Staff)"""
    if current_user.role.value not in ["teacher", "staff", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    behavior_log = models.BehaviorLog(
        student_id=student_id,
        behavior_type=behavior_type,
        description=description,
        location=location,
        created_by=current_user.id
    )
    db.add(behavior_log)
    db.commit()
    db.refresh(behavior_log)
    
    return behavior_log

@router.post("/note")
def create_behavior_note(
    student_id: int,
    behavior_type: BehaviorType,
    title: str,
    description: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create behavior note with notification (Teacher)"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create behavior notes")
    
    note = models.BehaviorNote(
        student_id=student_id,
        teacher_id=current_user.id,
        behavior_type=behavior_type,
        title=title,
        description=description
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    
    # Create notification for parent
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student and student.parent_id:
        notification = models.Notification(
            user_id=student.parent_id,
            notification_type=models.NotificationType.BEHAVIOR,
            title=f"ملاحظة سلوكية: {title}",
            message=description,
            status=models.NotificationStatus.PENDING
        )
        db.add(notification)
        db.commit()
    
    return note

@router.get("/student/{student_id}")
def get_student_behavior(
    student_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get behavior logs for a student"""
    logs = db.query(models.BehaviorLog).filter(
        models.BehaviorLog.student_id == student_id
    ).order_by(models.BehaviorLog.behavior_date.desc()).limit(limit).all()
    return logs

@router.get("/notes/{student_id}")
def get_behavior_notes(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get behavior notes for a student"""
    notes = db.query(models.BehaviorNote).filter(
        models.BehaviorNote.student_id == student_id
    ).order_by(models.BehaviorNote.note_date.desc()).all()
    return notes





