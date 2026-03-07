"""
Teacher Assignments Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from app.database import get_db
from app import models
from app import schemas
from app.schemas import teacher as teacher_schemas
from app.routers.auth import get_current_user

router = APIRouter(prefix="/teacher/assignments", tags=["teacher-assignments"])

def verify_teacher(current_user: models.User = Depends(get_current_user)):
    """Verify user is a teacher"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")
    return current_user

@router.post("/", response_model=teacher_schemas.AssignmentResponse)
def create_assignment(
    assignment: teacher_schemas.AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Create a new assignment"""
    db_assignment = models.Assignment(
        assignment_name=assignment.assignment_name,
        subject=assignment.subject,
        description=assignment.description,
        due_date=assignment.due_date,
        max_grade=assignment.max_grade,
        class_name=assignment.class_name,
        grade=assignment.grade,
        academic_year=assignment.academic_year,
        teacher_id=current_user.id,
        assignment_type=assignment.assignment_type,
        file_path=assignment.file_path,
        is_active=True
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    
    # Create notification for parents
    # TODO: Implement notification system
    
    return db_assignment

@router.get("/", response_model=List[teacher_schemas.AssignmentResponse])
def get_assignments(
    class_name: Optional[str] = None,
    grade: Optional[str] = None,
    subject: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get assignments created by current teacher"""
    query = db.query(models.Assignment).filter(
        models.Assignment.teacher_id == current_user.id,
        models.Assignment.is_active == True
    )
    
    if class_name:
        query = query.filter(models.Assignment.class_name == class_name)
    if grade:
        query = query.filter(models.Assignment.grade == grade)
    if subject:
        query = query.filter(models.Assignment.subject == subject)
    
    assignments = query.order_by(models.Assignment.due_date.desc()).all()
    return assignments

@router.get("/{assignment_id}", response_model=teacher_schemas.AssignmentResponse)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get assignment by ID"""
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id,
        models.Assignment.teacher_id == current_user.id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return assignment

@router.put("/{assignment_id}", response_model=teacher_schemas.AssignmentResponse)
def update_assignment(
    assignment_id: int,
    assignment: teacher_schemas.AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Update assignment"""
    db_assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id,
        models.Assignment.teacher_id == current_user.id
    ).first()
    
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    for key, value in assignment.dict().items():
        setattr(db_assignment, key, value)
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Delete assignment (soft delete)"""
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id,
        models.Assignment.teacher_id == current_user.id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    assignment.is_active = False
    db.commit()
    return {"message": "Assignment deleted successfully"}

@router.get("/{assignment_id}/submissions", response_model=List[teacher_schemas.AssignmentSubmissionResponse])
def get_assignment_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get all submissions for an assignment"""
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id,
        models.Assignment.teacher_id == current_user.id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    submissions = db.query(models.AssignmentSubmission).filter(
        models.AssignmentSubmission.assignment_id == assignment_id
    ).all()
    
    return submissions

@router.put("/submissions/{submission_id}", response_model=teacher_schemas.AssignmentSubmissionResponse)
def grade_submission(
    submission_id: int,
    submission_update: teacher_schemas.AssignmentSubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Grade and comment on a submission"""
    submission = db.query(models.AssignmentSubmission).filter(
        models.AssignmentSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Verify teacher owns the assignment
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == submission.assignment_id,
        models.Assignment.teacher_id == current_user.id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=403, detail="You don't have permission to grade this submission")
    
    if submission_update.teacher_comment:
        submission.teacher_comment = submission_update.teacher_comment
    if submission_update.grade is not None:
        submission.grade = submission_update.grade
    if submission_update.submission_status:
        submission.submission_status = submission_update.submission_status
    
    db.commit()
    db.refresh(submission)
    return submission

@router.get("/today/count")
def get_today_assignments_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get count of assignments due today"""
    today = date.today()
    count = db.query(models.Assignment).filter(
        models.Assignment.teacher_id == current_user.id,
        models.Assignment.is_active == True,
        models.Assignment.due_date >= datetime.combine(today, datetime.min.time()),
        models.Assignment.due_date < datetime.combine(today, datetime.max.time())
    ).count()
    
    return {"count": count}

