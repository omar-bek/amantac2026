"""
Teacher Student Evaluations Router
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

router = APIRouter(prefix="/teacher/evaluations", tags=["teacher-evaluations"])

def verify_teacher(current_user: models.User = Depends(get_current_user)):
    """Verify user is a teacher"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")
    return current_user

@router.post("/", response_model=teacher_schemas.StudentEvaluationResponse)
def create_evaluation(
    evaluation: teacher_schemas.StudentEvaluationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Create a new student evaluation (daily or monthly)"""
    db_evaluation = models.StudentEvaluation(
        student_id=evaluation.student_id,
        teacher_id=current_user.id,
        evaluation_type=evaluation.evaluation_type,
        evaluation_date=evaluation.evaluation_date,
        commitment_level=evaluation.commitment_level,
        interaction_level=evaluation.interaction_level,
        behavior_level=evaluation.behavior_level,
        participation_level=evaluation.participation_level,
        performance_trend=evaluation.performance_trend,
        interaction_trend=evaluation.interaction_trend,
        commitment_trend=evaluation.commitment_trend,
        educational_notes=evaluation.educational_notes,
        private_notes=evaluation.private_notes,
        shared_notes=evaluation.shared_notes
    )
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    
    # Create notification for parent (only shared notes)
    # TODO: Implement notification system
    
    return db_evaluation

@router.get("/", response_model=List[teacher_schemas.StudentEvaluationResponse])
def get_evaluations(
    student_id: Optional[int] = None,
    evaluation_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get evaluations created by current teacher"""
    query = db.query(models.StudentEvaluation).filter(
        models.StudentEvaluation.teacher_id == current_user.id
    )
    
    if student_id:
        query = query.filter(models.StudentEvaluation.student_id == student_id)
    if evaluation_type:
        query = query.filter(models.StudentEvaluation.evaluation_type == evaluation_type)
    
    evaluations = query.order_by(models.StudentEvaluation.evaluation_date.desc()).all()
    return evaluations

@router.get("/{evaluation_id}", response_model=teacher_schemas.StudentEvaluationResponse)
def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get evaluation by ID"""
    evaluation = db.query(models.StudentEvaluation).filter(
        models.StudentEvaluation.id == evaluation_id,
        models.StudentEvaluation.teacher_id == current_user.id
    ).first()
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return evaluation

@router.put("/{evaluation_id}", response_model=teacher_schemas.StudentEvaluationResponse)
def update_evaluation(
    evaluation_id: int,
    evaluation: teacher_schemas.StudentEvaluationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Update evaluation"""
    db_evaluation = db.query(models.StudentEvaluation).filter(
        models.StudentEvaluation.id == evaluation_id,
        models.StudentEvaluation.teacher_id == current_user.id
    ).first()
    
    if not db_evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    for key, value in evaluation.dict().items():
        if value is not None:
            setattr(db_evaluation, key, value)
    
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

@router.delete("/{evaluation_id}")
def delete_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Delete evaluation"""
    evaluation = db.query(models.StudentEvaluation).filter(
        models.StudentEvaluation.id == evaluation_id,
        models.StudentEvaluation.teacher_id == current_user.id
    ).first()
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    db.delete(evaluation)
    db.commit()
    return {"message": "Evaluation deleted successfully"}

@router.get("/student/{student_id}/history", response_model=List[teacher_schemas.StudentEvaluationResponse])
def get_student_evaluation_history(
    student_id: int,
    evaluation_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get evaluation history for a student"""
    query = db.query(models.StudentEvaluation).filter(
        models.StudentEvaluation.student_id == student_id,
        models.StudentEvaluation.teacher_id == current_user.id
    )
    
    if evaluation_type:
        query = query.filter(models.StudentEvaluation.evaluation_type == evaluation_type)
    
    evaluations = query.order_by(models.StudentEvaluation.evaluation_date.desc()).all()
    return evaluations

@router.get("/pending/count")
def get_pending_evaluations_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get count of students who need evaluation today"""
    # This is a simplified version - in reality, you'd check which students
    # haven't been evaluated today
    today = date.today()
    today_evaluations = db.query(models.StudentEvaluation).filter(
        models.StudentEvaluation.teacher_id == current_user.id,
        models.StudentEvaluation.evaluation_type == "daily",
        models.StudentEvaluation.evaluation_date >= datetime.combine(today, datetime.min.time()),
        models.StudentEvaluation.evaluation_date < datetime.combine(today, datetime.max.time())
    ).count()
    
    # Get teacher's classes and count students
    # TODO: Implement proper logic to count students who need evaluation
    return {"count": max(0, 10 - today_evaluations)}  # Placeholder

