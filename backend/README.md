# Backend - Mini Enterprise Collaboration Workflow

This folder contains the FastAPI backend for the Mini Enterprise Collaboration Workflow project. The backend handles authentication, role-based access, tasks, comments, approvals, documents, notifications, audit logs, and dashboard data.

The code follows a simple layered structure:

```text
Router -> Service -> Repository -> Database
```

Routers handle API requests, services contain business logic, repositories handle database operations, and models define the database tables.

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- MySQL
- fastapi-pagination
- python-jose for JWT authentication
- Passlib and bcrypt for password hashing

## Main Modules

Authentication:
- Register users with a selected role
- Login and receive a JWT access token
- Fetch the currently logged-in user

Users:
- Admin can view users
- Admin and Manager can fetch employee users for task assignment

Tasks:
- Create, list, view, update, assign, and delete tasks
- Admin can view all tasks
- Managers can manage tasks related to them
- Employees can view and update only their assigned tasks

Workflow:
- Main task flow is `todo -> in_progress -> review -> done`
- Invalid status changes are blocked from the backend
- Status changes are stored in task history
- Final movement to `done` happens through approval

Comments:
- Users can add comments to tasks they can access
- Admin and Manager can add internal notes
- Employees can add only public comments
- Internal notes are not shown to employees

Approvals:
- Tasks submitted for review create approval requests
- Manager reviews first, then Admin gives final approval
- Supported actions are `approve`, `reject`, and `hold`
- Rejection requires a comment
- Approval actions are saved in approval history

Documents:
- Upload documents against tasks
- Keep document versions for the same task
- Download documents with authentication and access checks

Notifications:
- Store user-specific workflow notifications
- Mark notifications as read
- Employees do not receive internal note notifications

Audit Logs and Activity:
- Audit logs record important backend actions
- Audit logs are available to Admin users
- Activity feed is filtered based on the logged-in user's role

Dashboard:
- Summary counts
- Task distribution by status
- Basic analytics
- AI-style workflow summary

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

Create a `.env` file in the backend folder. Use `.env.example` as the reference:

```text
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/workflow_db
SECRET_KEY=replace_with_a_secure_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

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
GET /dashboard/ai-summary
```

Documents:

```text
POST /documents/upload
GET  /documents/task/{task_id}
GET  /documents/{document_id}
```

Notifications:

```text
GET   /notifications/
PATCH /notifications/{id}/read
```

Audit Logs and Activity:

```text
GET /audit-logs/
GET /activity/
```

## Example Payloads

Comment:

```json
{
  "comment": "Please verify the report before approval.",
  "is_internal": false
}
```

Approval action:

```json
{
  "action": "approve",
  "comment": "Reviewed and approved."
}
```

Document upload is handled as multipart form data from Swagger or from the frontend document modal.
