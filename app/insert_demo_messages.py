from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# Replace with your actual PostgreSQL connection URL
DATABASE_URL = "postgresql://postgres:yourpassword@localhost/chat_app"

engine = create_engine(DATABASE_URL)

def insert_demo_messages(room_id: str, username: str):
    base_time = datetime.utcnow()

    with engine.connect() as connection:
        for i in range(20):
            timestamp = base_time - timedelta(seconds=i * 10)  # 10 seconds apart
            content = f"Demo message {20 - i}"  # So 1..20 ascending when reversed

            query = text("""
                INSERT INTO chat_messages (username, content, room_id, timestamp)
                VALUES (:username, :content, :room_id, :timestamp)
            """)

            connection.execute(query, {
                "username": username,
                "content": content,
                "room_id": room_id,
                "timestamp": timestamp
            })

        connection.commit()
    print("Inserted 20 demo messages.")

if __name__ == "__main__":
    insert_demo_messages(room_id="general", username="demo_user")
