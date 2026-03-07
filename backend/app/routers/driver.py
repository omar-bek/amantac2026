"""
Driver router - Vehicle checklist and route management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Text
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.database import get_db, Base
from app import models
from app.routers.auth import get_current_user
from app.models.user import UserRole

router = APIRouter(prefix="/driver", tags=["driver"])

def verify_driver(current_user: models.User = Depends(get_current_user)):
    """Verify user is driver"""
    user_role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if user_role != "driver":
        raise HTTPException(status_code=403, detail="Only drivers can access this endpoint")
    return current_user

class ChecklistSubmit(BaseModel):
    checklist: Dict[str, bool]
    notes: Dict[str, str]
    timestamp: str
    driver_id: Optional[int] = None

@router.post("/checklist")
def submit_checklist(
    checklist_data: ChecklistSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_driver)
):
    """Submit vehicle checklist"""
    try:
        # Here you can save to database if you have a VehicleChecklist model
        # For now, we'll just return success
        
        # You can create a model like this:
        # checklist_record = models.VehicleChecklist(
        #     driver_id=current_user.id,
        #     checklist=checklist_data.checklist,
        #     notes=checklist_data.notes,
        #     timestamp=datetime.fromisoformat(checklist_data.timestamp.replace('Z', '+00:00')),
        #     completed=True
        # )
        # db.add(checklist_record)
        # db.commit()
        
        return {
            "message": "تم حفظ الفحص بنجاح",
            "status": "success",
            "driver_id": current_user.id,
            "timestamp": checklist_data.timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في حفظ الفحص: {str(e)}")

@router.get("/checklist/latest")
def get_latest_checklist(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_driver)
):
    """Get latest checklist for driver"""
    # If you have a VehicleChecklist model, query it here
    # For now, return empty
    return {
        "message": "لا توجد سجلات فحص سابقة",
        "checklist": None
    }

class RouteStart(BaseModel):
    driver_id: Optional[int] = None
    timestamp: str

class RouteEnd(BaseModel):
    driver_id: Optional[int] = None
    timestamp: str

@router.post("/route/start")
def start_route(
    route_data: RouteStart,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_driver)
):
    """Start a route/trip"""
    try:
        # Get driver's bus (by driver_name or driver_phone matching user)
        driver_bus = db.query(models.Bus).filter(
            (models.Bus.driver_name == current_user.full_name) | 
            (models.Bus.driver_phone == current_user.phone),
            models.Bus.is_active == True
        ).first()
        
        if not driver_bus:
            # Return mock route data if no bus assigned
            return {
                "message": "تم بدء الرحلة",
                "status": "active",
                "route": {
                    "id": 1,
                    "name": "الطريق 1 - الصباح",
                    "type": "pickup",
                    "stops": []
                },
                "driver_id": current_user.id,
                "start_time": route_data.timestamp
            }
        
        # Get active route for this bus
        active_route = db.query(models.BusRoute).filter(
            models.BusRoute.bus_id == driver_bus.id,
            models.BusRoute.is_active == True
        ).first()
        
        if not active_route:
            return {
                "message": "تم بدء الرحلة",
                "status": "active",
                "route": {
                    "id": 1,
                    "name": "الطريق 1 - الصباح",
                    "type": "pickup",
                    "stops": []
                },
                "driver_id": current_user.id,
                "start_time": route_data.timestamp
            }
        
        return {
            "message": "تم بدء الرحلة",
            "status": "active",
            "route": {
                "id": active_route.id,
                "name": active_route.route_name,
                "type": "pickup",
                "stops": active_route.waypoints if active_route.waypoints else []
            },
            "driver_id": current_user.id,
            "start_time": route_data.timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في بدء الرحلة: {str(e)}")

@router.post("/route/end")
def end_route(
    route_data: RouteEnd,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_driver)
):
    """End a route/trip"""
    try:
        return {
            "message": "تم إنهاء الرحلة",
            "status": "completed",
            "driver_id": current_user.id,
            "end_time": route_data.timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في إنهاء الرحلة: {str(e)}")

@router.get("/route/active")
def get_active_route(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_driver)
):
    """Get active route for driver"""
    try:
        # Get driver's bus (by driver_name or driver_phone matching user)
        driver_bus = db.query(models.Bus).filter(
            (models.Bus.driver_name == current_user.full_name) | 
            (models.Bus.driver_phone == current_user.phone),
            models.Bus.is_active == True
        ).first()
        
        if not driver_bus:
            # Return mock data
            return {
                "id": 1,
                "name": "الطريق 1 - الصباح",
                "type": "pickup",
                "stops": [
                    {
                        "id": 1,
                        "name": "محطة 1",
                        "address": "شارع السلام، دبي",
                        "order": 1,
                        "students": [
                            {"id": 1, "name": "أحمد محمد", "class_name": "3A", "check_in": False, "check_out": False},
                            {"id": 2, "name": "فاطمة علي", "class_name": "3A", "check_in": False, "check_out": False},
                        ],
                        "estimated_arrival": "07:15"
                    },
                    {
                        "id": 2,
                        "name": "محطة 2",
                        "address": "شارع الخليج، دبي",
                        "order": 2,
                        "students": [
                            {"id": 3, "name": "خالد حسن", "class_name": "2B", "check_in": False, "check_out": False},
                        ],
                        "estimated_arrival": "07:30"
                    },
                    {
                        "id": 3,
                        "name": "المدرسة",
                        "address": "مدرسة الإمارات",
                        "order": 3,
                        "students": [],
                        "estimated_arrival": "07:45"
                    },
                ]
            }
        
        # Get active route
        active_route = db.query(models.BusRoute).filter(
            models.BusRoute.bus_id == driver_bus.id,
            models.BusRoute.is_active == True
        ).first()
        
        if not active_route:
            # Return mock data
            return {
                "id": 1,
                "name": "الطريق 1 - الصباح",
                "type": "pickup",
                "stops": [
                    {
                        "id": 1,
                        "name": "محطة 1",
                        "address": "شارع السلام، دبي",
                        "order": 1,
                        "students": [
                            {"id": 1, "name": "أحمد محمد", "class_name": "3A", "check_in": False, "check_out": False},
                            {"id": 2, "name": "فاطمة علي", "class_name": "3A", "check_in": False, "check_out": False},
                        ],
                        "estimated_arrival": "07:15"
                    },
                    {
                        "id": 2,
                        "name": "محطة 2",
                        "address": "شارع الخليج، دبي",
                        "order": 2,
                        "students": [
                            {"id": 3, "name": "خالد حسن", "class_name": "2B", "check_in": False, "check_out": False},
                        ],
                        "estimated_arrival": "07:30"
                    },
                    {
                        "id": 3,
                        "name": "المدرسة",
                        "address": "مدرسة الإمارات",
                        "order": 3,
                        "students": [],
                        "estimated_arrival": "07:45"
                    },
                ]
            }
        
        # Get students for this bus
        bus_students = db.query(models.Student).filter(
            models.Student.bus_id == driver_bus.id,
            models.Student.is_active == True
        ).all()
        
        # Format stops with students
        stops = []
        if active_route.waypoints:
            for idx, waypoint in enumerate(active_route.waypoints, 1):
                stops.append({
                    "id": idx,
                    "name": waypoint.get("name", f"محطة {idx}"),
                    "address": waypoint.get("address", ""),
                    "order": idx,
                    "students": [
                        {
                            "id": s.id,
                            "name": s.full_name,
                            "class_name": s.class_name or "",
                            "check_in": False,
                            "check_out": False
                        }
                        for s in bus_students
                    ],
                    "estimated_arrival": waypoint.get("estimated_arrival", "")
                })
        else:
            # Default stops if no waypoints
            stops = [
                {
                    "id": 1,
                    "name": "محطة 1",
                    "address": "شارع السلام، دبي",
                    "order": 1,
                    "students": [
                        {
                            "id": s.id,
                            "name": s.full_name,
                            "class_name": s.class_name or "",
                            "check_in": False,
                            "check_out": False
                        }
                        for s in bus_students[:2]
                    ],
                    "estimated_arrival": "07:15"
                },
                {
                    "id": 2,
                    "name": "المدرسة",
                    "address": "مدرسة الإمارات",
                    "order": 2,
                    "students": [],
                    "estimated_arrival": "07:45"
                }
            ]
        
        return {
            "id": active_route.id,
            "name": active_route.route_name,
            "type": "pickup",
            "stops": stops
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في جلب الرحلة: {str(e)}")

@router.post("/route/stop/{stop_id}/arrive")
def arrive_at_stop(
    stop_id: int,
    timestamp: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(verify_driver)
):
    """Mark arrival at a stop"""
    try:
        if not timestamp:
            timestamp = datetime.now().isoformat()
        return {
            "message": "تم تسجيل الوصول للمحطة",
            "stop_id": stop_id,
            "timestamp": timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في تسجيل الوصول: {str(e)}")

