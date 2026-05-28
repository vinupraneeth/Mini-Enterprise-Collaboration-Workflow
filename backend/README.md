# Mini Enterprise Workflow Management System - Backend

This is the FastAPI backend for the Mini Enterprise Workflow project. It handles authentication, role-based task management, Kanban workflow validation, task comments, approval reviews, status history, and dashboard data.

The backend follows a simple layered structure:

```text
Router -> Service -> Repository -> Database
```

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- MySQL
- Alembic
- JWT authentication
- Python jose
- Passlib / bcrypt

## Main Features

- User registration and login
- Password hashing
- JWT protected APIs
- Role-based access for Admin, Manager, and Employee
- Task create, view, update, assign, and delete
- Role-based task visibility
- Kanban status flow: `todo -> in_progress -> review -> done`
- Backend validation for invalid status transitions
- Task status history
- Public comments and restricted internal notes
- Approval requests with Manager and Admin review levels
- Approval actions: `approve`, `reject`, and `hold`
- Mandatory comment for rejection
- Approval history with action, actor, comment, and timestamp
- Dashboard summary and task distribution APIs

## Roles

Admin:
- Can view and manage all tasks
- Can assign tasks
- Can view all approvals
- Can complete final approval
- Can view dashboard analytics

Manager:
- Can create tasks
- Can assign tasks to employees
- Can manage related tasks
- Can review manager-level approvals for related tasks
- Cannot review another manager's unrelated task approvals

Employee:
- Can view assigned tasks
- Can update assigned task status through the allowed workflow
- Can add public comments
- Cannot create or view internal notes
- Cannot assign or delete tasks

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

Comment request body:

```json
{
  "comment": "Please verify the report before approval.",
  "is_internal": false
}
```

Approvals:

```text
POST  /approvals/
GET   /approvals/
PATCH /approvals/{id}/action
GET   /approvals/{id}/history
```

Create approval request body:

```json
{
  "title": "Approval request for monthly finance report",
  "description": "Please review and approve the completed report.",
  "task_id": 1
}
```

Approval action request body:

```json
{
  "action": "approve",
  "comment": "Manager reviewed and approved for final admin review."
}
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

## Setup

Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Update the database URL in `.env` or `alembic.ini` based on the local MySQL setup.

Run migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Verification Notes

Before submission, test the Phase 2 flow through Swagger:

- Move a task from `todo` to `in_progress` to `review`
- Confirm invalid status jumps are blocked
- Check `/tasks/{id}/status-history`
- Add public and internal comments
- Confirm employees cannot create or view internal notes
- Approve as Manager, then approve as Admin
- Confirm rejection without comment is blocked
- Check `/approvals/{id}/history`
- Check `/dashboard/summary` and `/dashboard/task-distribution`
