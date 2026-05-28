# Mini Enterprise Collaboration Workflow

A full-stack workflow management application built with FastAPI, React, MySQL, and Tailwind CSS.

The project started as a role-based task management system and was extended with workflow features such as Kanban tracking, comments, approval reviews, task history, and dashboard summaries.

## Features

- User registration and login with JWT authentication
- Role-based access for Admin, Manager, and Employee users
- Task creation, assignment, editing, deletion, and role-based task visibility
- Kanban workflow with the stages `todo`, `in_progress`, `review`, and `done`
- Backend validation to prevent invalid workflow transitions
- Task status history
- Public comments and internal notes on tasks
- Approval workflow with Manager review and Admin final approval
- Approval history with action, user, comment, and timestamp
- Dashboard summary and task distribution APIs
- React frontend connected with the FastAPI backend

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- MySQL
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

Create a `.env` file in the `backend` folder. A sample is available at:

```text
backend/.env.example
```

Run migrations and start the API:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Swagger UI:

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
- Dashboard: `/dashboard/summary`, `/dashboard/task-distribution`, `/dashboard/analytics`

## Screenshots

The `Screenshots` folder is organized by phase and includes backend Swagger tests, frontend screens, and MySQL verification screenshots.

```text
Screenshots/
|-- Phase 1 Screenshots/
`-- Phase 2 Screenshots/
```

## Notes

- The `.env` file is not committed.
- Use `backend/.env.example` as the reference for required environment variables.
- Run `npm run build` inside `frontend` to verify the React build.
