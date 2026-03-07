"""
Seed all users (Teachers, Parents, Admins, Drivers, Students, Super Admin)
"""

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.routers.auth import get_password_hash
from app import models

def seed_all_users():
    db = SessionLocal()
    try:
        print("🌱 Starting to seed all users...\n")

        # 1. Super Admin
        print("1️⃣ Creating Super Admin...")
        super_admin = db.query(User).filter(User.email == "superadmin@amantac.com").first()
        if not super_admin:
            super_admin = User(
                email="superadmin@amantac.com",
                phone="+201000000001",
                hashed_password=get_password_hash("superadmin123"),
                full_name="المشرف العام",
                role=UserRole.SUPER_ADMIN,
                is_active=True
            )
            db.add(super_admin)
            db.commit()
            print("   ✅ Super Admin created: superadmin@amantac.com / superadmin123")
        else:
            print("   ⚠️  Super Admin already exists")

        # 2. School Admin
        print("\n2️⃣ Creating School Admins...")
        admin_users = [
            {
                "email": "admin@amantac.com",
                "phone": "+201000000002",
                "password": "admin123",
                "name": "مدير المدرسة"
            },
            {
                "email": "admin2@amantac.com",
                "phone": "+201000000003",
                "password": "admin123",
                "name": "مدير المدرسة الثاني"
            }
        ]
        for admin_data in admin_users:
            admin = db.query(User).filter(User.email == admin_data["email"]).first()
            if not admin:
                admin = User(
                    email=admin_data["email"],
                    phone=admin_data["phone"],
                    hashed_password=get_password_hash(admin_data["password"]),
                    full_name=admin_data["name"],
                    role=UserRole.ADMIN,
                    is_active=True
                )
                db.add(admin)
                print(f"   ✅ Admin created: {admin_data['email']} / {admin_data['password']}")
            else:
                print(f"   ⚠️  Admin already exists: {admin_data['email']}")
        db.commit()

        # 3. Teachers
        print("\n3️⃣ Creating Teachers...")
        teachers = [
            {
                "email": "teacher1@amantac.com",
                "phone": "+201000000010",
                "password": "teacher123",
                "name": "أحمد محمد - مدرس رياضيات"
            },
            {
                "email": "teacher2@amantac.com",
                "phone": "+201000000011",
                "password": "teacher123",
                "name": "فاطمة علي - مدرسة علوم"
            },
            {
                "email": "teacher3@amantac.com",
                "phone": "+201000000012",
                "password": "teacher123",
                "name": "محمد حسن - مدرس لغة عربية"
            },
            {
                "email": "teacher4@amantac.com",
                "phone": "+201000000013",
                "password": "teacher123",
                "name": "سارة أحمد - مدرسة إنجليزية"
            },
            {
                "email": "teacher5@amantac.com",
                "phone": "+201000000014",
                "password": "teacher123",
                "name": "خالد إبراهيم - مدرس تربية رياضية"
            }
        ]
        for teacher_data in teachers:
            teacher = db.query(User).filter(User.email == teacher_data["email"]).first()
            if not teacher:
                teacher = User(
                    email=teacher_data["email"],
                    phone=teacher_data["phone"],
                    hashed_password=get_password_hash(teacher_data["password"]),
                    full_name=teacher_data["name"],
                    role=UserRole.TEACHER,
                    is_active=True
                )
                db.add(teacher)
                print(f"   ✅ Teacher created: {teacher_data['email']} / {teacher_data['password']}")
            else:
                print(f"   ⚠️  Teacher already exists: {teacher_data['email']}")
        db.commit()

        # 4. Parents
        print("\n4️⃣ Creating Parents...")
        parents = [
            {
                "email": "parent1@amantac.com",
                "phone": "+201000000020",
                "password": "parent123",
                "name": "علي أحمد - ولي أمر"
            },
            {
                "email": "parent2@amantac.com",
                "phone": "+201000000021",
                "password": "parent123",
                "name": "مريم خالد - ولي أمر"
            },
            {
                "email": "parent3@amantac.com",
                "phone": "+201000000022",
                "password": "parent123",
                "name": "حسن محمود - ولي أمر"
            },
            {
                "email": "parent4@amantac.com",
                "phone": "+201000000023",
                "password": "parent123",
                "name": "نورا سعيد - ولي أمر"
            },
            {
                "email": "parent5@amantac.com",
                "phone": "+201000000024",
                "password": "parent123",
                "name": "يوسف عمر - ولي أمر"
            }
        ]
        for parent_data in parents:
            parent = db.query(User).filter(User.email == parent_data["email"]).first()
            if not parent:
                parent = User(
                    email=parent_data["email"],
                    phone=parent_data["phone"],
                    hashed_password=get_password_hash(parent_data["password"]),
                    full_name=parent_data["name"],
                    role=UserRole.PARENT,
                    is_active=True
                )
                db.add(parent)
                print(f"   ✅ Parent created: {parent_data['email']} / {parent_data['password']}")
            else:
                print(f"   ⚠️  Parent already exists: {parent_data['email']}")
        db.commit()

        # 5. Drivers
        print("\n5️⃣ Creating Drivers...")
        drivers = [
            {
                "email": "driver1@amantac.com",
                "phone": "+201000000030",
                "password": "driver123",
                "name": "محمود السائق - سائق حافلة 1"
            },
            {
                "email": "driver2@amantac.com",
                "phone": "+201000000031",
                "password": "driver123",
                "name": "إبراهيم السائق - سائق حافلة 2"
            },
            {
                "email": "driver3@amantac.com",
                "phone": "+201000000032",
                "password": "driver123",
                "name": "عمر السائق - سائق حافلة 3"
            }
        ]
        for driver_data in drivers:
            driver = db.query(User).filter(User.email == driver_data["email"]).first()
            if not driver:
                driver = User(
                    email=driver_data["email"],
                    phone=driver_data["phone"],
                    hashed_password=get_password_hash(driver_data["password"]),
                    full_name=driver_data["name"],
                    role=UserRole.DRIVER,
                    is_active=True
                )
                db.add(driver)
                print(f"   ✅ Driver created: {driver_data['email']} / {driver_data['password']}")
            else:
                print(f"   ⚠️  Driver already exists: {driver_data['email']}")
        db.commit()

        # 6. Staff
        print("\n6️⃣ Creating Staff...")
        staff_members = [
            {
                "email": "staff1@amantac.com",
                "phone": "+201000000040",
                "password": "staff123",
                "name": "سالم الموظف - موظف إداري"
            },
            {
                "email": "staff2@amantac.com",
                "phone": "+201000000041",
                "password": "staff123",
                "name": "ليلى الموظفة - موظفة استقبال"
            }
        ]
        for staff_data in staff_members:
            staff = db.query(User).filter(User.email == staff_data["email"]).first()
            if not staff:
                staff = User(
                    email=staff_data["email"],
                    phone=staff_data["phone"],
                    hashed_password=get_password_hash(staff_data["password"]),
                    full_name=staff_data["name"],
                    role=UserRole.STAFF,
                    is_active=True
                )
                db.add(staff)
                print(f"   ✅ Staff created: {staff_data['email']} / {staff_data['password']}")
            else:
                print(f"   ⚠️  Staff already exists: {staff_data['email']}")
        db.commit()

        # 7. Government/Authority Admins
        print("\n7️⃣ Creating Government/Authority Admins...")
        government_admins = [
            {
                "email": "government@amantac.com",
                "phone": "+971500000001",
                "password": "government123",
                "name": "مسؤول الحكومة - Government Admin"
            },
            {
                "email": "authority@amantac.com",
                "phone": "+971500000002",
                "password": "authority123",
                "name": "مسؤول السلطة - Authority Admin"
            }
        ]
        for gov_admin_data in government_admins:
            gov_admin = db.query(User).filter(User.email == gov_admin_data["email"]).first()
            if not gov_admin:
                # Determine role based on email
                role = UserRole.GOVERNMENT_ADMIN if "government" in gov_admin_data["email"] else UserRole.AUTHORITY_ADMIN
                gov_admin = User(
                    email=gov_admin_data["email"],
                    phone=gov_admin_data["phone"],
                    hashed_password=get_password_hash(gov_admin_data["password"]),
                    full_name=gov_admin_data["name"],
                    role=role,
                    is_active=True
                )
                db.add(gov_admin)
                print(f"   ✅ Government Admin created: {gov_admin_data['email']} / {gov_admin_data['password']}")
            else:
                print(f"   ⚠️  Government Admin already exists: {gov_admin_data['email']}")
        db.commit()

        # 8. Students (Optional - if you want student portal users)
        print("\n8️⃣ Creating Students (Optional)...")
        students = [
            {
                "email": "student1@amantac.com",
                "phone": "+201000000050",
                "password": "student123",
                "name": "أحمد علي - طالب"
            },
            {
                "email": "student2@amantac.com",
                "phone": "+201000000051",
                "password": "student123",
                "name": "فاطمة محمد - طالبة"
            }
        ]
        for student_data in students:
            student = db.query(User).filter(User.email == student_data["email"]).first()
            if not student:
                student = User(
                    email=student_data["email"],
                    phone=student_data["phone"],
                    hashed_password=get_password_hash(student_data["password"]),
                    full_name=student_data["name"],
                    role=UserRole.STUDENT,
                    is_active=True
                )
                db.add(student)
                print(f"   ✅ Student created: {student_data['email']} / {student_data['password']}")
            else:
                print(f"   ⚠️  Student already exists: {student_data['email']}")
        db.commit()

        print("\n" + "="*60)
        print("✅ All users seeded successfully!")
        print("="*60)
        print("\n📋 Summary:")
        print("   - 1 Super Admin")
        print("   - 2 School Admins")
        print("   - 5 Teachers")
        print("   - 5 Parents")
        print("   - 3 Drivers")
        print("   - 2 Staff")
        print("   - 2 Government/Authority Admins")
        print("   - 2 Students (Optional)")
        print("\n💡 Total: 22 users")
        print("\n🔑 Default passwords:")
        print("   - Super Admin: superadmin123")
        print("   - Admins: admin123")
        print("   - Teachers: teacher123")
        print("   - Parents: parent123")
        print("   - Drivers: driver123")
        print("   - Staff: staff123")
        print("   - Government Admin: government123")
        print("   - Authority Admin: authority123")
        print("   - Students: student123")
        print("\n⚠️  Please change passwords after first login!")

    except Exception as e:
        print(f"\n❌ Error seeding users: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_all_users()

