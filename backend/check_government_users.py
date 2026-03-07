"""
Quick script to check if government admin users exist
"""

from app.database import SessionLocal
from app.models.user import User, UserRole

def check_government_users():
    db = SessionLocal()
    try:
        print("🔍 Checking for Government/Authority Admin users...\n")
        
        gov_admin = db.query(User).filter(User.email == "government@amantac.com").first()
        auth_admin = db.query(User).filter(User.email == "authority@amantac.com").first()
        
        if gov_admin:
            print("✅ Government Admin found:")
            print(f"   Email: {gov_admin.email}")
            print(f"   Role: {gov_admin.role}")
            print(f"   Active: {gov_admin.is_active}")
            print(f"   Name: {gov_admin.full_name}")
        else:
            print("❌ Government Admin NOT found")
            print("   Run: python seed_government_admin.py")
        
        print()
        
        if auth_admin:
            print("✅ Authority Admin found:")
            print(f"   Email: {auth_admin.email}")
            print(f"   Role: {auth_admin.role}")
            print(f"   Active: {auth_admin.is_active}")
            print(f"   Name: {auth_admin.full_name}")
        else:
            print("❌ Authority Admin NOT found")
            print("   Run: python seed_government_admin.py")
        
        print("\n" + "="*60)
        print("All users in database:")
        all_users = db.query(User).all()
        for user in all_users:
            print(f"  - {user.email} ({user.role.value})")
        
    except Exception as e:
        print(f"\n❌ Error checking users: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_government_users()


