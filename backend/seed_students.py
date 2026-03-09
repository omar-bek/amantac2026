"""
Seed Student records
Creates Student model records linked to parent users
"""

import sys
import io

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from app.database import SessionLocal
from app.models.student import Student
from app.models.user import User, UserRole
from datetime import date, timedelta
import random

def seed_students():
    db = SessionLocal()
    try:
        print("Starting to seed students...\n")

        # Get parent users
        parents = db.query(User).filter(User.role == UserRole.PARENT).all()
        if not parents:
            print("[WARNING] No parent users found. Please run seed_all_users.py first to create parents.")
            return

        print(f"Found {len(parents)} parent(s)\n")

        # Sample student data
        students_data = [
            {
                "student_id": "STU001",
                "full_name": "أحمد علي",
                "grade": "1",
                "class_name": "1A",
                "date_of_birth": date(2018, 3, 15),
            },
            {
                "student_id": "STU002",
                "full_name": "فاطمة محمد",
                "grade": "1",
                "class_name": "1A",
                "date_of_birth": date(2018, 5, 20),
            },
            {
                "student_id": "STU003",
                "full_name": "محمد حسن",
                "grade": "1",
                "class_name": "1B",
                "date_of_birth": date(2018, 7, 10),
            },
            {
                "student_id": "STU004",
                "full_name": "سارة أحمد",
                "grade": "2",
                "class_name": "2A",
                "date_of_birth": date(2017, 2, 14),
            },
            {
                "student_id": "STU005",
                "full_name": "خالد إبراهيم",
                "grade": "2",
                "class_name": "2A",
                "date_of_birth": date(2017, 9, 5),
            },
            {
                "student_id": "STU006",
                "full_name": "نورا سعيد",
                "grade": "2",
                "class_name": "2B",
                "date_of_birth": date(2017, 11, 22),
            },
            {
                "student_id": "STU007",
                "full_name": "يوسف عمر",
                "grade": "3",
                "class_name": "3A",
                "date_of_birth": date(2016, 4, 8),
            },
            {
                "student_id": "STU008",
                "full_name": "مريم خالد",
                "grade": "3",
                "class_name": "3A",
                "date_of_birth": date(2016, 6, 30),
            },
            {
                "student_id": "STU009",
                "full_name": "عمر محمود",
                "grade": "3",
                "class_name": "3B",
                "date_of_birth": date(2016, 8, 12),
            },
            {
                "student_id": "STU010",
                "full_name": "ليلى أحمد",
                "grade": "4",
                "class_name": "4A",
                "date_of_birth": date(2015, 1, 25),
            },
            {
                "student_id": "STU011",
                "full_name": "حسام الدين",
                "grade": "4",
                "class_name": "4A",
                "date_of_birth": date(2015, 3, 18),
            },
            {
                "student_id": "STU012",
                "full_name": "رنا محمد",
                "grade": "4",
                "class_name": "4B",
                "date_of_birth": date(2015, 10, 7),
            },
            {
                "student_id": "STU013",
                "full_name": "طارق علي",
                "grade": "5",
                "class_name": "5A",
                "date_of_birth": date(2014, 5, 15),
            },
            {
                "student_id": "STU014",
                "full_name": "هند سامي",
                "grade": "5",
                "class_name": "5A",
                "date_of_birth": date(2014, 7, 28),
            },
            {
                "student_id": "STU015",
                "full_name": "عبدالله كريم",
                "grade": "5",
                "class_name": "5B",
                "date_of_birth": date(2014, 12, 3),
            },
            {
                "student_id": "STU016",
                "full_name": "زينب حسن",
                "grade": "6",
                "class_name": "6A",
                "date_of_birth": date(2013, 2, 20),
            },
            {
                "student_id": "STU017",
                "full_name": "مصطفى رضا",
                "grade": "6",
                "class_name": "6A",
                "date_of_birth": date(2013, 4, 11),
            },
            {
                "student_id": "STU018",
                "full_name": "سلمى نادر",
                "grade": "6",
                "class_name": "6B",
                "date_of_birth": date(2013, 9, 19),
            },
            {
                "student_id": "STU019",
                "full_name": "باسم خليل",
                "grade": "7",
                "class_name": "7A",
                "date_of_birth": date(2012, 6, 5),
            },
            {
                "student_id": "STU020",
                "full_name": "ريم عادل",
                "grade": "7",
                "class_name": "7A",
                "date_of_birth": date(2012, 8, 16),
            },
        ]

        created_count = 0
        skipped_count = 0

        for idx, student_data in enumerate(students_data):
            # Check if student already exists
            existing_student = db.query(Student).filter(
                Student.student_id == student_data["student_id"]
            ).first()

            if existing_student:
                print(f"   [SKIP] Student {student_data['student_id']} ({student_data['full_name']}) already exists.")
                skipped_count += 1
                continue

            # Assign parent (cycle through available parents)
            parent = parents[idx % len(parents)]

            # Create student
            student = Student(
                student_id=student_data["student_id"],
                full_name=student_data["full_name"],
                grade=student_data["grade"],
                class_name=student_data["class_name"],
                date_of_birth=student_data["date_of_birth"],
                parent_id=parent.id,
                is_active=True
            )

            db.add(student)
            created_count += 1
            print(f"   [OK] Created student: {student_data['student_id']} - {student_data['full_name']} ({student_data['grade']}/{student_data['class_name']}) - Parent: {parent.full_name}")

        db.commit()

        print("\n" + "="*60)
        print("Student seeding completed!")
        print("="*60)
        print(f"\nSummary:")
        print(f"   - Created: {created_count} students")
        print(f"   - Skipped: {skipped_count} students (already exist)")
        print(f"   - Total: {created_count + skipped_count} students")
        print(f"\nStudents are distributed across:")
        print(f"   - Grades: 1-7")
        print(f"   - Classes: Multiple classes per grade")
        print(f"   - Parents: Linked to existing parent users")

    except Exception as e:
        print(f"\n[ERROR] Error seeding students: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_students()
