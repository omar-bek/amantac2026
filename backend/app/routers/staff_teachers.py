"""
Staff Teacher Management Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta
from typing import List, Optional
from app.database import get_db
from app import models
from app.models.user import UserRole
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/staff/teachers", tags=["staff-teachers"])

def verify_staff(current_user: models.User = Depends(get_current_user)):
    """Verify user is staff or admin"""
    user_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if user_role not in ["staff", "admin"]:
        raise HTTPException(status_code=403, detail="Only staff and admin can access this endpoint")
    return current_user

class TeacherWorkload(BaseModel):
    teacher_id: int
    teacher_name: str
    teacher_email: str
    total_classes: int
    total_students: int
    assignments_count: int
    pending_evaluations: int
    messages_count: int
    activity_score: float  # Based on recent activity

class TeacherActivitySummary(BaseModel):
    teacher_id: int
    date: str
    assignments_created: int
    evaluations_done: int
    messages_sent: int
    activity_level: str  # high, medium, low

@router.get("/")
def get_all_teachers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get all teachers with basic info"""
    try:
        teachers = db.query(models.User).filter(
            models.User.role == UserRole.TEACHER
        ).all()
        
        result = []
        for teacher in teachers:
            # Get teacher's subjects from TeacherClass
            teacher_classes = db.query(models.TeacherClass).filter(
                models.TeacherClass.teacher_id == teacher.id
            ).all()
            
            # Get unique subjects (include both regular classes and TEMP_SPECIALIZATION entries)
            subjects = list(set([
                tc.subject for tc in teacher_classes 
                if tc.subject
            ]))
            specialization = ', '.join(subjects) if subjects else None
            
            result.append({
                "id": teacher.id,
                "full_name": teacher.full_name,
                "email": teacher.email,
                "phone": teacher.phone if hasattr(teacher, 'phone') and teacher.phone else None,
                "is_active": teacher.is_active if hasattr(teacher, 'is_active') else True,
                "specialization": specialization,
                "subjects": subjects,
                "created_at": teacher.created_at.isoformat() if teacher.created_at else None
            })
        
        return result
    except Exception as e:
        print(f"Error in get_all_teachers: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching teachers: {str(e)}")

