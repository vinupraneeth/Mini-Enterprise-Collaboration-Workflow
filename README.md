# Mini Enterprise Collaboration Workflow

Mini Enterprise Collaboration Workflow is a full-stack application for managing internal tasks, approvals, comments, documents, workflow updates, tenant onboarding, and collaboration spaces. It is built with FastAPI, React, MySQL, and Tailwind CSS.

The project was developed in phases. The first phase focused on authentication, roles, and task management. Later phases added Kanban workflow tracking, comments, approvals, dashboard analytics, document versioning, notifications, audit logs, activity tracking, advanced authentication, WebSockets, intelligent task insights, multi-tenant SaaS support, subscription plans, credits, Razorpay billing integration, and workflow governance features such as SLA tracking, approval escalations, delegations, notification preferences, and Auditor access. Phase 10A adds the backend foundation for SaaS tenant onboarding, tenant collaboration limits, tenant workspaces, workspace members, and workspace channels.

## Features

- User registration and login using JWT authentication
- JWT refresh token flow for renewing access tokens
- Token-based password reset with secure token storage
- Google OAuth login support when OAuth credentials are configured
- Role-based access for Admin, Manager, Employee, and Auditor users
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
- SLA rules for task and approval workflows
- SLA tracking for active, breached, and completed workflow records
- SLA status fields on tasks and approvals
- Approval escalation tracking and Manager-to-Admin escalation flow
- Approval delegation between eligible approval users
- User notification preferences
- Enhanced audit log filtering and detail view
- Auditor role with read-only access to audit and governance views
- Platform tenant management with create, update, list, view, suspend, and activate support
- Tenant onboarding with first admin creation and default collaboration setup
- Tenant collaboration settings and usage tracking for workspace, channel, member, and storage limits
- Tenant-scoped workspace management with public/private visibility and archive/restore actions
- Workspace member management with Workspace Admin, Moderator, Member, and Viewer roles
- Workspace channel foundation with public, private, announcement, and project channels
- Docker Compose MySQL service for local development and Phase 10A demo delivery
- Shared database commit exception handling with rollback on database errors

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
|-- docker-compose.yml
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

Start the MySQL database through Docker from the project root:

```bash
docker compose up -d mysql
```

Default Docker database values:

```text
Database: workflow_db
User: workflow_user
Password: workflow_password
Host port: 3307
Container port: 3306
```

Example backend database URL for the included Docker MySQL service:

```text
DATABASE_URL=mysql+pymysql://workflow_user:workflow_password@localhost:3307/workflow_db
```

Useful Docker checks:

```bash
docker compose ps
docker exec mecw_mysql mysqladmin ping -h localhost -uworkflow_user -pworkflow_password
```

MySQL Workbench can connect to the Docker database with:

```text
Host: 127.0.0.1
Port: 3307
User: workflow_user
Password: workflow_password
Default schema: workflow_db
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
- SLA Rules: `/sla-rules/`, `/sla-rules/{id}`
- SLA Tracking: `/sla-tracking/active`, `/sla-tracking/breached`, `/sla-tracking/completed`, `/sla-tracking/record/{module_name}/{record_id}`
- Approval Escalations: `/approval-escalations/`, `/approval-escalations/pending`, `/approval-escalations/{id}/resolve`, `/approval-escalations/{id}/cancel`
- Approval Delegations: `/approval-delegations/`, `/approval-delegations/me`, `/approval-delegations/active`, `/approval-delegations/{id}/cancel`
- Notification Preferences: `/notification-preferences/me`
- Tenants: `/tenants/`, `/tenants/{tenant_id}`, `/tenants/onboard`, `/tenants/{tenant_id}/admin`, `/tenants/{tenant_id}/onboarding-status`
- Tenant Collaboration: `/tenants/{tenant_id}/collaboration/settings`, `/tenants/{tenant_id}/collaboration/usage`, `/tenants/{tenant_id}/collaboration/recalculate-usage`
- Workspaces: `/workspaces/`, `/workspaces/{workspace_id}`, `/workspaces/{workspace_id}/archive`, `/workspaces/{workspace_id}/restore`
- Workspace Members: `/workspaces/{workspace_id}/members`, `/workspaces/{workspace_id}/members/{user_id}/role`
- Channels: `/channels`, `/workspaces/{workspace_id}/channels`, `/channels/{channel_id}`, `/channels/{channel_id}/join`, `/channels/{channel_id}/leave`

## Demo Data

The clean local demo database contains the original project users and baseline workflow data:

```text
Admin:    arjun.admin@example.com / Admin@123
Managers: kavya.manager@example.com, vikram.manager@example.com / Manager@12345
Employees: ananya.employee@example.com, rahul.employee@example.com, meenakshi.employee@example.com, suresh.employee@example.com, lakshmi.employee@example.com / Employee@12345
Auditor:  meera.auditor@example.com / Auditor@12345
```

The Phase 10A collaboration tables are intentionally clean in the demo database. During a demo, create a tenant through Swagger, onboard its first tenant admin, then create workspaces, members, and channels to show the full flow from a clean state.

## Screenshots

The `Screenshots` folder contains the testing proof for each phase. Screenshots are separated into Backend, Frontend, and MySQL folders.

```text
Screenshots/
|-- Phase 1 Screenshots/
|-- Phase 2 Screenshots/
|-- Phase 3 Screenshots/
|-- Phase 4 to 7 Screenshots/
|-- Phase 8 Screenshots/
`-- Phase 10A Screenshots/
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
- Phase 10A is a backend/API foundation phase. Tenant, workspace, member, and channel flows are tested and demonstrated from Swagger.
- Docker MySQL uses port `3307` on the host so it can run beside an existing local MySQL service on port `3306`.
- Run `npm run build` inside `frontend` before final submission to confirm the frontend build.
