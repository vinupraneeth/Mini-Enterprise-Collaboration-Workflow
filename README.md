# Mini Enterprise Collaboration Workflow

Mini Enterprise Collaboration Workflow is a full-stack application for managing internal tasks, approvals, comments, documents, and workflow updates. It is built with FastAPI, React, MySQL, and Tailwind CSS.

The project was developed in phases. The first phase focused on authentication, roles, and task management. Later phases added Kanban workflow tracking, comments, approvals, dashboard analytics, document versioning, notifications, audit logs, and activity tracking.

## Features

- User registration and login using JWT authentication
- Role-based access for Admin, Manager, and Employee users
- Task creation, assignment, editing, deletion, and role-based visibility
- Kanban workflow using `todo`, `in_progress`, `review`, and `done`
- Backend validation for allowed task status transitions
- Task status history for tracking workflow changes
- Public comments and internal notes on tasks
- Manager and Admin approval workflow with conditional admin escalation
- General approval requests for items like laptop, leave, or purchase requests
- Employees and Managers can raise general requests; Admin reviews them directly
- Approval history with action, comment, reviewer, and status details
- Dashboard summary, task distribution, analytics, and AI-style summary
- Document upload, download, and version tracking for tasks
- User notifications for task, document, and approval updates
- Audit logs for important workflow actions
- Role-based activity feed
- Paginated listing APIs using `fastapi_pagination`

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- MySQL
- fastapi-pagination
- JWT authentication

Frontend:
- React
- Vite
- Tailwind CSS
- Axios
- React Router DOM
- @hello-pangea/dnd

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

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder. The required variables are shown in:

```text
backend/.env.example
```

Run the database migrations:

```bash
alembic upgrade head
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

Swagger UI will be available at:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Main API Groups

- Auth: `/auth/register`, `/auth/login`, `/auth/me`
- Users: `/users/`, `/users/employees`, `/users/{id}`
- Tasks: `/tasks/`, `/tasks/kanban`, `/tasks/{id}/status`, `/tasks/{id}/status-history`
- Comments: `/tasks/{id}/comments`
- Approvals: `/approvals/`, `/approvals/{id}/action`, `/approvals/{id}/history`
- Dashboard: `/dashboard/summary`, `/dashboard/task-distribution`, `/dashboard/analytics`, `/dashboard/ai-summary`
- Documents: `/documents/upload`, `/documents/task/{task_id}`, `/documents/{document_id}`
- Notifications: `/notifications/`, `/notifications/{id}/read`
- Audit Logs: `/audit-logs/`
- Activity: `/activity/`

## Screenshots

The `Screenshots` folder contains the testing proof for each phase. Screenshots are separated into Backend, Frontend, and MySQL folders.

```text
Screenshots/
|-- Phase 1 Screenshots/
|-- Phase 2 Screenshots/
`-- Phase 3 Screenshots/
```

## Notes

- The `.env` file is not committed.
- Uploaded files are stored locally during development and ignored by git.
- Run `npm run build` inside `frontend` before final submission to confirm the frontend build.
