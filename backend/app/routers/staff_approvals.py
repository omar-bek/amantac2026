"""
Staff Approvals & Operations Router
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List, Optional
from app.database import get_db
from app import models
from app.models.pickup import PickupStatus
from app.models.dismissal import DismissalStatus
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/staff/approvals", tags=["staff-approvals"])

def verify_staff(current_user: models.User = Depends(get_current_user)):
    """Verify user is staff"""
    if current_user.role.value not in ["staff", "admin"]:
        raise HTTPException(status_code=403, detail="Only staff can access this endpoint")
    return current_user

class PickupRequestDetail(BaseModel):
    id: int
    student_id: int
    student_name: str
    parent_id: int
    parent_name: str
    recipient_name: str
    recipient_phone: Optional[str]
    recipient_relation: Optional[str]
    pickup_date: str
    pickup_time: str
    reason: Optional[str]
    status: str
    requested_at: str
    approved_by: Optional[int]
    approved_at: Optional[str]

class DismissalRequestDetail(BaseModel):
    id: int
    student_id: int
    student_name: str
    parent_id: int
    parent_name: str
    dismissal_date: str
    dismissal_time: str
    reason_type: str
    reason_details: Optional[str]
    status: str
    requested_at: str
    teacher_approved_by: Optional[int]
    admin_approved_by: Optional[int]

@router.get("/pickup-requests", response_model=List[PickupRequestDetail])
def get_pending_pickup_requests(
    status: Optional[str] = Query(None, description="Filter by status: pending, approved, rejected"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get pickup requests (all or filtered by status)"""
    query = db.query(models.PickupRequest)
    
    if status:
        query = query.filter(models.PickupRequest.status == PickupStatus(status))
    else:
        # Default: get pending requests
        query = query.filter(models.PickupRequest.status == PickupStatus.PENDING)
    
    requests = query.order_by(models.PickupRequest.created_at.desc()).all()
    
    result = []
    for req in requests:
        student = db.query(models.Student).filter(models.Student.id == req.student_id).first()
        parent = db.query(models.User).filter(models.User.id == req.parent_id).first()
        
        result.append(PickupRequestDetail(
            id=req.id,
            student_id=req.student_id,
            student_name=student.full_name if student else "غير معروف",
            parent_id=req.parent_id,
            parent_name=parent.full_name if parent else "غير معروف",
            recipient_name=req.recipient_name,
            recipient_phone=req.recipient_phone,
            recipient_relation=req.recipient_relation,
            pickup_date=req.pickup_date.isoformat() if req.pickup_date else "",
            pickup_time=req.pickup_time.isoformat() if req.pickup_time else "",
            reason=req.reason,
            status=req.status.value,
            requested_at=req.created_at.isoformat() if req.created_at else "",
            approved_by=req.approved_by,
            approved_at=req.approved_at.isoformat() if req.approved_at else None
        ))
    
    return result

@router.get("/dismissal-requests", response_model=List[DismissalRequestDetail])
def get_pending_dismissal_requests(
    status: Optional[str] = Query(None, description="Filter by status: pending, teacher_approved, admin_approved, rejected"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get dismissal requests (all or filtered by status)"""
    query = db.query(models.DismissalRequest)
    
    if status:
        query = query.filter(models.DismissalRequest.status == DismissalStatus(status))
    else:
        # Default: get pending requests
        query = query.filter(models.DismissalRequest.status == DismissalStatus.PENDING)
    
    requests = query.order_by(models.DismissalRequest.created_at.desc()).all()
    
    result = []
    for req in requests:
        student = db.query(models.Student).filter(models.Student.id == req.student_id).first()
        parent = db.query(models.User).filter(models.User.id == req.parent_id).first()
        
        result.append(DismissalRequestDetail(
            id=req.id,
            student_id=req.student_id,
            student_name=student.full_name if student else "غير معروف",
            parent_id=req.parent_id,
            parent_name=parent.full_name if parent else "غير معروف",
            dismissal_date=req.dismissal_date.isoformat() if req.dismissal_date else "",
            dismissal_time=req.dismissal_time.isoformat() if req.dismissal_time else "",
            reason_type=req.reason_type.value if req.reason_type else "",
            reason_details=req.reason_details,
            status=req.status.value,
            requested_at=req.created_at.isoformat() if req.created_at else "",
            teacher_approved_by=req.teacher_approved_by,
            admin_approved_by=req.admin_approved_by
        ))
    
    return result

@router.post("/pickup/{request_id}/approve")
def approve_pickup_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Approve a pickup request"""
    request = db.query(models.PickupRequest).filter(models.PickupRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Pickup request not found")
    
    if request.status != PickupStatus.PENDING:
        raise HTTPException(status_code=400, detail="Request is not pending")
    
    request.status = PickupStatus.APPROVED
    request.approved_by = current_user.id
    request.approved_at = datetime.now()
    
    db.commit()
    db.refresh(request)
    
    return {"message": "Pickup request approved successfully", "request": request}

@router.post("/pickup/{request_id}/reject")
def reject_pickup_request(
    request_id: int,
    rejection_reason: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Reject a pickup request"""
    request = db.query(models.PickupRequest).filter(models.PickupRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Pickup request not found")
    
    if request.status != PickupStatus.PENDING:
        raise HTTPException(status_code=400, detail="Request is not pending")
    
    request.status = PickupStatus.REJECTED
    request.approved_by = current_user.id
    request.approved_at = datetime.now()
    # Note: You may want to add a rejection_reason field to PickupRequest model
    
    db.commit()
    db.refresh(request)
    
    return {"message": "Pickup request rejected successfully", "request": request}

@router.post("/dismissal/{request_id}/approve")
def approve_dismissal_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Approve a dismissal request (admin approval)"""
    request = db.query(models.DismissalRequest).filter(models.DismissalRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Dismissal request not found")
    
    if request.status not in [DismissalStatus.PENDING, DismissalStatus.TEACHER_APPROVED]:
        raise HTTPException(status_code=400, detail="Request cannot be approved")
    
    request.status = DismissalStatus.ADMIN_APPROVED
    request.admin_approved_by = current_user.id
    
    db.commit()
    db.refresh(request)
    
    return {"message": "Dismissal request approved successfully", "request": request}

@router.post("/dismissal/{request_id}/reject")
def reject_dismissal_request(
    request_id: int,
    rejection_reason: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Reject a dismissal request"""
    request = db.query(models.DismissalRequest).filter(models.DismissalRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Dismissal request not found")
    
    if request.status == DismissalStatus.REJECTED:
        raise HTTPException(status_code=400, detail="Request is already rejected")
    
    request.status = DismissalStatus.REJECTED
    request.rejected_by = current_user.id
    request.rejection_reason = rejection_reason
    
    db.commit()
    db.refresh(request)
    
    return {"message": "Dismissal request rejected successfully", "request": request}

