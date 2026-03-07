"""
Staff Dashboard Router - Statistics and Overview
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta
from typing import List
from app.database import get_db
from app import models
from app.models.pickup import PickupStatus
from app.models.dismissal import DismissalStatus
from app.models.attendance import AttendanceStatus
from app.models.behavior import BehaviorType
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/staff/dashboard", tags=["staff-dashboard"])

def verify_staff(current_user: models.User = Depends(get_current_user)):
    """Verify user is staff"""
    if current_user.role.value not in ["staff", "admin"]:
        raise HTTPException(status_code=403, detail="Only staff can access this endpoint")
    return current_user

class StaffDashboardStats(BaseModel):
    total_students: int
    students_present_today: int
    students_absent_today: int
    total_teachers: int
    teachers_active_today: int
    total_buses: int
    active_buses: int
    total_drivers: int
    active_drivers: int
    todays_pickups: int
    todays_dismissals: int
    pending_pickup_approvals: int
    pending_dismissal_approvals: int
    alerts_count: int
    incidents_count: int

class AttendanceTrend(BaseModel):
    date: str
    present: int
    absent: int
    attendance_rate: float

class TransportEfficiency(BaseModel):
    bus_number: str
    route_name: str
    students_on_route: int
    on_time_rate: float
    status: str

@router.get("/stats", response_model=StaffDashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get staff dashboard statistics"""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    # Total students
    total_students = db.query(models.Student).filter(
        models.Student.is_active == True
    ).count()
    
    # Students present/absent today - check Attendance table
    students_present_today = db.query(models.Attendance).filter(
        func.date(models.Attendance.date) == today,
        models.Attendance.status == AttendanceStatus.PRESENT
    ).count()
    
    students_absent_today = max(0, total_students - students_present_today)
    
    # Total teachers
    total_teachers = db.query(models.User).filter(
        models.User.role == models.UserRole.TEACHER,
        models.User.is_active == True
    ).count()
    
    # Teachers active today (teachers with any activity today)
    teachers_active_today = db.query(func.count(func.distinct(models.TeacherMessage.teacher_id))).filter(
        models.TeacherMessage.created_at >= today_start
    ).scalar() or 0
    
    # Total buses
    total_buses = db.query(models.Bus).filter(
        models.Bus.is_active == True
    ).count()
    
    # Active buses (buses with active routes or current trips)
    active_buses = total_buses  # Simplified - can be enhanced with trip status
    
    # Total drivers
    total_drivers = db.query(models.User).filter(
        models.User.role == models.UserRole.DRIVER,
        models.User.is_active == True
    ).count()
    
    # Active drivers (drivers assigned to active buses)
    active_drivers = db.query(func.count(func.distinct(models.Bus.driver_id))).filter(
        models.Bus.is_active == True,
        models.Bus.driver_id.isnot(None)
    ).scalar() or 0
    
    # Today's pickups (pickups scheduled for today)
    todays_pickups = db.query(models.PickupRequest).filter(
        models.PickupRequest.pickup_date >= today_start,
        models.PickupRequest.pickup_date <= today_end,
        models.PickupRequest.status == PickupStatus.APPROVED
    ).count()
    
    # Today's dismissals (dismissals scheduled for today)
    todays_dismissals = db.query(models.DismissalRequest).filter(
        models.DismissalRequest.dismissal_date >= today_start,
        models.DismissalRequest.dismissal_date <= today_end,
        models.DismissalRequest.status == DismissalStatus.ADMIN_APPROVED
    ).count()
    
    # Pending pickup approvals
    pending_pickup_approvals = db.query(models.PickupRequest).filter(
        models.PickupRequest.status == PickupStatus.PENDING
    ).count()
    
    # Pending dismissal approvals
    pending_dismissal_approvals = db.query(models.DismissalRequest).filter(
        models.DismissalRequest.status == DismissalStatus.PENDING
    ).count()
    
    # Alerts count (non-critical behavior incidents) - using behavior_date field
    alerts_count = db.query(models.BehaviorLog).filter(
        models.BehaviorLog.behavior_type.in_([BehaviorType.NEUTRAL, BehaviorType.POSITIVE]),
        func.date(models.BehaviorLog.behavior_date) >= today - timedelta(days=7)
    ).count()
    
    # Incidents count (recent behavior logs)
    incidents_count = db.query(models.BehaviorLog).filter(
        func.date(models.BehaviorLog.behavior_date) >= today - timedelta(days=7)
    ).count()
    
    return StaffDashboardStats(
        total_students=total_students,
        students_present_today=students_present_today,
        students_absent_today=students_absent_today,
        total_teachers=total_teachers,
        teachers_active_today=teachers_active_today,
        total_buses=total_buses,
        active_buses=active_buses,
        total_drivers=total_drivers,
        active_drivers=active_drivers,
        todays_pickups=todays_pickups,
        todays_dismissals=todays_dismissals,
        pending_pickup_approvals=pending_pickup_approvals,
        pending_dismissal_approvals=pending_dismissal_approvals,
        alerts_count=alerts_count,
        incidents_count=incidents_count
    )

@router.get("/attendance-trend", response_model=List[AttendanceTrend])
def get_attendance_trend(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get attendance trend for the last N days"""
    start_date = date.today() - timedelta(days=days)
    
    trends = []
    total_students = db.query(models.Student).filter(
        models.Student.is_active == True
    ).count()
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        present_count = db.query(models.Attendance).filter(
            func.date(models.Attendance.date) == current_date,
            models.Attendance.status == AttendanceStatus.PRESENT
        ).count()
        
        absent_count = max(0, total_students - present_count)
        attendance_rate = (present_count / total_students * 100) if total_students > 0 else 0
        
        trends.append(AttendanceTrend(
            date=current_date.isoformat(),
            present=present_count,
            absent=absent_count,
            attendance_rate=round(attendance_rate, 2)
        ))
    
    return trends

@router.get("/transport-efficiency", response_model=List[TransportEfficiency])
def get_transport_efficiency(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get transport efficiency metrics"""
    buses = db.query(models.Bus).filter(
        models.Bus.is_active == True
    ).all()
    
    efficiency_data = []
    for bus in buses:
        # Count students assigned to this bus
        students_on_route = db.query(models.Student).filter(
            models.Student.bus_id == bus.id,
            models.Student.is_active == True
        ).count()
        
        # Simplified on-time rate (can be enhanced with actual trip data)
        on_time_rate = 95.0  # Placeholder
        
        # Bus status
        status = "active" if bus.is_active else "inactive"
        
        efficiency_data.append(TransportEfficiency(
            bus_number=bus.bus_number,
            route_name=bus.route_name or "غير محدد",
            students_on_route=students_on_route,
            on_time_rate=on_time_rate,
            status=status
        ))
    
    return efficiency_data
