from app.core.database import engine

try:
    connection = engine.connect()

    print("✅ Connected to MySQL Successfully!")

    connection.close()

except Exception as e:
    print("❌ Connection Failed")

    print(e)