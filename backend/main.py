"""
Amantac School Management System - Main Application
نظام أمانتاك لإدارة المدرسة
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


load_dotenv()

from app.database import engine, Base
from app.routers import (
    auth,
    students,
    buses,
    attendance,
    pickup,
    dismissal,
    academic,
    behavior,
    activities,
    notifications,
    teacher_dashboard,
    teacher_assignments,
    teacher_evaluations,
    teacher_messages,
    teacher_exams,
    teacher_announcements,
    ai_insights,
    audit,
    staff_dashboard,
    staff_teachers,
    staff_approvals,
    staff_buses,
    staff_notifications,
    admin_classes,
    driver
)

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown

app = FastAPI(
    title="Amantac School Management System",
    description="نظام متكامل لإدارة المدرسة وتتبع سلامة الطلاب",
    version="1.0.0",
    lifespan=lifespan
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

frontend_dist = "../frontend/dist"

app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    index_path = os.path.join(frontend_dist, "index.html")
    return FileResponse(index_path)

# CORS Middleware - Configure from environment variables
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins != "*":
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",")]
else:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(buses.router, prefix="/api/buses", tags=["Buses"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(pickup.router, prefix="/api/pickup", tags=["Pickup"])
app.include_router(dismissal.router, prefix="/api/dismissal", tags=["Dismissal"])
app.include_router(academic.router, prefix="/api/academic", tags=["Academic"])
app.include_router(behavior.router, prefix="/api/behavior", tags=["Behavior"])
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])

# Teacher routes
app.include_router(teacher_assignments.router, prefix="/api", tags=["Teacher Assignments"])
app.include_router(teacher_evaluations.router, prefix="/api", tags=["Teacher Evaluations"])
app.include_router(teacher_messages.router, prefix="/api", tags=["Teacher Messages"])
app.include_router(teacher_dashboard.router, prefix="/api", tags=["Teacher Dashboard"])
app.include_router(teacher_exams.router, prefix="/api", tags=["Teacher Exams"])
app.include_router(teacher_announcements.router, prefix="/api", tags=["Teacher Announcements"])

# AI & Security routes
app.include_router(ai_insights.router, prefix="/api", tags=["AI Insights"])
app.include_router(audit.router, prefix="/api", tags=["Audit"])

# Staff routes
app.include_router(staff_dashboard.router, prefix="/api", tags=["Staff Dashboard"])
app.include_router(staff_teachers.router, prefix="/api", tags=["Staff Teachers"])
app.include_router(staff_approvals.router, prefix="/api", tags=["Staff Approvals"])
app.include_router(staff_buses.router, prefix="/api", tags=["Staff Buses"])
app.include_router(staff_notifications.router, prefix="/api", tags=["Staff Notifications"])

# Admin routes
app.include_router(admin_classes.router, prefix="/api", tags=["Admin Classes"])

# Driver routes
app.include_router(driver.router, prefix="/api", tags=["Driver"])

# @app.get("/")
# async def root():
 #   return {
 #       "message": "Welcome to Amantac School Management System",
 #       "version": "1.0.0",
 #       "status": "running"
  #  }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

