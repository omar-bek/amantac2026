"""
AI Insights Router
Provides AI-driven insights while maintaining ethical guidelines
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai-insights"])

class ParentGuidanceSuggestion(BaseModel):
    suggestion: str
    category: str
    priority: str
    context: Optional[dict] = None

class WorkloadReductionTip(BaseModel):
    tip: str
    category: str
    estimated_time_saved: str

class AnomalyDetection(BaseModel):
    type: str
    description: str
    severity: str
    recommendation: str
    is_alarm: bool = False  # Always False - non-alarm only

class SmartSummary(BaseModel):
    summary: str
    key_points: List[str]
    period: str

@router.get("/parent-guidance/{student_id}")
def get_parent_guidance_suggestions(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get AI-driven guidance suggestions for parents
    Ethical: Supportive, non-diagnostic, no student comparison
    """
    # Verify parent has access to this student
    if current_user.role.value != "parent":
        raise HTTPException(status_code=403, detail="Only parents can access this")
    
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.parent_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get recent data (attendance, grades, behavior)
    recent_attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id
    ).order_by(models.Attendance.date.desc()).limit(30).all()
    
    attendance_rate = len([a for a in recent_attendance if a.status.value == "PRESENT"]) / max(len(recent_attendance), 1) * 100
    
    suggestions = []
    
    # Generate supportive suggestions based on data
    if attendance_rate < 80:
        suggestions.append(ParentGuidanceSuggestion(
            suggestion="نلاحظ أن معدل الحضور يحتاج تحسين. يمكنك التواصل مع المدرسة لمناقشة طرق دعم الحضور المنتظم.",
            category="attendance",
            priority="medium",
            context={"attendance_rate": attendance_rate}
        ))
    
    # Always supportive, never diagnostic
    suggestions.append(ParentGuidanceSuggestion(
        suggestion="ننصح بمتابعة التواصل مع المدرسة للحصول على تحديثات منتظمة عن تقدم الطالب.",
        category="communication",
        priority="low"
    ))
    
    return {"suggestions": suggestions}

@router.get("/teacher/workload-reduction")
def get_workload_reduction_tips(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get tips to reduce teacher workload
    Ethical: Efficiency-focused, no student evaluation
    """
    if current_user.role.value != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this")
    
    tips = [
        WorkloadReductionTip(
            tip="استخدم قوالب التعليقات الجاهزة لتوفير الوقت في التقييمات اليومية",
            category="evaluation",
            estimated_time_saved="5-10 دقائق يومياً"
        ),
        WorkloadReductionTip(
            tip="قم بجدولة الإعلانات مسبقاً لتوفير الوقت",
            category="announcements",
            estimated_time_saved="3-5 دقائق لكل إعلان"
        ),
        WorkloadReductionTip(
            tip="استخدم نظام التقييم السريع (Quick Tags) لتسريع عملية التقييم",
            category="evaluation",
            estimated_time_saved="2-3 دقائق لكل طالب"
        ),
    ]
    
    return {"tips": tips}

@router.get("/anomaly-detection")
def detect_anomalies(
    student_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Detect anomalies in data (non-alarm)
    Ethical: No diagnosis, no classification, supportive only
    """
    anomalies = []
    
    if student_id:
        # Check attendance patterns
        recent_attendance = db.query(models.Attendance).filter(
            models.Attendance.student_id == student_id
        ).order_by(models.Attendance.date.desc()).limit(10).all()
        
        if len(recent_attendance) > 0:
            absent_count = len([a for a in recent_attendance if a.status.value == "ABSENT"])
            if absent_count > 5:
                anomalies.append(AnomalyDetection(
                    type="attendance_pattern",
                    description="تم ملاحظة نمط غياب متكرر مؤخراً",
                    severity="low",
                    recommendation="ننصح بمتابعة التواصل مع ولي الأمر لفهم الأسباب",
                    is_alarm=False
                ))
    
    return {"anomalies": anomalies, "note": "جميع التنبيهات غير تنبيهية - للمتابعة فقط"}

@router.get("/smart-summary/{student_id}")
def get_smart_summary(
    student_id: int,
    period: str = "month",  # week, month, semester
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Generate smart summary for student
    Ethical: Supportive, no comparison, no classification
    """
    # Verify access
    if current_user.role.value == "parent":
        student = db.query(models.Student).filter(
            models.Student.id == student_id,
            models.Student.parent_id == current_user.id
        ).first()
    elif current_user.role.value == "teacher":
        student = db.query(models.Student).filter(
            models.Student.id == student_id
        ).first()
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Calculate period dates
    end_date = datetime.now()
    if period == "week":
        start_date = end_date - timedelta(days=7)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    else:
        start_date = end_date - timedelta(days=90)
    
    # Get data
    attendance_records = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id,
        models.Attendance.date >= start_date
    ).all()
    
    attendance_rate = len([a for a in attendance_records if a.status.value == "PRESENT"]) / max(len(attendance_records), 1) * 100
    
    key_points = [
        f"معدل الحضور: {attendance_rate:.1f}%",
        f"إجمالي أيام الحضور: {len([a for a in attendance_records if a.status.value == 'PRESENT'])}",
    ]
    
    summary = f"ملخص {period} للطالب {student.full_name}. "
    summary += f"معدل الحضور خلال هذه الفترة {attendance_rate:.1f}%. "
    summary += "ننصح بمتابعة التواصل مع المدرسة للحصول على تحديثات منتظمة."
    
    return SmartSummary(
        summary=summary,
        key_points=key_points,
        period=period
    )

@router.get("/predictive-absenteeism")
def predict_absenteeism(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Predict potential absenteeism (non-diagnostic)
    Ethical: Supportive guidance only, no classification
    """
    if current_user.role.value not in ["parent", "teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Analyze recent patterns
    recent_attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id
    ).order_by(models.Attendance.date.desc()).limit(20).all()
    
    if len(recent_attendance) < 5:
        return {
            "prediction": "insufficient_data",
            "message": "لا توجد بيانات كافية للتنبؤ",
            "recommendation": "ننصح بمتابعة الحضور"
        }
    
    absent_recent = len([a for a in recent_attendance[:10] if a.status.value == "ABSENT"])
    absent_older = len([a for a in recent_attendance[10:] if a.status.value == "ABSENT"])
    
    if absent_recent > absent_older:
        return {
            "prediction": "increasing_trend",
            "message": "تم ملاحظة نمط غياب متزايد مؤخراً",
            "recommendation": "ننصح بمتابعة التواصل مع ولي الأمر والمدرسة لفهم الأسباب ودعم الحضور",
            "is_alarm": False
        }
    
    return {
        "prediction": "stable",
        "message": "نمط الحضور مستقر",
        "recommendation": "نواصل المتابعة"
    }





