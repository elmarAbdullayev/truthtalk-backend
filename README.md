# 🧠 TruthTalk Backend

A scalable backend system for a real-time social communication platform with rooms, moderation, authentication, and role-based access control.

Built with FastAPI, SQLAlchemy, and JWT authentication, the system supports real-time room creation, user participation, and administrative moderation features such as banning, muting, and kicking users.

---

## 🚀 Features

### 🔐 Authentication & Security
- JWT-based authentication (OAuth2 flow)
- Password hashing with bcrypt
- Role-based access control (User / Admin)
- Optional guest access support
- Secure token validation middleware

---

### 🏠 Room System
- Create public/private rooms
- Join and leave rooms dynamically
- Auto room deletion when empty
- Room status management (active / closed)
- Participant tracking per room

---

### 🎤 Real-Time Ready Architecture
- Agora RTC integration for voice/video channels
- Unique channel generation per room
- Token-based secure Agora authentication
- Random UID generation for participants

---

### 🛡️ Moderation System
- Ban / Unban users (Admin-only)
- Kick users from rooms (Admin / Creator)
- Mute / Unmute participants
- Automatic participant cleanup on ban/kick

---

### 👑 Admin Panel APIs
- Platform statistics (users, rooms, active rooms)
- Full user management (ban/unban)
- Room management (close/kick users)
- System-wide moderation controls

---

## 🏗️ Tech Stack

- **Backend:** FastAPI
- **Database:** SQLAlchemy + MySQL
- **Auth:** JWT (python-jose)
- **Security:** bcrypt (passlib)
- **Realtime Integration:** Agora RTC
- **Validation:** Pydantic
- **Architecture:** Dependency Injection (FastAPI pattern)

---

## 📁 Project Structure
app/
├── core/
│ ├── database.py
│ ├── dependencies.py
│ ├── security.py
│ └── config.py
│
├── models/
│ ├── user.py
│ ├── room.py
│ └── participant.py
│
├── routes/
│ ├── auth.py
│ ├── rooms.py
│ └── admin.py
│
├── schemas/
│ ├── user.py
│ ├── room.py
│ └── admin.py
│
└── services/
└── agora_service.py



---

## ⚙️ Key System Design Concepts

### 🔄 State Management
- Rooms transition between `ACTIVE` and `CLOSED`
- Participants tracked with join/leave lifecycle
- Automatic cleanup when rooms become empty

---

### 🧠 Access Control Logic
- Admin-only endpoints protected via dependency injection
- Room creator permissions separated from admin permissions
- Optional authentication for public endpoints

---

### 📡 Real-Time Architecture (Agora)
- Each room generates a unique Agora channel
- Secure token generation per user session
- Random UID assignment for collision safety

---

## 🔥 API Highlights

### Authentication

POST /auth/register
POST /auth/login

### Rooms

POST /rooms/ # create room
GET /rooms/ # list rooms
POST /rooms/{id}/join # join room
POST /rooms/{id}/leave # leave room
POST /rooms/{id}/kick # kick user
POST /rooms/{id}/mute # mute user


### Admin

GET /admin/stats
GET /admin/users
POST /admin/users/{id}/ban
POST /admin/users/{id}/unban
GET /admin/rooms
POST /admin/rooms/{id}/close


---

## 💡 Key Learnings

- Designing real-time backend systems
- Role-based access control at scale
- Building moderation systems (ban/mute/kick flows)
- Managing relational state between users and rooms
- Integrating third-party RTC services (Agora)
- Structuring production-ready FastAPI applications

---

## 🚀 Why this project matters

This project simulates a real-world backend system similar to:
- Discord (rooms + voice channels)
- Clubhouse (real-time rooms)
- Slack (user + room interaction systems)

It demonstrates:
- System design thinking
- Backend architecture skills
- Security awareness
- Real-time system integration

---

## 📌 Status

✔ Backend completed  
✔ Authentication system implemented  
✔ Admin moderation system implemented  
✔ Agora integration completed  

---

## 👤 Author

Built as part of a personal full-stack portfolio focused on:
- Backend engineering
- System design
- Real-time applications
