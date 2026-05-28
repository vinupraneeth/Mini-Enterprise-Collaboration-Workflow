# Backend - Mini Enterprise Collaboration Workflow

This folder contains the FastAPI backend for the workflow application. It handles authentication, role-based access, task management, Kanban workflow rules, comments, approvals, and dashboard data.

The code is organized in a layered style:

```text
Router -> Service -> Repository -> Database
```

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- MySQL
- python-jose for JWT
- Passlib and bcrypt for password hashing

## Main Modules

Authentication:
- Register users with a role
- Login and receive JWT token
- Get current logged-in user

Users:
- Admin can view all users
- Admin and Manager can fetch employee users for assignment

Tasks:
- Create, list, view, update, assign, and delete tasks
- Admin can access all tasks
- Managers can manage related tasks
- Employees can view and update only assigned tasks

Workflow:
- Supported status flow: `todo -> in_progress -> review -> done`
- Invalid status transitions are blocked
- Status changes are stored in task history

Comments:
- Users can add comments to tasks they can access
- Admin and Manager can add internal notes
- Employee users can only add public comments

Approvals:
- Approval requests move through Manager and Admin review levels
- Supported actions are `approve`, `reject`, and `hold`
- Rejection requires a comment
- Approval actions are saved in approval history
- Managers can review only approvals related to their tasks

Dashboard:
- Summary counts
- Task distribution by status
- Basic analytics endpoint

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the backend folder. Use `.env.example` as a guide:

```text
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/workflow_db
SECRET_KEY=replace_with_a_secure_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run database migrations:

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

## API Reference

Authentication:

```text
POST /auth/register
POST /auth/login
GET  /auth/me
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
GET /dashboard/summary
GET /dashboard/task-distribution
GET /dashboard/analytics
```

## Example Payloads

Comment:

```json
{
  "comment": "Please verify the report before approval.",
  "is_internal": false
}
```

Approval request:

```json
{
  "title": "Approval request for monthly finance report",
  "description": "Please review and approve the completed report.",
  "task_id": 1
}
```

Approval action:

```json
{
  "action": "approve",
  "comment": "Reviewed and approved."
}
```
