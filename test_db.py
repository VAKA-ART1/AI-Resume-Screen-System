from database import db

if db.is_connected():
    print("✅ MySQL Connected Successfully!")
else:
    print("❌ Connection Failed")