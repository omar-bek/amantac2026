"""
Admin Classes Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from app.models.user import UserRole
from pydantic import BaseModel

router = APIRouter(prefix="/admin/classes", tags=["admin-classes"])

def verify_admin(current_user: models.User = Depends(get_current_user)):
    """Verify user is admin"""
    user_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if user_role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Only admin can access this endpoint")
    return current_user

@router.get("/")
def get_all_classes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_admin)
):
    """Get all classes with statistics"""
    try:
        # Get unique classes from students
        unique_classes = db.query(
            models.Student.class_name,
            models.Student.grade,
            func.count(models.Student.id).label('student_count')
        ).filter(
            models.Student.is_active == True,
            models.Student.class_name.isnot(None),
            models.Student.grade.isnot(None)
        ).group_by(
            models.Student.class_name,
            models.Student.grade
        ).all()
        
        result = []
        for class_name, grade, student_count in unique_classes:
            # Get teacher for this class from TeacherClass
            teacher_class = db.query(models.TeacherClass).filter(
                models.TeacherClass.class_name == class_name,
                models.TeacherClass.grade == grade
            ).first()
            
            teacher_name = None
            teacher_id = None
            subject = None
            if teacher_class:
                teacher = db.query(models.User).filter(
                    models.User.id == teacher_class.teacher_id
                ).first()
                if teacher:
                    teacher_name = teacher.full_name
                    teacher_id = teacher.id
                subject = teacher_class.subject
            
            result.append({
                "id": f"{class_name}_{grade}",  # Composite ID
                "class_name": class_name,
                "grade": grade,
                "student_count": student_count,
                "teacher_name": teacher_name,
                "teacher_id": teacher_id,
                "subject": subject
            })
        
        return result
    except Exception as e:
        print(f"Error in get_all_classes: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching classes: {str(e)}")


