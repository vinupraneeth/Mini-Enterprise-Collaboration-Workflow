# Backend - Mini Enterprise Collaboration Workflow

This folder contains the FastAPI backend for the Mini Enterprise Collaboration Workflow project. The backend handles authentication, role-based access, tasks, comments, approvals, documents, notifications, audit logs, dashboard data, real-time updates, intelligent insights, SaaS subscriptions, credits, and Razorpay billing.

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
- Redis
- Razorpay SDK
- WebSockets
- python-jose for JWT authentication
- Passlib and bcrypt for password hashing

## Main Modules

Authentication:
- Register users with a selected role
- Login and receive a JWT access token
- Refresh access tokens using refresh tokens
- Request and confirm token-based password reset
- Use Google OAuth when OAuth credentials are configured
- Fetch the currently logged-in user
- Rate limiting is applied to sensitive authentication endpoints

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
- Manager reviews first, then Admin gives final approval when required
- High priority task approvals are escalated to Admin after Manager approval
- General approval requests can be raised without linking to a task
- General approval requests are sent directly to Admin
- Admin users review approval requests instead of raising them
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
- Role-specific dashboard view
- Smart assignment recommendation
- Delay-risk task detection

Real-time Updates:
- WebSocket endpoint sends live notification events
- Kanban updates refresh related users when task state changes

SaaS:
- Organization model for multi-tenant isolation
- Paid Basic, Silver, and Gold subscription plans
- Credit ledger for usage credits
- Billing transaction records
- Razorpay order creation and signature verification

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
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES=30
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
FRONTEND_URL=http://localhost:5173
REDIS_URL=redis://localhost:6379/0
CACHE_DEFAULT_TTL_SECONDS=300
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
```

For Razorpay local testing, use Razorpay test mode keys:

```text
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxx
```

After changing `.env`, restart the backend server.

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
POST /auth/refresh
POST /auth/password-reset/request
POST /auth/password-reset/confirm
GET  /auth/google/status
GET  /auth/google
GET  /auth/google/callback
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
GET /dashboard/role-view
GET /dashboard/smart-assignment
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

SaaS and Payments:

```text
GET   /saas/organizations
POST  /saas/organizations
GET   /saas/organization
GET   /saas/plans
GET   /saas/subscription
GET   /saas/credits
GET   /saas/billing/transactions
POST  /payments/create-payment
POST  /payments/verify-razorpay
```

All paid subscription plans are activated through Razorpay payment verification. The backend creates a Razorpay order, the frontend opens Razorpay Checkout, and the backend verifies the returned Razorpay signature before updating the subscription and credits.

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

General approval request:

```json
{
  "title": "Laptop request",
  "description": "Need a laptop for project work.",
  "task_id": null
}
```

Document upload is handled as multipart form data from Swagger or from the frontend document modal.
