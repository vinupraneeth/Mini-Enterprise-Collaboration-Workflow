# Mini Enterprise Collaboration Workflow

Mini Enterprise Collaboration Workflow is a full-stack application for managing internal tasks, approvals, comments, documents, and workflow updates. It is built with FastAPI, React, MySQL, and Tailwind CSS.

The project was developed in phases. The first phase focused on authentication, roles, and task management. Later phases added Kanban workflow tracking, comments, approvals, dashboard analytics, document versioning, notifications, audit logs, activity tracking, advanced authentication, WebSockets, intelligent task insights, multi-tenant SaaS support, subscription plans, credits, and Razorpay billing integration.

## Features

- User registration and login using JWT authentication
- JWT refresh token flow for renewing access tokens
- Token-based password reset with secure token storage
- Google OAuth login support when OAuth credentials are configured
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
- Reusable role permission dependencies
- API rate limiting middleware
- Input validation and sanitization
- Redis-based dashboard caching with in-memory fallback
- Database query indexes for dashboard and workflow-heavy tables
- WebSocket notifications and live Kanban refresh events
- Role-based dashboard views for Employee, Manager, and Admin
- Smart task insights with high-priority, delayed, and delay-risk signals
- Smart assignment recommendation based on workload and completed-task history
- Multi-tenant organization model
- Basic, Silver, and Gold subscription plans
- Credit ledger and billing transaction tracking
- Razorpay checkout integration with backend signature verification

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- MySQL
- fastapi-pagination
- Redis
- Razorpay SDK
- WebSockets
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
- Auth Phase 4: `/auth/refresh`, `/auth/password-reset/request`, `/auth/password-reset/confirm`, `/auth/google`, `/auth/google/callback`
- Users: `/users/`, `/users/employees`, `/users/{id}`
- Tasks: `/tasks/`, `/tasks/kanban`, `/tasks/{id}/status`, `/tasks/{id}/status-history`
- Comments: `/tasks/{id}/comments`
- Approvals: `/approvals/`, `/approvals/{id}/action`, `/approvals/{id}/history`
- Dashboard: `/dashboard/summary`, `/dashboard/task-distribution`, `/dashboard/analytics`, `/dashboard/ai-summary`
- Intelligent Dashboard: `/dashboard/role-view`, `/dashboard/smart-assignment`
- Documents: `/documents/upload`, `/documents/task/{task_id}`, `/documents/{document_id}`
- Notifications: `/notifications/`, `/notifications/{id}/read`
- Audit Logs: `/audit-logs/`
- Activity: `/activity/`
- SaaS: `/saas/organizations`, `/saas/plans`, `/saas/subscription`, `/saas/credits`
- Payments: `/payments/create-payment`, `/payments/verify-razorpay`

## Screenshots

The `Screenshots` folder contains the testing proof for each phase. Screenshots are separated into Backend, Frontend, and MySQL folders.

```text
Screenshots/
|-- Phase 1 Screenshots/
|-- Phase 2 Screenshots/
|-- Phase 3 Screenshots/
`-- Phase 4 to 7 Screenshots/
```

## Notes

- The `.env` file is not committed.
- Google OAuth requires `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, and `FRONTEND_URL` in `backend/.env`.
- Razorpay checkout requires `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in `backend/.env`. Use Razorpay test mode keys for development and local testing.
- Subscription tiers are paid plans:
  - Basic: Rs 499/month, 300 credits, up to 10 users
  - Silver: Rs 1499/month, 1000 credits, up to 50 users
  - Gold: Rs 3999/month, 3000 credits, up to 200 users
- Password reset uses secure reset tokens. In local development, the token is displayed for testing; in production, the same token should be delivered by email.
- Redis caching is optional. If Redis is not running, the backend uses an in-memory cache fallback.
- Uploaded files are stored locally during development and ignored by git.
- Run `npm run build` inside `frontend` before final submission to confirm the frontend build.
