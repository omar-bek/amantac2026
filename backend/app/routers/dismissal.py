"""
Early Dismissal router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from app.models.dismissal import DismissalStatus, DismissalReason

router = APIRouter()

@router.post("/request")
def create_dismissal_request(
    student_id: int,
    dismissal_date: datetime,
    dismissal_time: datetime,
    reason_type: DismissalReason,
    reason_details: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create early dismissal request"""
    if current_user.role.value != "parent":
        raise HTTPException(status_code=403, detail="Only parents can create dismissal requests")
    
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized for this student")
    
    dismissal_request = models.DismissalRequest(
        student_id=student_id,
        parent_id=current_user.id,
        dismissal_date=dismissal_date,
        dismissal_time=dismissal_time,
        reason_type=reason_type,
        reason_details=reason_details,
        status=DismissalStatus.PENDING
    )
    db.add(dismissal_request)
    db.commit()
    db.refresh(dismissal_request)
    
    return dismissal_request

@router.post("/{request_id}/teacher-approve")
def teacher_approve_dismissal(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Teacher approval for dismissal"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can approve")
    
    request = db.query(models.DismissalRequest).filter(models.DismissalRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request.status = DismissalStatus.TEACHER_APPROVED
    request.teacher_approved_by = current_user.id
    request.teacher_approved_at = datetime.now()
    db.commit()
    
    return request

@router.post("/{request_id}/admin-approve")
def admin_approve_dismissal(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Admin approval for dismissal"""
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only admins can approve")
    
    request = db.query(models.DismissalRequest).filter(models.DismissalRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != DismissalStatus.TEACHER_APPROVED:
        raise HTTPException(status_code=400, detail="Teacher approval required first")
    
    request.status = DismissalStatus.ADMIN_APPROVED
    request.admin_approved_by = current_user.id
    request.admin_approved_at = datetime.now()
    db.commit()
    
    return request

@router.get("/student/{student_id}")
def get_dismissal_requests(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get dismissal requests for a student"""
    requests = db.query(models.DismissalRequest).filter(
        models.DismissalRequest.student_id == student_id
    ).order_by(models.DismissalRequest.created_at.desc()).all()
    return requests





