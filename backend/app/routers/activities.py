"""
School activities router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app import models
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/")
def get_activities(
    is_active: bool = True,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all activities"""
    activities = db.query(models.Activity).filter(
        models.Activity.is_active == is_active
    ).order_by(models.Activity.start_date).all()
    return activities

@router.get("/{activity_id}")
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get activity details"""
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.get("/student/{student_id}")
def get_student_activities(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get activities for a student"""
    participations = db.query(models.ActivityParticipation).filter(
        models.ActivityParticipation.student_id == student_id
    ).all()
    return participations

@router.post("/participation")
def add_activity_participation(
    activity_id: int,
    student_id: int,
    participation_type: str,
    achievement: str = None,
    evaluation: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Add student participation in activity"""
    participation = models.ActivityParticipation(
        activity_id=activity_id,
        student_id=student_id,
        participation_type=participation_type,
        achievement=achievement,
        evaluation=evaluation
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)
    
    return participation





