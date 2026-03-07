"""
Staff Bus & Transport Management Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta
from typing import List, Optional
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/staff/buses", tags=["staff-buses"])

def verify_staff(current_user: models.User = Depends(get_current_user)):
    """Verify user is staff"""
    if current_user.role.value not in ["staff", "admin"]:
        raise HTTPException(status_code=403, detail="Only staff can access this endpoint")
    return current_user

class BusDetail(BaseModel):
    id: int
    bus_number: str
    driver_id: Optional[int]
    driver_name: Optional[str]
    route_name: Optional[str]
    capacity: Optional[int]
    is_active: bool
    students_count: int
    on_time_rate: float

class BusRouteDetail(BaseModel):
    bus_id: int
    bus_number: str
    route_name: str
    students_on_route: int
    stops_count: int
    estimated_duration: Optional[int]

@router.get("/", response_model=List[BusDetail])
def get_all_buses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get all buses with detailed information"""
    buses = db.query(models.Bus).filter(models.Bus.is_active == True).all()
    
    result = []
    for bus in buses:
        # Count students assigned to this bus
        students_count = db.query(models.Student).filter(
            models.Student.bus_id == bus.id,
            models.Student.is_active == True
        ).count()
        
        # Get driver name
        driver_name = None
        if bus.driver_id:
            driver = db.query(models.User).filter(models.User.id == bus.driver_id).first()
            driver_name = driver.full_name if driver else None
        
        # Simplified on-time rate (can be enhanced with actual trip data)
        on_time_rate = 95.0  # Placeholder
        
        result.append(BusDetail(
            id=bus.id,
            bus_number=bus.bus_number,
            driver_id=bus.driver_id,
            driver_name=driver_name,
            route_name=bus.route_name,
            capacity=bus.capacity,
            is_active=bus.is_active,
            students_count=students_count,
            on_time_rate=on_time_rate
        ))
    
    return result

@router.get("/{bus_id}/details", response_model=BusDetail)
def get_bus_details(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get detailed information about a specific bus"""
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    # Count students
    students_count = db.query(models.Student).filter(
        models.Student.bus_id == bus.id,
        models.Student.is_active == True
    ).count()
    
    # Get driver name
    driver_name = None
    if bus.driver_id:
        driver = db.query(models.User).filter(models.User.id == bus.driver_id).first()
        driver_name = driver.full_name if driver else None
    
    # Simplified on-time rate
    on_time_rate = 95.0  # Placeholder
    
    return BusDetail(
        id=bus.id,
        bus_number=bus.bus_number,
        driver_id=bus.driver_id,
        driver_name=driver_name,
        route_name=bus.route_name,
        capacity=bus.capacity,
        is_active=bus.is_active,
        students_count=students_count,
        on_time_rate=on_time_rate
    )

@router.get("/{bus_id}/students")
def get_bus_students(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get students assigned to a specific bus"""
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    students = db.query(models.Student).filter(
        models.Student.bus_id == bus_id,
        models.Student.is_active == True
    ).all()
    
    return [
        {
            "id": student.id,
            "full_name": student.full_name,
            "student_id": student.student_id,
            "grade": student.grade,
            "class_name": student.class_name,
            "parent_name": db.query(models.User).filter(models.User.id == student.parent_id).first().full_name if student.parent_id else None
        }
        for student in students
    ]

@router.get("/routes/", response_model=List[BusRouteDetail])
def get_all_routes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get all bus routes with details"""
    buses = db.query(models.Bus).filter(
        models.Bus.is_active == True,
        models.Bus.route_name.isnot(None)
    ).all()
    
    result = []
    for bus in buses:
        students_count = db.query(models.Student).filter(
            models.Student.bus_id == bus.id,
            models.Student.is_active == True
        ).count()
        
        # Get route stops (if BusRoute model exists with stops)
        # For now, using placeholder
        stops_count = 5  # Placeholder
        
        result.append(BusRouteDetail(
            bus_id=bus.id,
            bus_number=bus.bus_number,
            route_name=bus.route_name or "غير محدد",
            students_on_route=students_count,
            stops_count=stops_count,
            estimated_duration=None  # Can be enhanced with route data
        ))
    
    return result





