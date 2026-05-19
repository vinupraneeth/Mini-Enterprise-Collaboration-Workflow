# Workflow Management System API

## Tech Stack
- FastAPI
- MySQL
- SQLAlchemy
- JWT Authentication

## Features
- User Authentication
- Role-Based Access Control
- Task Assignment
- Task Status Updates
- Protected APIs

## Roles
- Admin
- Manager
- Employee

## Setup

```bash
pip install -r requirements.txt
```

Create `.env`

Run server:

```bash
uvicorn app.main:app --reload
```