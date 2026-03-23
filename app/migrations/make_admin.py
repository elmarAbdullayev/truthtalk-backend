from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

# Replace with your email
admin_email = "abdullayevelmar758@gmail.com"

user = db.query(User).filter(User.email == admin_email).first()
if user:
    user.is_admin = True
    db.commit()
    print(f"✅ {user.username} is now admin!")
else:
    print("❌ User not found")

db.close()