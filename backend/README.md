# Backend - Mini Enterprise Collaboration Workflow

This folder contains the FastAPI backend for the Mini Enterprise Collaboration Workflow project. The backend handles authentication, role-based access, tasks, comments, approvals, documents, notifications, audit logs, dashboard data, real-time updates, intelligent insights, SaaS subscriptions, credits, Razorpay billing, Phase 8 workflow governance, and the Phase 10A tenant-aware workspace/channel foundation.

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
- Audit logs are available to Admin and Auditor users
- Audit logs support module, user, date range, and detail views
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

Tenant and Collaboration Foundation:
- Platform Admin can create, update, list, view, suspend, and activate tenants
- Tenant slug is generated automatically and checked for uniqueness
- Tenant contact email and slug duplication are blocked
- Tenant onboarding can create the first tenant admin and default collaboration setup
- Collaboration settings control workspace, channel, member, and storage limits per tenant
- Collaboration usage tracks workspace count, channel count, member count, and storage usage
- Workspaces are scoped to the current user's tenant and support public/private visibility
- Workspace members have Workspace Admin, Moderator, Member, and Viewer roles
- Channels are created inside workspaces and support PUBLIC, PRIVATE, ANNOUNCEMENT, and PROJECT types
- Cross-tenant workspace, member, and channel access is blocked from the service layer

Workflow Governance:
- Admin can manage SLA rules for tasks and approvals
- SLA tracking records active, breached, and completed workflow items
- Tasks and approvals store SLA status and due time
- Managers can escalate valid manager-level approvals to Admin
- Admin and Manager users can manage approval delegations within allowed roles
- Users can manage notification preferences
- Auditor users can view audit logs, SLA tracking, and escalation records in read-only mode

Error Handling:
- Services and routers use `HTTPException` for application errors such as not found, unauthorized access, invalid workflow actions, and validation failures
- Database commits use a shared helper that rolls back on SQLAlchemy errors and returns clean API errors for constraint or database failures

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

Phase 10A uses MySQL through Docker for the local demo database. Start it from the project root:

```bash
docker compose up -d mysql
```

Example database URL for the included Docker MySQL service:

```text
DATABASE_URL=mysql+pymysql://workflow_user:workflow_password@localhost:3307/workflow_db
```

MySQL Workbench can connect to the Docker database with:

```text
Host: 127.0.0.1
Port: 3307
User: workflow_user
Password: workflow_password
Default schema: workflow_db
```

Docker health checks:

```bash
docker compose ps
docker exec mecw_mysql mysqladmin ping -h localhost -uworkflow_user -pworkflow_password
```

The Docker service uses host port `3307` so it can run next to an existing local MySQL service on `3306`.

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
GET /audit-logs/module/{module_name}
GET /audit-logs/user/{user_id}
GET /audit-logs/date-range
GET /audit-logs/{log_id}
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

Tenant Management:

```text
POST  /tenants/
GET   /tenants/
GET   /tenants/{tenant_id}
PUT   /tenants/{tenant_id}
PATCH /tenants/{tenant_id}/suspend
PATCH /tenants/{tenant_id}/activate
POST  /tenants/onboard
POST  /tenants/{tenant_id}/admin
GET   /tenants/{tenant_id}/onboarding-status
```

Tenant Collaboration Settings and Usage:

```text
GET  /tenants/{tenant_id}/collaboration/settings
PUT  /tenants/{tenant_id}/collaboration/settings
GET  /tenants/{tenant_id}/collaboration/usage
POST /tenants/{tenant_id}/collaboration/recalculate-usage
```

Workspaces:

```text
POST  /workspaces/
GET   /workspaces/
GET   /workspaces/{workspace_id}
PUT   /workspaces/{workspace_id}
PATCH /workspaces/{workspace_id}/archive
PATCH /workspaces/{workspace_id}/restore
```

Workspace Members:

```text
POST   /workspaces/{workspace_id}/members
GET    /workspaces/{workspace_id}/members
PATCH  /workspaces/{workspace_id}/members/{user_id}/role
DELETE /workspaces/{workspace_id}/members/{user_id}
```

Channels:

```text
POST  /channels
GET   /workspaces/{workspace_id}/channels
GET   /channels/{channel_id}
PUT   /channels/{channel_id}
PATCH /channels/{channel_id}/archive
PATCH /channels/{channel_id}/restore
POST  /channels/{channel_id}/join
POST  /channels/{channel_id}/leave
```

Workflow Governance:

```text
POST   /sla-rules/
GET    /sla-rules/
GET    /sla-rules/{id}
PUT    /sla-rules/{id}
DELETE /sla-rules/{id}

POST /sla-tracking/tasks/{task_id}
POST /sla-tracking/approvals/{approval_id}
PUT  /sla-tracking/{tracking_id}/complete
GET  /sla-tracking/active
GET  /sla-tracking/breached
GET  /sla-tracking/completed
GET  /sla-tracking/module/{module_name}
GET  /sla-tracking/record/{module_name}/{record_id}

POST /approval-escalations/
GET  /approval-escalations/
GET  /approval-escalations/pending
GET  /approval-escalations/approval/{approval_id}
PUT  /approval-escalations/{escalation_id}/resolve
PUT  /approval-escalations/{escalation_id}/cancel

POST /approval-delegations/
GET  /approval-delegations/me
GET  /approval-delegations/active
PUT  /approval-delegations/{delegation_id}/cancel

GET /notification-preferences/me
PUT /notification-preferences/me
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

General approval request:

```json
{
  "title": "Laptop request",
  "description": "Need a laptop for project work.",
  "task_id": null
}
```

Tenant onboarding:

```json
{
  "name": "Nexora Technologies Pvt Ltd",
  "slug": "nexora-technologies",
  "contact_email": "operations@nexoratech.example.com",
  "phone": "9876543210",
  "address": "Chennai, Tamil Nadu",
  "industry": "Information Technology",
  "admin_name": "Rohan Mehta",
  "admin_email": "rohan.mehta@nexoratech.example.com",
  "admin_password": "Tenant@12345",
  "create_default_workspace": true
}
```

Collaboration settings:

```json
{
  "max_workspaces": 5,
  "max_channels_per_workspace": 10,
  "max_workspace_members": 50,
  "max_storage_mb": 1024,
  "workspace_enabled": true,
  "channel_enabled": true
}
```

Workspace:

```json
{
  "name": "Finance Team",
  "description": "Workspace for finance approvals and monthly reviews.",
  "visibility": "PUBLIC"
}
```

Workspace member:

```json
{
  "user_id": 4,
  "role": "MEMBER"
}
```

Channel:

```json
{
  "workspace_id": 1,
  "name": "Budget Planning",
  "description": "Discussion channel for budget planning work.",
  "channel_type": "PUBLIC"
}
```

Document upload is handled as multipart form data from Swagger or from the frontend document modal.

## Phase 10A Demo Notes

For the clean demo database, the original users remain as IDs 1 to 9 and the Phase 10A tenant/workspace/channel tables start empty. This keeps the demo flow clear: create or onboard a tenant from Swagger, log in as the tenant admin if needed, then create workspaces, add members, and create channels.

The local and Docker databases were kept aligned for the final demo. Use Docker MySQL on `localhost:3307` when showing the deliverable because the Phase 10A mail specifically asks for MySQL running through Docker.
