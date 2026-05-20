# Mini Enterprise Workflow Management System - Backend

## Overview

This project is a backend system developed using FastAPI for managing enterprise workflow tasks with Role-Based Access Control (RBAC).

The application supports:
- User authentication using JWT
- Task management
- Task assignment workflows
- Role-based permissions
- MySQL database integration
- Alembic database migrations

---

# Tech Stack

- FastAPI
- Python
- MySQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Pydantic
- Uvicorn

---

# Project Architecture

The backend follows layered enterprise architecture:

Router → Service → Repository → Database

## Folder Structure

```bash
backend/
│
├── alembic/
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── requirements.txt
├── alembic.ini
└── README.md
```

---

# Features

## Authentication

- User Registration
- User Login
- JWT Token Authentication
- Protected APIs

---

## Role-Based Access Control

### Admin
- Create tasks
- Edit tasks
- Delete tasks
- Assign tasks to anyone
- View all tasks

### Manager
- Create tasks
- Assign tasks only to employees
- Edit own created tasks
- Delete own created tasks
- View own created tasks

### Employee
- View assigned tasks only
- Update task status only

---

# Task Features

- Create Task
- Edit Task
- Delete Task
- Assign Task
- Update Task Status
- Get Single Task
- Get All Tasks

---

# Database

Database used:
- MySQL

ORM:
- SQLAlchemy

Migration Tool:
- Alembic

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login user |
| GET | /auth/me | Get current user |

---

## Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | /tasks | Create task |
| GET | /tasks | Get tasks |
| GET | /tasks/{id} | Get single task |
| PUT | /tasks/{id} | Update task |
| PATCH | /tasks/{id}/status | Update task status |
| PATCH | /tasks/{id}/assign | Assign task |
| DELETE | /tasks/{id} | Delete task |

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-url>
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Database

Create MySQL database:

```sql
CREATE DATABASE workflow_db;
```

---

# Configure Database URL

Update database URL inside:

```bash
alembic.ini
```

Example:

```ini
sqlalchemy.url = mysql+pymysql://root:password@localhost:3306/workflow_db
```

---

# Run Alembic Migration

```bash
alembic upgrade head
```

---

# Start Backend Server

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

Open:

```bash
http://127.0.0.1:8000/docs
```

---

# Security Features

- JWT Authentication
- Password Hashing
- Protected Routes
- RBAC Authorization
- Input Validation

---