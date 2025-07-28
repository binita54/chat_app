from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query, Header, HTTPException
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from .database import Base, engine, SessionLocal
from .routes.user_routes import user_router
from .auth import decode_token
import traceback
from fastapi.staticfiles import StaticFiles
from .routes import room
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)
app.include_router(user_router)
app.include_router(room.router)


@app.get("/")
def root():
    return {"message": "Chat API is running"}

# --- WebSocket Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, room_id: str, message: dict):
        for connection in self.active_connections.get(room_id, []):
            await connection.send_json(message)

manager = ConnectionManager()

# --- Database Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- HTTP GET endpoint to fetch older messages ---
@app.get("/messages/{room_id}")
def get_older_messages(
    room_id: str,
    before_timestamp: Optional[str] = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if payload is None or payload.get("sub") is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    query = text("""
        SELECT username, content, timestamp
        FROM chat_messages
        WHERE room_id = :room_id
        {time_filter}
        ORDER BY timestamp DESC
        LIMIT 20
    """.format(time_filter="AND timestamp < :before_timestamp" if before_timestamp else ""))

    params = {"room_id": room_id}
    if before_timestamp:
        params["before_timestamp"] = datetime.fromisoformat(before_timestamp)

    messages = db.execute(query, params).fetchall()

    return [
        {"username": m.username, "content": m.content, "timestamp": m.timestamp.isoformat()}
        for m in reversed(messages)
    ]

# --- WebSocket Endpoint ---
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
    before_timestamp: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if payload is None or payload.get("sub") is None:
        await websocket.close(code=1008)  # Unauthorized
        return

    username = payload["sub"]
    await manager.connect(room_id, websocket)

    try:
        # Fetch past messages
        if before_timestamp:
            try:
                before_dt = datetime.fromisoformat(before_timestamp)
            except Exception:
                before_dt = datetime.utcnow()  # fallback if invalid format

            query = text("""
                SELECT username, content, timestamp
                FROM chat_messages
                WHERE room_id = :room_id AND timestamp < :before_timestamp
                ORDER BY timestamp DESC
                LIMIT 20
            """)
            messages = db.execute(query, {"room_id": room_id, "before_timestamp": before_dt}).fetchall()
        else:
            query = text("""
                SELECT username, content, timestamp
                FROM chat_messages
                WHERE room_id = :room_id
                ORDER BY timestamp DESC
                LIMIT 20
            """)
            messages = db.execute(query, {"room_id": room_id}).fetchall()

        # Send messages oldest first
        for msg in reversed(messages):
            await websocket.send_json({
                "username": msg.username,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            })

        # Receive and store new messages
        while True:
            data = await websocket.receive_json()
            content = data.get("content")
            if not content:
                continue

            timestamp = datetime.utcnow()

            db.execute(
                text("""
                    INSERT INTO chat_messages (username, content, room_id, timestamp)
                    VALUES (:username, :content, :room_id, :timestamp)
                """),
                {
                    "username": username,
                    "content": content,
                    "room_id": room_id,
                    "timestamp": timestamp
                }
            )
            db.commit()

            # Broadcast new message to all clients in room
            await manager.broadcast(room_id, {
                "username": username,
                "content": content,
                "timestamp": timestamp.isoformat()
            })

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    except Exception as e:
        print(f"⚠️ Exception in websocket_endpoint: {e}")
        traceback.print_exc()
        await websocket.close(code=1011)
        manager.disconnect(room_id, websocket)
