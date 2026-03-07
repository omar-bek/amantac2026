"""
Teacher Dashboard Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.database import get_db
from app import models
from app import schemas
from app.schemas import teacher as teacher_schemas
from app.routers.auth import get_current_user

router = APIRouter(prefix="/teacher/dashboard", tags=["teacher-dashboard"])

def verify_teacher(current_user: models.User = Depends(get_current_user)):
    """Verify user is a teacher"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")
    return current_user

@router.get("/stats", response_model=teacher_schemas.TeacherDashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get teacher dashboard statistics"""
    today = date.today()
    
    # Get teacher's classes
    teacher_classes = db.query(models.TeacherClass).filter(
        models.TeacherClass.teacher_id == current_user.id,
        models.TeacherClass.is_active == True
    ).all()
    
    class_names = [tc.class_name for tc in teacher_classes]
    grades = [tc.grade for tc in teacher_classes]
    
    # Count students today (students in teacher's classes)
    students_today = db.query(models.Student).filter(
        models.Student.is_active == True,
        models.Student.class_name.in_(class_names) if class_names else True
    ).count()
    
    # Count assignments due today
    assignments_today = db.query(models.Assignment).filter(
        models.Assignment.teacher_id == current_user.id,
        models.Assignment.is_active == True,
        models.Assignment.due_date >= datetime.combine(today, datetime.min.time()),
        models.Assignment.due_date < datetime.combine(today, datetime.max.time())
    ).count()
    
    # Count pending evaluations (students who need evaluation today)
    today_evaluations = db.query(models.StudentEvaluation).filter(
        models.StudentEvaluation.teacher_id == current_user.id,
        models.StudentEvaluation.evaluation_type == "daily",
        models.StudentEvaluation.evaluation_date >= datetime.combine(today, datetime.min.time()),
        models.StudentEvaluation.evaluation_date < datetime.combine(today, datetime.max.time())
    ).count()
    
    pending_evaluations = max(0, students_today - today_evaluations)
    
    # Count unread messages
    unread_messages = db.query(models.TeacherMessage).filter(
        models.TeacherMessage.teacher_id == current_user.id,
        models.TeacherMessage.is_from_teacher == False,
        models.TeacherMessage.status != "read"
    ).count()
    
    return teacher_schemas.TeacherDashboardStats(
        students_today=students_today,
        assignments_today=assignments_today,
        pending_evaluations=pending_evaluations,
        unread_messages=unread_messages
    )

@router.get("/classes")
def get_teacher_classes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get teacher's classes"""
    classes = db.query(models.TeacherClass).filter(
        models.TeacherClass.teacher_id == current_user.id,
        models.TeacherClass.is_active == True
    ).all()
    
    return classes

@router.post("/classes", response_model=teacher_schemas.TeacherClassResponse)
def create_teacher_class(
    class_data: teacher_schemas.TeacherClassCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Create a new teacher class association"""
    db_class = models.TeacherClass(
        teacher_id=current_user.id,
        class_name=class_data.class_name,
        subject=class_data.subject,
        grade=class_data.grade,
        academic_year=class_data.academic_year,
        is_active=True
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

