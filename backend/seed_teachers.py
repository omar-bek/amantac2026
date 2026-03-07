"""
Seed script to create sample teachers
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.routers.auth import get_password_hash
from sqlalchemy.orm import Session

def create_teachers():
    """Create sample teachers"""
    db: Session = SessionLocal()
    created_count = 0
    
    try:
        # Check if teachers already exist
        existing_teachers = db.query(User).filter(User.role == UserRole.TEACHER).all()
        if existing_teachers:
            print(f"ℹ️  Found {len(existing_teachers)} existing teachers:")
            for teacher in existing_teachers:
                print(f"   - {teacher.full_name} ({teacher.email})")

        teachers = [
            {
                "email": "teacher1@amantac.com",
                "full_name": "أحمد محمد علي",
                "phone": "01012345678",
                "password": "teacher123",
                "role": UserRole.TEACHER
            },
            {
                "email": "teacher2@amantac.com",
                "full_name": "فاطمة أحمد حسن",
                "phone": "01012345679",
                "password": "teacher123",
                "role": UserRole.TEACHER
            },
            {
                "email": "teacher3@amantac.com",
                "full_name": "محمد سعيد إبراهيم",
                "phone": "01012345680",
                "password": "teacher123",
                "role": UserRole.TEACHER
            },
            {
                "email": "teacher4@amantac.com",
                "full_name": "سارة محمود عبدالله",
                "phone": "01012345681",
                "password": "teacher123",
                "role": UserRole.TEACHER
            },
            {
                "email": "teacher5@amantac.com",
                "full_name": "خالد يوسف أحمد",
                "phone": "01012345682",
                "password": "teacher123",
                "role": UserRole.TEACHER
            },
            {
                "email": "teacher6@amantac.com",
                "full_name": "مريم علي محمود",
                "phone": "01012345683",
                "password": "teacher123",
                "role": UserRole.TEACHER
            },
            {
                "email": "teacher7@amantac.com",
                "full_name": "يوسف خالد محمد",
                "phone": "01012345684",
                "password": "teacher123",
                "role": UserRole.TEACHER
            },
            {
                "email": "teacher8@amantac.com",
                "full_name": "نورا سعد الدين",
                "phone": "01012345685",
                "password": "teacher123",
                "role": UserRole.TEACHER
            }
        ]
        

        for teacher_data in teachers:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == teacher_data["email"]).first()
            if existing_user:
                print(f"⚠️  User {teacher_data['email']} already exists. Skipping.")
                continue
            
            # Hash password
            hashed_password = get_password_hash(teacher_data["password"])
            
            # Create user
            teacher = User(
                email=teacher_data["email"],
                full_name=teacher_data["full_name"],
                phone=teacher_data.get("phone"),
                hashed_password=hashed_password,
                role=teacher_data["role"],
                is_active=True
            )
            
            db.add(teacher)
            created_count += 1
            print(f"✅ Created teacher: {teacher_data['full_name']} ({teacher_data['email']})")
        
        db.commit()
        print(f"\n🎉 Successfully created {created_count} teachers!")
        print("\n📋 Login credentials:")
        print("   Email: teacher1@amantac.com")
        print("   Password: teacher123")
        print("\n   (Same password for all teachers)")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating teachers: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Starting teacher seeding...")
    create_teachers()
    print("\n✅ Seeding completed!")
