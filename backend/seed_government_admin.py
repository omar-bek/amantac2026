"""
Quick script to seed government admin users
Run this if you need to add government admin users quickly
"""

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.routers.auth import get_password_hash

def seed_government_admins():
    db = SessionLocal()
    try:
        print("🌱 Seeding Government/Authority Admins...\n")

        # Government Admin
        print("1️⃣ Creating Government Admin...")
        gov_admin = db.query(User).filter(User.email == "government@amantac.com").first()
        if not gov_admin:
            gov_admin = User(
                email="government@amantac.com",
                phone="+971500000001",
                hashed_password=get_password_hash("government123"),
                full_name="مسؤول الحكومة - Government Admin",
                role=UserRole.GOVERNMENT_ADMIN,
                is_active=True
            )
            db.add(gov_admin)
            db.commit()
            print("   ✅ Government Admin created: government@amantac.com / government123")
        else:
            # Update existing user to ensure correct role and password
            gov_admin.role = UserRole.GOVERNMENT_ADMIN
            gov_admin.hashed_password = get_password_hash("government123")
            gov_admin.is_active = True
            db.commit()
            print("   ✅ Government Admin updated: government@amantac.com / government123")

        # Authority Admin
        print("\n2️⃣ Creating Authority Admin...")
        auth_admin = db.query(User).filter(User.email == "authority@amantac.com").first()
        if not auth_admin:
            auth_admin = User(
                email="authority@amantac.com",
                phone="+971500000002",
                hashed_password=get_password_hash("authority123"),
                full_name="مسؤول السلطة - Authority Admin",
                role=UserRole.AUTHORITY_ADMIN,
                is_active=True
            )
            db.add(auth_admin)
            db.commit()
            print("   ✅ Authority Admin created: authority@amantac.com / authority123")
        else:
            # Update existing user to ensure correct role and password
            auth_admin.role = UserRole.AUTHORITY_ADMIN
            auth_admin.hashed_password = get_password_hash("authority123")
            auth_admin.is_active = True
            db.commit()
            print("   ✅ Authority Admin updated: authority@amantac.com / authority123")

        print("\n" + "="*60)
        print("✅ Government/Authority Admins seeded successfully!")
        print("="*60)
        print("\n🔑 Login Credentials:")
        print("   Government Admin:")
        print("   - Email: government@amantac.com")
        print("   - Password: government123")
        print("\n   Authority Admin:")
        print("   - Email: authority@amantac.com")
        print("   - Password: authority123")
        print("\n⚠️  Please change passwords after first login!")

    except Exception as e:
        print(f"\n❌ Error seeding government admins: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_government_admins()


