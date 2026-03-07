"""
Buses router - Real-time tracking
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/")
def get_buses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all active buses"""
    buses = db.query(models.Bus).filter(models.Bus.is_active == True).all()
    return buses

@router.get("/{bus_id}")
def get_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get bus details"""
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus

@router.get("/{bus_id}/location")
def get_bus_location(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get latest bus location"""
    location = db.query(models.BusLocation).filter(
        models.BusLocation.bus_id == bus_id
    ).order_by(models.BusLocation.timestamp.desc()).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.get("/{bus_id}/students")
def get_bus_students(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all students on a bus"""
    students = db.query(models.Student).filter(models.Student.bus_id == bus_id).all()
    return students





