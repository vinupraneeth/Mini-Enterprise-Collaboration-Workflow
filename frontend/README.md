# Frontend - Mini Enterprise Collaboration Workflow

This folder contains the React frontend for the Mini Enterprise Collaboration Workflow project. It connects with the FastAPI backend and provides the screens used for login, task management, Kanban workflow, approvals, comments, documents, notifications, audit logs, dashboard updates, intelligent insights, and subscription management.

## Tech Stack

- React
- Vite
- Tailwind CSS
- Axios
- React Router DOM
- @hello-pangea/dnd

## Screens

- Login
- Registration
- Dashboard
- Kanban task board
- Create task modal
- Edit task modal
- Task comments
- Approvals page
- General approval request form
- My requests and approval records view
- Task documents modal
- Notifications panel
- Activity feed panel
- AI summary panel
- Role dashboard panel
- Smart assignment panel
- Admin audit logs page
- Admin subscription page
- Razorpay checkout flow for paid plans

## Role-Based UI

Admin:
- Can view all tasks
- Can review final approval requests
- Cannot create general approval requests
- Can view dashboard information
- Can open audit logs
- Can see wider workflow activity
- Can open the Subscription page
- Can choose Basic, Silver, or Gold plans through Razorpay checkout

Manager:
- Can create and assign tasks to employees
- Can manage tasks related to them
- Can review manager-level approval requests
- Can raise general approval requests
- Can add public comments and internal notes
- Can view related documents, notifications, and activity

Employee:
- Can view assigned tasks
- Can update assigned tasks through allowed workflow stages
- Can add public comments
- Can upload and download documents for assigned tasks
- Can view related notifications and activity
- Can raise general approval requests
- Cannot create internal notes or review approvals

## Setup

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Default frontend URL:

```text
http://localhost:5173
```

The backend should be running at:

```text
http://127.0.0.1:8000
```

## Build Check

```bash
npm run build
```

The frontend stores the JWT token in local storage after login and sends it with authenticated API requests.

Document upload and download are handled from the task documents modal. Dashboard panels show summary, notifications, activity, AI insights, role-specific actions, and smart assignment suggestions based on the logged-in user's role.

The Subscription page is available to Admin users from the top navigation. Paid plans open Razorpay Checkout when Razorpay test or live keys are configured in the backend environment.