@router.get("/workload", response_model=List[TeacherWorkload])
def get_teachers_workload(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get workload overview for all teachers"""
    teachers = db.query(models.User).filter(
        models.User.role == UserRole.TEACHER,
        models.User.is_active == True
    ).all()
    
    workload_data = []
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    for teacher in teachers:
        # Count classes
        total_classes = db.query(models.TeacherClass).filter(
            models.TeacherClass.teacher_id == teacher.id
        ).count()
        
        # Count students in teacher's classes
        teacher_classes = db.query(models.TeacherClass).filter(
            models.TeacherClass.teacher_id == teacher.id
        ).all()
        
        class_names = [tc.class_name for tc in teacher_classes]
        total_students = db.query(models.Student).filter(
            models.Student.is_active == True,
            models.Student.class_name.in_(class_names) if class_names else False
        ).count() if class_names else 0
        
        # Count assignments
        assignments_count = db.query(models.Assignment).filter(
            models.Assignment.teacher_id == teacher.id,
            models.Assignment.is_active == True
        ).count()
        
        # Count pending evaluations (students who need evaluation today)
        students_today = total_students
        today_evaluations = db.query(models.StudentEvaluation).filter(
            models.StudentEvaluation.teacher_id == teacher.id,
            models.StudentEvaluation.evaluation_type == "daily",
            func.date(models.StudentEvaluation.evaluation_date) == today
        ).count()
        pending_evaluations = max(0, students_today - today_evaluations)
        
        # Count unread messages
        messages_count = db.query(models.TeacherMessage).filter(
            models.TeacherMessage.teacher_id == teacher.id,
            models.TeacherMessage.is_from_teacher == False,
            models.TeacherMessage.status != "read"
        ).count()
        
        # Calculate activity score (based on last 7 days)
        week_assignments = db.query(models.Assignment).filter(
            models.Assignment.teacher_id == teacher.id,
            models.Assignment.created_at >= datetime.combine(week_ago, datetime.min.time())
        ).count()
        
        week_evaluations = db.query(models.StudentEvaluation).filter(
            models.StudentEvaluation.teacher_id == teacher.id,
            models.StudentEvaluation.created_at >= datetime.combine(week_ago, datetime.min.time())
        ).count()
        
        week_messages = db.query(models.TeacherMessage).filter(
            models.TeacherMessage.teacher_id == teacher.id,
            models.TeacherMessage.is_from_teacher == True,
            models.TeacherMessage.created_at >= datetime.combine(week_ago, datetime.min.time())
        ).count()
        
        # Activity score (0-100) based on actions per day
        activity_score = min(100, ((week_assignments + week_evaluations + week_messages) / 7) * 10)
        
        workload_data.append(TeacherWorkload(
            teacher_id=teacher.id,
            teacher_name=teacher.full_name,
            teacher_email=teacher.email,
            total_classes=total_classes,
            total_students=total_students,
            assignments_count=assignments_count,
            pending_evaluations=pending_evaluations,
            messages_count=messages_count,
            activity_score=round(activity_score, 1)
        ))
    
    return workload_data

@router.get("/{teacher_id}/activity", response_model=List[TeacherActivitySummary])
def get_teacher_activity_summary(
    teacher_id: int,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get daily activity summary for a teacher"""
    teacher = db.query(models.User).filter(
        models.User.id == teacher_id,
        models.User.role == UserRole.TEACHER
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    start_date = date.today() - timedelta(days=days)
    activity_data = []
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        date_start = datetime.combine(current_date, datetime.min.time())
        date_end = datetime.combine(current_date, datetime.max.time())
        
        assignments_created = db.query(models.Assignment).filter(
            models.Assignment.teacher_id == teacher_id,
            models.Assignment.created_at >= date_start,
            models.Assignment.created_at <= date_end
        ).count()
        
        evaluations_done = db.query(models.StudentEvaluation).filter(
            models.StudentEvaluation.teacher_id == teacher_id,
            models.StudentEvaluation.created_at >= date_start,
            models.StudentEvaluation.created_at <= date_end
        ).count()
        
        messages_sent = db.query(models.TeacherMessage).filter(
            models.TeacherMessage.teacher_id == teacher_id,
            models.TeacherMessage.is_from_teacher == True,
            models.TeacherMessage.created_at >= date_start,
            models.TeacherMessage.created_at <= date_end
        ).count()
        
        total_actions = assignments_created + evaluations_done + messages_sent
        activity_level = "high" if total_actions >= 10 else "medium" if total_actions >= 5 else "low"
        
        activity_data.append(TeacherActivitySummary(
            teacher_id=teacher_id,
            date=current_date.isoformat(),
            assignments_created=assignments_created,
            evaluations_done=evaluations_done,
            messages_sent=messages_sent,
            activity_level=activity_level
        ))
    
    return activity_data

@router.post("/{teacher_id}/specialization")
def add_teacher_specialization(
    teacher_id: int,
    specialization: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Add specialization to a teacher by creating a TeacherClass entry"""
    teacher = db.query(models.User).filter(
        models.User.id == teacher_id,
        models.User.role == UserRole.TEACHER
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Parse specialization (comma-separated subjects)
    subjects = [s.strip() for s in specialization.split(',') if s.strip()]
    
    if not subjects:
        raise HTTPException(status_code=400, detail="التخصص مطلوب")
    
    # Create TeacherClass entries for each subject (without specific class/grade)
    # This is just to store the specialization
    created_classes = []
    for subject in subjects:
        # Check if already exists
        existing = db.query(models.TeacherClass).filter(
            models.TeacherClass.teacher_id == teacher_id,
            models.TeacherClass.subject == subject,
            models.TeacherClass.class_name == "TEMP_SPECIALIZATION"
        ).first()
        
        if not existing:
            teacher_class = models.TeacherClass(
                teacher_id=teacher_id,
                class_name="TEMP_SPECIALIZATION",  # Temporary placeholder
                grade="N/A",  # Temporary placeholder
                subject=subject
            )
            db.add(teacher_class)
            created_classes.append(teacher_class)
    
    db.commit()
    
    return {
        "message": "تم إضافة التخصص بنجاح",
        "subjects": subjects
    }

@router.get("/{teacher_id}")
def get_teacher_detail(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get detailed information about a teacher"""
    teacher = db.query(models.User).filter(
        models.User.id == teacher_id,
        models.User.role == UserRole.TEACHER
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Get teacher's classes
    classes = db.query(models.TeacherClass).filter(
        models.TeacherClass.teacher_id == teacher_id
    ).all()
    
    # Get unique subjects
    subjects = list(set([tc.subject for tc in classes if tc.subject]))
    specialization = ', '.join(subjects) if subjects else None
    
    # Get classes with student counts
    classes_with_students = []
    for tc in classes:
        student_count = db.query(models.Student).filter(
            models.Student.class_name == tc.class_name,
            models.Student.grade == tc.grade,
            models.Student.is_active == True
        ).count()
        
        classes_with_students.append({
            "id": tc.id,
            "class_name": tc.class_name,
            "grade": tc.grade,
            "subject": tc.subject,
            "student_count": student_count
        })
    
    # Get statistics
    total_students = sum([c["student_count"] for c in classes_with_students])
    assignments_count = db.query(models.Assignment).filter(
        models.Assignment.teacher_id == teacher_id,
        models.Assignment.is_active == True
    ).count()
    
    return {
        "id": teacher.id,
        "full_name": teacher.full_name,
        "email": teacher.email,
        "phone": teacher.phone if hasattr(teacher, 'phone') and teacher.phone else None,
        "is_active": teacher.is_active if hasattr(teacher, 'is_active') else True,
        "specialization": specialization,
        "subjects": subjects,
        "classes": classes_with_students,
        "total_students": total_students,
        "assignments_count": assignments_count,
        "created_at": teacher.created_at.isoformat() if teacher.created_at else None
    }

@router.get("/{teacher_id}/classes")
def get_teacher_classes(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_staff)
):
    """Get classes assigned to a teacher"""
    teacher = db.query(models.User).filter(
        models.User.id == teacher_id,
        models.User.role == UserRole.TEACHER
    ).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    classes = db.query(models.TeacherClass).filter(
        models.TeacherClass.teacher_id == teacher_id
    ).all()
    
    classes_with_students = []
    for tc in classes:
        student_count = db.query(models.Student).filter(
            models.Student.class_name == tc.class_name,
            models.Student.grade == tc.grade,
            models.Student.is_active == True
        ).count()
        
        classes_with_students.append({
            "id": tc.id,
            "class_name": tc.class_name,
            "grade": tc.grade,
            "subject": tc.subject,
            "student_count": student_count
        })
    
    return classes_with_students

