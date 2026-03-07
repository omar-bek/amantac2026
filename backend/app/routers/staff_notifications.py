"""
Staff Notifications Management Router
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from datetime import datetime, date, time, timedelta
from typing import List, Optional
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/staff/notifications", tags=["staff-notifications"])

def verify_staff(current_user: models.User = Depends(get_current_user)):
    """Verify user is staff"""
    if current_user.role.value not in ["staff", "admin"]:
        raise HTTPException(status_code=403, detail="Only staff can access this endpoint")
    return current_user

class NotificationCreate(BaseModel):
    title: str
    message: str
    target_role: Optional[str] = None  # parent, teacher, driver, student, all
    target_user_id: Optional[int] = None
    target_class: Optional[str] = None
    priority: str = "normal"  # low, normal, high, urgent
    send_immediately: bool = True

class NotificationTemplate(BaseModel):
    id: int
    name: str
    title_template: str
    message_template: str
    target_role: str
    created_at: str

class QuietHoursConfig(BaseModel):
    enabled: bool
    start_time: str  # HH:mm format
    end_time: str    # HH:mm format
    days_of_week: List[int]  # 0-6 (Monday-Sunday)

@router.post("/broadcast")
def create_broadcast_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Create and send a broadcast notification"""
    # Create notification record
    notification_record = models.Notification(
        title=notification.title,
        message=notification.message,
        target_role=notification.target_role,
        target_user_id=notification.target_user_id,
        priority=notification.priority,
        created_by=current_user.id,
        created_at=datetime.now()
    )
    
    db.add(notification_record)
    db.commit()
    db.refresh(notification_record)
    
    # If send_immediately, mark as sent
    if notification.send_immediately:
        notification_record.sent_at = datetime.now()
        db.commit()
    
    return {
        "id": notification_record.id,
        "message": "Notification created successfully",
        "notification": notification_record
    }

@router.get("/history")
def get_notification_history(
    target_role: Optional[str] = None,
    limit: int = 50,
    skip: int = 0,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get notification history"""
    query = db.query(models.Notification).order_by(models.Notification.created_at.desc())
    
    if target_role:
        query = query.filter(models.Notification.target_role == target_role)
    
    notifications = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": notif.id,
            "title": notif.title,
            "message": notif.message,
            "target_role": notif.target_role,
            "priority": notif.priority,
            "created_at": notif.created_at.isoformat() if notif.created_at else None,
            "sent_at": notif.sent_at.isoformat() if notif.sent_at else None,
            "created_by": notif.created_by,
            "read_count": 0  # Can be enhanced with actual read tracking
        }
        for notif in notifications
    ]

@router.get("/templates")
def get_notification_templates(
    target_role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get notification templates (can be extended with actual Template model)"""
    # Placeholder templates - can be enhanced with a Template model
    templates = [
        {
            "id": 1,
            "name": "إشعار عام للآباء",
            "title_template": "إشعار عام",
            "message_template": "نود إبلاغكم بأن: {message}",
            "target_role": "parent",
            "created_at": datetime.now().isoformat()
        },
        {
            "id": 2,
            "name": "إشعار للمدرسين",
            "title_template": "إشعار للمدرسين",
            "message_template": "نود إبلاغكم: {message}",
            "target_role": "teacher",
            "created_at": datetime.now().isoformat()
        },
        {
            "id": 3,
            "name": "تذكير مهم",
            "title_template": "تذكير: {title}",
            "message_template": "نود تذكيركم: {message}",
            "target_role": "all",
            "created_at": datetime.now().isoformat()
        }
    ]
    
    if target_role:
        templates = [t for t in templates if t["target_role"] == target_role or t["target_role"] == "all"]
    
    return templates

@router.post("/templates")
def create_notification_template(
    template: NotificationTemplate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Create a notification template (placeholder - can be enhanced with Template model)"""
    # For now, return success message
    # In production, this would save to a Template table
    return {
        "message": "Template created successfully (placeholder)",
        "template_id": 1
    }

@router.get("/quiet-hours")
def get_quiet_hours_config(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get quiet hours configuration"""
    # Placeholder - can be enhanced with a Settings model
    return {
        "enabled": False,
        "start_time": "22:00",
        "end_time": "07:00",
        "days_of_week": [5, 6]  # Friday, Saturday
    }

@router.post("/quiet-hours")
def update_quiet_hours_config(
    config: QuietHoursConfig,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Update quiet hours configuration"""
    # Placeholder - can be enhanced with a Settings model
    return {
        "message": "Quiet hours configuration updated successfully",
        "config": config
    }

@router.get("/stats")
def get_notification_stats(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get notification statistics"""
    start_date = datetime.now() - timedelta(days=days)
    
    total_sent = db.query(models.Notification).filter(
        models.Notification.created_at >= start_date,
        models.Notification.sent_at.isnot(None)
    ).count()
    
    by_role = {}
    for role in ["parent", "teacher", "driver", "student", "all"]:
        count = db.query(models.Notification).filter(
            models.Notification.target_role == role,
            models.Notification.created_at >= start_date
        ).count()
        by_role[role] = count
    
    return {
        "total_sent": total_sent,
        "by_role": by_role,
        "period_days": days
    }

