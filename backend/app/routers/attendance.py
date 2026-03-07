"""
Attendance tracking router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List, Optional
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from app.models.attendance import AttendanceType, AttendanceStatus

router = APIRouter()

@router.post("/log")
def log_attendance(
    student_id: int,
    attendance_type: AttendanceType,
    device_id: str,
    location: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Log attendance event (RFID/Smartwatch)"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Verify device
    device = db.query(models.StudentDevice).filter(
        models.StudentDevice.device_id == device_id,
        models.StudentDevice.student_id == student_id,
        models.StudentDevice.is_active == True
    ).first()
    if not device:
        raise HTTPException(status_code=403, detail="Device not authorized")
    
    # Create attendance log
    log = models.AttendanceLog(
        student_id=student_id,
        attendance_type=attendance_type,
        device_id=device_id,
        location=location,
        verified=True
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    
    # Update or create attendance record
    today = date.today()
    attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id,
        models.Attendance.date == today
    ).first()
    
    if not attendance:
        attendance = models.Attendance(
            student_id=student_id,
            date=datetime.now(),
            status=AttendanceStatus.PRESENT
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
    
    log.attendance_id = attendance.id
    db.commit()
    
    return log

@router.get("/student/{student_id}")
def get_student_attendance(
    student_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get student attendance records"""
    query = db.query(models.Attendance).filter(models.Attendance.student_id == student_id)
    
    if start_date:
        query = query.filter(models.Attendance.date >= start_date)
    if end_date:
        query = query.filter(models.Attendance.date <= end_date)
    
    attendance = query.order_by(models.Attendance.date.desc()).all()
    return attendance

@router.get("/logs/{student_id}")
def get_attendance_logs(
    student_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get attendance logs for a student"""
    logs = db.query(models.AttendanceLog).filter(
        models.AttendanceLog.student_id == student_id
    ).order_by(models.AttendanceLog.timestamp.desc()).limit(limit).all()
    return logs





