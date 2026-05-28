# Mini Enterprise Workflow Management System

## Overview

Mini Enterprise Workflow Management System is a full-stack workflow application built with FastAPI, React, MySQL, and Tailwind CSS.

The application supports secure role-based task management for Admin, Manager, and Employee users. Phase 2 extends the basic task system with Kanban workflow tracking, comments, approvals, activity/history records, and dashboard analytics.

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- MySQL
- Alembic
- JWT authentication
- Pydantic
- Passlib / bcrypt

Frontend:
- React
- Vite
- Tailwind CSS
- Axios
- React Router DOM
- @hello-pangea/dnd

## Main Features

Authentication:
- User registration with role
- Login with JWT token
- Current logged-in user API
- Protected frontend routes

Role-based access:
- Admin can manage all users, tasks, approvals, and workflow data
- Manager can create tasks, assign tasks to employees, and manage related workflow approvals
- Employee can view assigned tasks, update task status through the allowed workflow, add public comments, and submit approval requests

Task management:
- Create, view, edit, delete, and assign tasks
- Role-based task filtering
- Priority and due date support
- MySQL persistence with Alembic migrations

Phase 2 workflow:
- Kanban stages: `todo -> in_progress -> review -> done`
- Backend validation for invalid status transitions
- Task status history tracking
- Public comments and restricted internal notes
- Approval workflow with Manager review and Admin final approval
- Approval actions: `approve`, `reject`, and `hold`
- Mandatory comment for rejection
- Approval audit history
- Dashboard summary and task distribution APIs

## Important APIs

Authentication:

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

Users:

```text
GET /users/
GET /users/employees
GET /users/{id}
```

Tasks:

```text
POST   /tasks/
GET    /tasks/
GET    /tasks/kanban
GET    /tasks/{id}
PUT    /tasks/{id}
PATCH  /tasks/{id}/status
GET    /tasks/{id}/status-history
PATCH  /tasks/{id}/assign
DELETE /tasks/{id}
```

Comments:

```text
POST /tasks/{id}/comments
GET  /tasks/{id}/comments
```

Approvals:

```text
POST  /approvals/
GET   /approvals/
PATCH /approvals/{id}/action
GET   /approvals/{id}/history
```

Dashboard:

```text
GET /dashboard/analytics
GET /dashboard/summary
GET /dashboard/task-distribution
```

Activity:

```text
GET /activity/
```

## Project Structure

```text
mini-enterprise-workflow/
|-- backend/
|   |-- alembic/
|   |-- app/
|   |-- requirements.txt
|   `-- README.md
|-- frontend/
|   |-- src/
|   |-- package.json
|   `-- README.md
|-- Screenshots/
`-- README.md
```

## Setup Instructions

Backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Submission Notes

The `Screenshots` folder contains proof for Swagger/API testing, frontend screens, and MySQL verification. Phase 2 screenshots cover Kanban workflow, status history, comments, approvals, approval history, dashboard APIs, and database records.

## Future Improvements

- Search and filtering
- Pagination
- Notifications
- Docker deployment
- Automated test coverage
- Email notifications
