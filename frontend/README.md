# Frontend - Mini Enterprise Collaboration Workflow

This folder contains the React frontend for the workflow application. It connects to the FastAPI backend and provides screens for authentication, task management, Kanban tracking, comments, dashboard summaries, and approval review.

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
- Create task form
- Edit task modal
- Task comments
- Approvals page

## Role-Based UI

Admin:
- Can view and manage tasks
- Can review approvals at the final approval level
- Can access dashboard information

Manager:
- Can create and assign tasks
- Can review related manager-level approvals
- Can add public comments and internal notes

Employee:
- Can view assigned tasks
- Can move assigned tasks through allowed workflow stages
- Can add public comments
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

Default URL:

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

The frontend stores the JWT token in local storage after login and uses it for authenticated API requests.
