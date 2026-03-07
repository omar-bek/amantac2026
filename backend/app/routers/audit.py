"""
Audit Log Router for Security & Privacy
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app import models
from app.routers.auth import get_current_user
from app.models.audit_log import AuditActionType

router = APIRouter(prefix="/audit", tags=["audit"])

def log_audit_event(
    db: Session,
    user_id: Optional[int],
    action_type: AuditActionType,
    resource_type: str,
    resource_id: Optional[int] = None,
    description: str = "",
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    extra_data: Optional[dict] = None
):
    """Helper function to log audit events"""
    audit_log = models.AuditLog(
        user_id=user_id,
        action_type=action_type,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        extra_data=extra_data
    )
    db.add(audit_log)
    db.commit()
    return audit_log

@router.get("/logs")
def get_audit_logs(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    action_type: Optional[AuditActionType] = None,
    resource_type: Optional[str] = None,
    user_id: Optional[int] = None,
    limit: int = Query(default=100, le=1000),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get audit logs
    Only admins and super_admins can access
    """
    if current_user.role.value not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Only admins can access audit logs")
    
    query = db.query(models.AuditLog)
    
    if start_date:
        query = query.filter(models.AuditLog.created_at >= start_date)
    if end_date:
        query = query.filter(models.AuditLog.created_at <= end_date)
    if action_type:
        query = query.filter(models.AuditLog.action_type == action_type)
    if resource_type:
        query = query.filter(models.AuditLog.resource_type == resource_type)
    if user_id:
        query = query.filter(models.AuditLog.user_id == user_id)
    
    logs = query.order_by(models.AuditLog.created_at.desc()).limit(limit).all()
    return logs

@router.get("/logs/my")
def get_my_audit_logs(
    limit: int = Query(default=50, le=500),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get user's own audit logs"""
    logs = db.query(models.AuditLog).filter(
        models.AuditLog.user_id == current_user.id
    ).order_by(models.AuditLog.created_at.desc()).limit(limit).all()
    return logs

@router.get("/stats")
def get_audit_stats(
    days: int = Query(default=30, le=365),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get audit statistics"""
    if current_user.role.value not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Only admins can access audit stats")
    
    start_date = datetime.now() - timedelta(days=days)
    
    total_logs = db.query(models.AuditLog).filter(
        models.AuditLog.created_at >= start_date
    ).count()
    
    action_counts = {}
    for action in AuditActionType:
        count = db.query(models.AuditLog).filter(
            models.AuditLog.action_type == action,
            models.AuditLog.created_at >= start_date
        ).count()
        action_counts[action.value] = count
    
    return {
        "total_logs": total_logs,
        "period_days": days,
        "action_counts": action_counts
    }

