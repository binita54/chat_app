# 💬 Chat App 

Hi! I'm **Binita Ghale**, and this repository contains my completed tasks for the **Python Internship** at **Brahmabyte Lab**.

---

## 📌 Overview

This is a simple **Chat Application** built using **FastAPI**, **WebSockets**, and **PostgreSQL**. It supports real-time messaging between users in chat rooms and includes JWT-based authentication. The app is structured with clean modular code and follows RESTful practices.

---

## ✅ Tasks Completed

### 🔹 Group A (Mandatory)
1. **User Authentication System**
   - Sign up and login using JWT tokens
   - Passwords hashed for security

2. **Protected WebSocket Chat**
   - Real-time messaging via `/ws/{room_id}` WebSocket route
   - Messages stored in PostgreSQL
   - Pagination support for loading recent messages

3. **Database Integration**
   - ORM: SQLAlchemy
   - Tables: `User`, `Room`, `Message`
   - Proper foreign key relationships established

### 🔸 Group B (Chosen Task)
**Task 1: Real-time WebSocket Chat Application**

- Implemented secure WebSocket chat system
- Messages broadcast to all users in the room
- Connected users can join different rooms by ID

---

## 🛠 Tech Stack

- **Backend:** FastAPI
- **Real-Time:** WebSockets
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (via FastAPI's dependency injection)
- **Language:** Python 3.11+

---
## 📂 Project Structure
```
chat_app/
│
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── models.py                # SQLAlchemy models (User, Room, Message)
│   ├── schemas.py               # Pydantic schemas for request/response
│   ├── database.py              # DB connection and session config
│   ├── auth.py                  # JWT auth utilities (token creation, verification, etc.)
│   ├── dependencies.py          # Dependency utilities (e.g., current_user, DB session)
│   ├── insert_demo_messages.py # Script to insert dummy messages into DB
│   ├── test_send_message.py     # Script to test message sending logic
│   └── routers/
│       ├── user_routes.py       # Routes for user registration and login
│       ├── room.py              # Routes for room creation and listing
│
├── static/
│   └── chat.html                # Frontend UI for basic chat interaction
│
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── __init__.py                 # (Optional) Python package indicator


```
## 🧾 Setup Instructions

## 1.Clone the Repository
```
git clone https://github.com/binita54/chat_app.git
cd chat_app
```

## 2. Create and Activate a Virtual Environment
```
Windows:
python -m venv venv
venv\Scripts\activate
Mac/Linux:
python3 -m venv venv
source venv/bin/activate
```
## 3. Install Required Packages
```
pip install -r requirements.txt
```
## 4. Set Up PostgreSQL Database
```
DATABASE_URL=postgresql://username:password@localhost/chatdb
```
## 5. Run the Application
```
uvicorn app.main:app --reload
This will start your FastAPI app at: http://127.0.0.1:8000
```
## 6. Access the WebSocket Chat
```
To connect to the WebSocket (replace room_id with a real room):
ws://localhost:8000/ws/{room_id}
```
## 📧 Contact
```
Binita Ghale
📩 ghalebinita54@gmail.com
🔗 GitHub: binita54
```
