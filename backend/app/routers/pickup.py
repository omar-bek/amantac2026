"""
Smart Private Pickup router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import uuid
import qrcode
from io import BytesIO
import base64
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from app.models.pickup import PickupStatus, VerificationMethod

router = APIRouter()

@router.post("/request")
def create_pickup_request(
    student_id: int,
    recipient_name: str,
    recipient_phone: str,
    recipient_relation: str,
    pickup_date: datetime,
    pickup_time: datetime,
    reason: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create pickup request from parent"""
    if current_user.role.value != "parent":
        raise HTTPException(status_code=403, detail="Only parents can create pickup requests")
    
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized for this student")
    
    # Generate QR code
    qr_code_value = str(uuid.uuid4())
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_code_value)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Create pickup request
    pickup_request = models.PickupRequest(
        student_id=student_id,
        parent_id=current_user.id,
        recipient_name=recipient_name,
        recipient_phone=recipient_phone,
        recipient_relation=recipient_relation,
        pickup_date=pickup_date,
        pickup_time=pickup_time,
        reason=reason,
        qr_code=qr_code_value,
        verification_method=VerificationMethod.QR_CODE,
        status=PickupStatus.PENDING
    )
    db.add(pickup_request)
    db.commit()
    db.refresh(pickup_request)
    
    return pickup_request

@router.post("/{request_id}/approve")
def approve_pickup_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Approve pickup request (Teacher/Admin)"""
    if current_user.role.value not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    request = db.query(models.PickupRequest).filter(models.PickupRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request.status = PickupStatus.APPROVED
    request.approved_by = current_user.id
    request.approved_at = datetime.now()
    db.commit()
    
    return request

@router.post("/{request_id}/verify")
def verify_pickup(
    request_id: int,
    verification_code: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Verify pickup with QR/NFC/Bluetooth code"""
    request = db.query(models.PickupRequest).filter(
        models.PickupRequest.id == request_id,
        models.PickupRequest.qr_code == verification_code
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Invalid verification code")
    
    if request.status != PickupStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Request not approved")
    
    # Create authorization
    authorization = models.PickupAuthorization(
        pickup_request_id=request_id,
        authorized_by=current_user.id,
        verification_code=verification_code,
        verified_at=datetime.now(),
        is_used=True
    )
    db.add(authorization)
    
    request.status = PickupStatus.COMPLETED
    request.completed_at = datetime.now()
    db.commit()
    
    return {"message": "Pickup verified successfully", "request": request}

@router.get("/student/{student_id}")
def get_pickup_requests(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get pickup requests for a student"""
    requests = db.query(models.PickupRequest).filter(
        models.PickupRequest.student_id == student_id
    ).order_by(models.PickupRequest.created_at.desc()).all()
    return requests





