"""
Teacher Exams Router
"""

from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
from pathlib import Path
from app.database import get_db
from app import models
from app.models.academic import ExamType
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/teacher/exams", tags=["teacher-exams"])

# Create uploads directory if it doesn't exist
# Use absolute path based on backend directory
BACKEND_DIR = Path(__file__).parent.parent.parent
UPLOAD_DIR = BACKEND_DIR / "uploads" / "exams"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class ExamCreate(BaseModel):
    exam_name: str
    subject: str
    exam_type: str  # 'quiz', 'midterm', 'final'
    class_name: Optional[str] = None
    exam_date: Optional[str] = None
    duration_minutes: int = 60
    max_grade: float = 100.0
    description: Optional[str] = None

def verify_teacher(current_user: models.User = Depends(get_current_user)):
    """Verify user is a teacher"""
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")
    return current_user

@router.post("/")
async def create_exam(
    exam_name: str = Form(...),
    subject: str = Form(...),
    exam_type: str = Form(...),
    class_name: Optional[str] = Form(default=None),
    exam_date: Optional[str] = Form(default=None),
    duration_minutes: int = Form(default=60),
    max_grade: float = Form(default=100.0),
    description: Optional[str] = Form(default=None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Create a new exam/quiz with optional PDF file"""
    try:
        # Convert string inputs to proper types (FormData sends everything as strings)
        try:
            duration_minutes = int(duration_minutes) if duration_minutes else 60
        except (ValueError, TypeError):
            duration_minutes = 60
        
        try:
            max_grade = float(max_grade) if max_grade else 100.0
        except (ValueError, TypeError):
            max_grade = 100.0
        
        if exam_type not in ['quiz', 'midterm', 'final']:
            raise HTTPException(status_code=400, detail="Invalid exam_type. Must be 'quiz', 'midterm', or 'final'")
    
        # Convert exam_type string to ExamType enum
        exam_type_enum = None
        for et in ExamType:
            if et.value == exam_type:
                exam_type_enum = et
                break
        
        if not exam_type_enum:
            raise HTTPException(status_code=400, detail="Invalid exam_type")
        
        # Parse exam_date if provided
        exam_date_obj = datetime.now()
        if exam_date:
            try:
                # Handle ISO format strings
                exam_date_str = exam_date.replace('Z', '+00:00')
                exam_date_obj = datetime.fromisoformat(exam_date_str)
            except Exception as e:
                # If parsing fails, use current time
                exam_date_obj = datetime.now()
        
        # Handle file upload
        file_path = None
        if file and file.filename:
            # Validate file type (only PDF)
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
            # Generate unique filename
            file_extension = Path(file.filename).suffix
            unique_filename = f"{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
            file_path = str(UPLOAD_DIR / unique_filename)
            
            # Save file
            try:
                with open(file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        # Create Exam record
        db_exam = models.Exam(
            exam_name=exam_name,
            subject=subject,
            exam_type=exam_type_enum,
            class_name=class_name,
            exam_date=exam_date_obj,
            duration=duration_minutes,
            max_grade=max_grade,
            description=description,
            file_path=file_path,
            teacher_id=current_user.id
        )
        db.add(db_exam)
        db.commit()
        db.refresh(db_exam)
        
        # Convert enum to string for JSON response
        response = {
            "id": db_exam.id,
            "exam_name": db_exam.exam_name,
            "subject": db_exam.subject,
            "exam_type": db_exam.exam_type.value,
            "class_name": db_exam.class_name,
            "exam_date": db_exam.exam_date.isoformat() if db_exam.exam_date else None,
            "duration_minutes": db_exam.duration or 60,
            "max_grade": db_exam.max_grade,
            "description": db_exam.description,
            "file_path": db_exam.file_path,
        }
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error creating exam: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)  # Log to console for debugging
        raise HTTPException(status_code=500, detail=f"Failed to create exam: {str(e)}")

@router.get("/")
def get_exams(
    class_name: Optional[str] = None,
    exam_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get exams created by current teacher"""
    query = db.query(models.Exam).filter(
        models.Exam.teacher_id == current_user.id
    )
    
    if class_name:
        query = query.filter(models.Exam.class_name == class_name)
    if exam_type:
        query = query.filter(models.Exam.exam_type == exam_type)
    
    exams = query.order_by(models.Exam.exam_date.desc()).all()
    
    # Convert to dict with string enum values
    result = []
    for exam in exams:
        result.append({
            "id": exam.id,
            "exam_name": exam.exam_name,
            "subject": exam.subject,
            "exam_type": exam.exam_type.value,
            "class_name": exam.class_name,
            "exam_date": exam.exam_date.isoformat() if exam.exam_date else None,
            "duration_minutes": exam.duration or 60,
            "max_grade": exam.max_grade,
            "description": exam.description,
            "file_path": exam.file_path,
        })
    
    return result

@router.get("/{exam_id}")
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Get exam by ID"""
    exam = db.query(models.Exam).filter(
        models.Exam.id == exam_id,
        models.Exam.teacher_id == current_user.id
    ).first()
    
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    return {
        "id": exam.id,
        "exam_name": exam.exam_name,
        "subject": exam.subject,
        "exam_type": exam.exam_type.value,
        "class_name": exam.class_name,
        "exam_date": exam.exam_date.isoformat() if exam.exam_date else None,
        "duration_minutes": exam.duration or 60,
        "max_grade": exam.max_grade,
        "description": exam.description,
        "file_path": exam.file_path,
    }

@router.put("/{exam_id}")
async def update_exam(
    exam_id: int,
    exam_name: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    exam_type: Optional[str] = Form(None),
    class_name: Optional[str] = Form(None),
    exam_date: Optional[str] = Form(None),
    duration_minutes: Optional[int] = Form(None),
    max_grade: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Update exam"""
    db_exam = db.query(models.Exam).filter(
        models.Exam.id == exam_id,
        models.Exam.teacher_id == current_user.id
    ).first()
    
    if not db_exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    if exam_name is not None:
        db_exam.exam_name = exam_name
    if subject is not None:
        db_exam.subject = subject
    
    # Convert exam_type to enum
    if exam_type:
        exam_type_enum = None
        for et in ExamType:
            if et.value == exam_type:
                exam_type_enum = et
                break
        if exam_type_enum:
            db_exam.exam_type = exam_type_enum
    
    if class_name is not None:
        db_exam.class_name = class_name
    
    if exam_date:
        try:
            exam_date_str = exam_date.replace('Z', '+00:00')
            db_exam.exam_date = datetime.fromisoformat(exam_date_str)
        except:
            pass
    
    if duration_minutes is not None:
        db_exam.duration = duration_minutes
    if max_grade is not None:
        db_exam.max_grade = max_grade
    if description is not None:
        db_exam.description = description
    
    # Handle file upload
    if file and file.filename:
        # Validate file type (only PDF)
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Delete old file if exists
        if db_exam.file_path and os.path.exists(db_exam.file_path):
            try:
                os.remove(db_exam.file_path)
            except:
                pass
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
        file_path = str(UPLOAD_DIR / unique_filename)
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            db_exam.file_path = file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    db.commit()
    db.refresh(db_exam)
    
    return {
        "id": db_exam.id,
        "exam_name": db_exam.exam_name,
        "subject": db_exam.subject,
        "exam_type": db_exam.exam_type.value,
        "class_name": db_exam.class_name,
        "exam_date": db_exam.exam_date.isoformat() if db_exam.exam_date else None,
        "duration_minutes": db_exam.duration or 60,
        "max_grade": db_exam.max_grade,
        "description": db_exam.description,
        "file_path": db_exam.file_path,
    }

@router.delete("/{exam_id}")
def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Delete exam"""
    exam = db.query(models.Exam).filter(
        models.Exam.id == exam_id,
        models.Exam.teacher_id == current_user.id
    ).first()
    
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Delete file if exists
    if exam.file_path and os.path.exists(exam.file_path):
        try:
            os.remove(exam.file_path)
        except:
            pass
    
    db.delete(exam)
    db.commit()
    return {"message": "Exam deleted successfully"}

@router.get("/{exam_id}/download")
def download_exam_file(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_teacher)
):
    """Download exam PDF file"""
    from fastapi.responses import FileResponse
    
    exam = db.query(models.Exam).filter(
        models.Exam.id == exam_id,
        models.Exam.teacher_id == current_user.id
    ).first()
    
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    if not exam.file_path or not os.path.exists(exam.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        exam.file_path,
        media_type="application/pdf",
        filename=f"{exam.exam_name}.pdf"
    )
