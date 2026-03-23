from app.core.database import engine

# Add columns manually
with engine.connect() as conn:
    try:
        conn.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE")
        print("✅ Added is_admin column")
    except:
        print("⚠️ is_admin column already exists")

    try:
        conn.execute("ALTER TABLE users ADD COLUMN is_banned BOOLEAN DEFAULT FALSE")
        print("✅ Added is_banned column")
    except:
        print("⚠️ is_banned column already exists")

    conn.commit()

print("✅ Migration complete!")