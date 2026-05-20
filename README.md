# Mini Enterprise Workflow Management System

## Overview

Mini Enterprise Workflow Management System is a full-stack enterprise task management application developed using FastAPI, React, MySQL, and Tailwind CSS.

The system provides secure role-based workflow management where Admins, Managers, and Employees have different levels of access and responsibilities.

---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- MySQL
- Alembic
- JWT Authentication
- Pydantic

## Frontend
- React
- Vite
- Tailwind CSS
- Axios
- React Router DOM

---

# Features

## Authentication
- User Registration
- User Login
- JWT Authentication
- Protected Routes

---

# Role-Based Access Control

## Admin
- Full system access
- Manage all tasks
- Assign tasks
- Edit/Delete tasks

## Manager
- Create tasks
- Assign tasks to employees
- Manage own created tasks

## Employee
- View assigned tasks
- Update task status

---

# Task Management

- Create Task
- Edit Task
- Delete Task
- Assign Task
- Update Task Status
- View Single Task
- View All Tasks

---

# Architecture

Backend follows enterprise layered architecture:

```text
Router → Service → Repository → Database
```

---

# Database

- MySQL Database
- SQLAlchemy ORM
- Alembic Migrations

---

# Frontend Features

- Responsive Dashboard
- Task Statistics Cards
- Edit Task Modal
- Modern Tailwind UI
- Protected Frontend Routing
- Empty State UI

---

# Project Structure

```bash
mini-enterprise-workflow/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── README.md
│
└── README.md
```

---

# Setup Instructions

## Backend Setup

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Start backend:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```bash
http://127.0.0.1:8000
```

Swagger Docs:

```bash
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start frontend:

```bash
npm run dev
```

Frontend URL:

```bash
http://localhost:5173
```

---

# Security Features

- JWT Authentication
- Password Hashing
- RBAC Authorization
- Protected APIs
- Input Validation

---

# Future Improvements

- Search & Filtering
- Pagination
- Notifications
- Docker Deployment
- Unit Testing
- Email Notifications

---
