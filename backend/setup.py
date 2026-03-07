"""
Setup script for initial database setup
"""

from app.database import engine, Base, SessionLocal
from app.models import User
from app.models.user import UserRole
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    """Initialize database with tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def create_admin_user():
    """Create default admin user"""
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@amantac.com").first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            email="admin@amantac.com",
            phone="+1234567890",
            hashed_password=pwd_context.hash("admin123"),
            full_name="System Administrator",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("Admin user created successfully!")
        print("Email: admin@amantac.com")
        print("Password: admin123")
        print("Please change the password after first login!")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("\nCreating admin user...")
    create_admin_user()
    print("\nSetup completed!")





