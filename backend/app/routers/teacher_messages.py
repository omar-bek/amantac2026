"""
Teacher-Parent Messaging Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app import models
from app import schemas
from app.schemas import teacher as teacher_schemas
from app.routers.auth import get_current_user

router = APIRouter(prefix="/teacher/messages", tags=["teacher-messages"])

def verify_teacher(current_user: models.User = Depends(get_current_user)):
    """Verify user is a teacher"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")
    return current_user

@router.post("/", response_model=teacher_schemas.TeacherMessageResponse)
def send_message(
    message: teacher_schemas.TeacherMessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Send a message to a parent"""
    # Verify student exists and has the specified parent
    student = db.query(models.Student).filter(
        models.Student.id == message.student_id,
        models.Student.parent_id == message.parent_id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found or parent mismatch")
    
    db_message = models.TeacherMessage(
        student_id=message.student_id,
        teacher_id=current_user.id,
        parent_id=message.parent_id,
        message=message.message,
        attachment_path=message.attachment_path,
        is_from_teacher=True,
        status="sent"
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Create notification for parent
    # TODO: Implement notification system
    
    return db_message

@router.get("/", response_model=List[teacher_schemas.TeacherMessageResponse])
def get_messages(
    student_id: Optional[int] = None,
    parent_id: Optional[int] = None,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get messages for current teacher"""
    query = db.query(models.TeacherMessage).filter(
        models.TeacherMessage.teacher_id == current_user.id
    )
    
    if student_id:
        query = query.filter(models.TeacherMessage.student_id == student_id)
    if parent_id:
        query = query.filter(models.TeacherMessage.parent_id == parent_id)
    if unread_only:
        query = query.filter(models.TeacherMessage.status != "read")
    
    messages = query.order_by(models.TeacherMessage.created_at.desc()).all()
    return messages

@router.get("/student/{student_id}", response_model=List[teacher_schemas.TeacherMessageResponse])
def get_student_messages(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get all messages for a specific student"""
    messages = db.query(models.TeacherMessage).filter(
        models.TeacherMessage.student_id == student_id,
        models.TeacherMessage.teacher_id == current_user.id
    ).order_by(models.TeacherMessage.created_at.asc()).all()
    
    return messages

@router.get("/{message_id}", response_model=teacher_schemas.TeacherMessageResponse)
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get message by ID"""
    message = db.query(models.TeacherMessage).filter(
        models.TeacherMessage.id == message_id,
        models.TeacherMessage.teacher_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message

@router.put("/{message_id}/read")
def mark_message_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Mark message as read"""
    message = db.query(models.TeacherMessage).filter(
        models.TeacherMessage.id == message_id,
        models.TeacherMessage.teacher_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.status = "read"
    message.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Message marked as read"}

@router.get("/unread/count")
def get_unread_messages_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get count of unread messages"""
    count = db.query(models.TeacherMessage).filter(
        models.TeacherMessage.teacher_id == current_user.id,
        models.TeacherMessage.is_from_teacher == False,  # Messages from parents
        models.TeacherMessage.status != "read"
    ).count()
    
    return {"count": count}

