# TruthTalk Backend – Real-Time Voice Room API

## 📌 Overview

TruthTalk Backend is a FastAPI-based REST API that powers a real-time voice communication platform.

It handles authentication, room management, user administration, and real-time voice token generation using Agora RTC.

The system is designed with scalability, security, and role-based access control (user / admin).

---

## ⚙️ Tech Stack

- FastAPI
- SQLAlchemy
- MySQL (PyMySQL)
- JWT Authentication (python-jose)
- Passlib (bcrypt)
- Pydantic
- Agora RTC Token Builder
- Uvicorn

---

## 🏗️ Project Architecture

Core structure:

- auth → user registration & login
- rooms → create, join, leave, manage rooms
- admin → user & room administration
- core → security, dependencies, configuration
- models → database models (User, Room, Participant)
- schemas → request/response validation
- services → Agora token service

---

## 🔐 Authentication System

- JWT-based authentication
- Password hashing with bcrypt
- Token validation middleware
- Protected routes using dependencies

Features:
- Register new user
- Login user
- Secure token generation
- Current user dependency injection

---

## 🎙️ Room System

- Create voice rooms
- Join / leave rooms
- Public & private rooms
- Language-based room grouping
- Max participant control

Room Features:
- Auto generate unique Agora channel
- Auto delete room when empty
- Creator-based permissions

---

## 👥 Room Management

- Kick users from room
- Mute / unmute users
- Close room (creator only)
- Participant tracking system

---

## 🛡️ Admin System

Admin-only features:

- View platform statistics
  - total users
  - total rooms
  - active rooms
  - banned users

- User management:
  - ban user
  - unban user

- Room management:
  - force close room
  - kick users from any room

---

## 🔑 Security Layer

- JWT token verification
- Role-based access control (RBAC)
- Admin-only dependencies
- Banned user restriction
- Protected endpoints

---

## 🎧 Agora Integration

- Real-time voice communication support
- Dynamic channel generation per room
- Secure token generation
- UID-based participant identity

---

## 📡 API Endpoints

### Auth
- POST `/auth/register`
- POST `/auth/login`

### Rooms
- GET `/rooms`
- GET `/rooms/{room_id}`
- POST `/rooms`
- POST `/rooms/{room_id}/join`
- POST `/rooms/{room_id}/leave`
- POST `/rooms/{room_id}/kick/{user_id}`
- POST `/rooms/{room_id}/close`
- GET `/rooms/{room_id}/token`

### Admin
- GET `/admin/stats`
- GET `/admin/users`
- POST `/admin/users/{user_id}/ban`
- POST `/admin/users/{user_id}/unban`
- GET `/admin/rooms`
- POST `/admin/rooms/{room_id}/close`

---

## 🗄️ Database Models

- User
  - id, username, email, password
  - is_admin, is_banned, is_verified

- Room
  - id, title, topic, language
  - max_participants, status
  - agora_channel_name

- Participant
  - user_id, room_id
  - is_muted, is_banned

---

## 🚀 Features Summary

- JWT authentication system
- Role-based access control (Admin/User)
- Real-time voice room backend
- Agora RTC integration
- Scalable modular architecture
- Secure API design
- Full room lifecycle management

---

## 🚀 Future Improvements

- WebSocket real-time updates
- Chat system inside rooms
- Notifications system
- Docker deployment
- CI/CD pipeline
- Microservice separation

---

## 👨‍💻 Author

Full-Stack Backend Project  
Built with FastAPI + SQLAlchemy + Agora RTC
