"""
Teacher Announcements Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app import models
from app.models.teacher import AnnouncementPriority
from app.routers.auth import get_current_user

router = APIRouter(prefix="/teacher/announcements", tags=["teacher-announcements"])

class AnnouncementCreate(BaseModel):
    title: str
    message: str
    target_class: Optional[str] = None
    priority: str = "normal"
    send_notification: bool = False

def verify_teacher(current_user: models.User = Depends(get_current_user)):
    """Verify user is a teacher"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")
    return current_user

@router.post("/", response_model=dict)
def create_announcement(
    announcement_data: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Create a new announcement"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Creating announcement for teacher {current_user.id}: {announcement_data.title}")
        
        # Convert priority string to enum
        priority_enum = AnnouncementPriority.NORMAL
        if announcement_data.priority == "high":
            priority_enum = AnnouncementPriority.HIGH
        elif announcement_data.priority == "low":
            priority_enum = AnnouncementPriority.LOW

        # Handle empty string for target_class
        target_class_value = announcement_data.target_class if announcement_data.target_class and announcement_data.target_class.strip() else None
        
        db_announcement = models.TeacherAnnouncement(
            teacher_id=current_user.id,
            title=announcement_data.title,
            message=announcement_data.message,
            target_class=target_class_value,
            priority=priority_enum,
            send_notification=announcement_data.send_notification
        )
        db.add(db_announcement)
        db.commit()
        db.refresh(db_announcement)

        logger.info(f"Announcement created successfully with ID: {db_announcement.id}")

        # If notification is requested, create notifications for students/parents
        if announcement_data.send_notification:
            # TODO: Implement notification creation logic
            logger.info("Notification requested but not yet implemented")

        return {
            "id": db_announcement.id,
            "title": db_announcement.title,
            "message": db_announcement.message,
            "target_class": db_announcement.target_class,
            "priority": db_announcement.priority.value,
            "send_notification": db_announcement.send_notification,
            "views_count": db_announcement.views_count,
            "created_at": db_announcement.created_at.isoformat() if db_announcement.created_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        error_msg = f"Failed to create announcement: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/", response_model=List[dict])
def get_announcements(
    target_class: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get announcements created by current teacher"""
    query = db.query(models.TeacherAnnouncement).filter(
        models.TeacherAnnouncement.teacher_id == current_user.id
    )

    if target_class:
        query = query.filter(
            (models.TeacherAnnouncement.target_class == target_class) |
            (models.TeacherAnnouncement.target_class == None) |
            (models.TeacherAnnouncement.target_class == "all")
        )

    announcements = query.order_by(models.TeacherAnnouncement.created_at.desc()).all()

    return [
        {
            "id": ann.id,
            "title": ann.title,
            "message": ann.message,
            "target_class": ann.target_class,
            "priority": ann.priority.value,
            "send_notification": ann.send_notification,
            "views_count": ann.views_count,
            "created_at": ann.created_at.isoformat() if ann.created_at else None
        }
        for ann in announcements
    ]

@router.get("/{announcement_id}", response_model=dict)
def get_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get announcement by ID"""
    announcement = db.query(models.TeacherAnnouncement).filter(
        models.TeacherAnnouncement.id == announcement_id,
        models.TeacherAnnouncement.teacher_id == current_user.id
    ).first()

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    # Increment views count
    announcement.views_count += 1
    db.commit()

    return {
        "id": announcement.id,
        "title": announcement.title,
        "message": announcement.message,
        "target_class": announcement.target_class,
        "priority": announcement.priority.value,
        "send_notification": announcement.send_notification,
        "views_count": announcement.views_count,
        "created_at": announcement.created_at.isoformat() if announcement.created_at else None
    }

@router.put("/{announcement_id}", response_model=dict)
def update_announcement(
    announcement_id: int,
    title: Optional[str] = None,
    message: Optional[str] = None,
    target_class: Optional[str] = None,
    priority: Optional[str] = None,
    send_notification: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Update announcement"""
    announcement = db.query(models.TeacherAnnouncement).filter(
        models.TeacherAnnouncement.id == announcement_id,
        models.TeacherAnnouncement.teacher_id == current_user.id
    ).first()

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if title is not None:
        announcement.title = title
    if message is not None:
        announcement.message = message
    if target_class is not None:
        announcement.target_class = target_class
    if priority:
        if priority == "high":
            announcement.priority = AnnouncementPriority.HIGH
        elif priority == "low":
            announcement.priority = AnnouncementPriority.LOW
        else:
            announcement.priority = AnnouncementPriority.NORMAL
    if send_notification is not None:
        announcement.send_notification = send_notification

    db.commit()
    db.refresh(announcement)

    return {
        "id": announcement.id,
        "title": announcement.title,
        "message": announcement.message,
        "target_class": announcement.target_class,
        "priority": announcement.priority.value,
        "send_notification": announcement.send_notification,
        "views_count": announcement.views_count,
        "created_at": announcement.created_at.isoformat() if announcement.created_at else None
    }

@router.delete("/{announcement_id}")
def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Delete announcement"""
    announcement = db.query(models.TeacherAnnouncement).filter(
        models.TeacherAnnouncement.id == announcement_id,
        models.TeacherAnnouncement.teacher_id == current_user.id
    ).first()

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    db.delete(announcement)
    db.commit()
    return {"message": "Announcement deleted successfully"}

