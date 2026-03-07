"""
Notifications router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from app.models.notification import NotificationStatus

router = APIRouter()

@router.get("/")
def get_notifications(
    unread_only: bool = False,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get user notifications"""
    query = db.query(models.Notification).filter(models.Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(models.Notification.status != NotificationStatus.READ)
    
    notifications = query.order_by(models.Notification.created_at.desc()).limit(limit).all()
    return notifications

@router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Mark notification as read"""
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.status = NotificationStatus.READ
    notification.read_at = datetime.now()
    db.commit()
    
    return notification

@router.post("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Mark all notifications as read"""
    notifications = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.status != NotificationStatus.READ
    ).all()
    
    for notification in notifications:
        notification.status = NotificationStatus.READ
        notification.read_at = datetime.now()
    
    db.commit()
    return {"message": "All notifications marked as read", "count": len(notifications)}

@router.get("/unread/count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get count of unread notifications"""
    count = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.status != NotificationStatus.READ
    ).count()
    return {"unread_count": count}

