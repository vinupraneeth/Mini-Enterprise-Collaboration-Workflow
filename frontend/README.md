# Mini Enterprise Workflow Management System - Frontend

This is the React frontend for the Mini Enterprise Workflow project. It connects to the FastAPI backend and provides screens for login, registration, task dashboard, Kanban tracking, comments, and approval review.

## Tech Stack

- React
- Vite
- Tailwind CSS
- Axios
- React Router DOM
- @hello-pangea/dnd for Kanban drag and drop

## Main Screens

- Login page
- Registration page
- Workflow dashboard
- Kanban task board
- Create task form
- Edit task modal
- Task comments section
- Approval review page

## Features

- JWT token stored after login
- Protected dashboard and approval routes
- Role-based buttons and navigation
- Task statistics cards
- Kanban columns for `todo`, `in_progress`, `review`, and `done`
- Drag and drop status updates
- Public and internal task comments
- Employee view hides internal notes
- Employees are blocked from creating internal notes by the backend
- Approval actions: `approve`, `reject`, and `hold`
- Rejection remarks prompt

## Role-Based UI

Admin:
- Can create, edit, delete, and review approvals
- Can access the approvals page
- Can complete final approval

Manager:
- Can create and assign tasks
- Can review related manager-level approvals
- Can access the approvals page

Employee:
- Can view assigned tasks
- Can update task status through the workflow
- Can add public comments
- Cannot access approval review actions

## Setup

Install dependencies:

```bash
npm install
```

Start frontend:

```bash
npm run dev
```

Default URL:

```text
http://localhost:5173
```

## Backend Requirement

Start the backend first:

```text
http://127.0.0.1:8000
```

The frontend API calls are currently pointed to this backend URL.

## Build Check

To check the frontend before submission:

```bash
npm run build
```

If the build passes and the backend is running, the main workflow can be tested from the browser.

## Submission Screens

For Phase 2 proof, capture the dashboard/Kanban board, comments UI, and approval review page. Swagger screenshots are used for the deeper approval history and role-restriction checks.
