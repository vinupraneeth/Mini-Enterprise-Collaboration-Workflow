# Mini Enterprise Workflow Management System - Frontend

## Overview

This project is the frontend application for the Enterprise Workflow Management System.

Built using React and Tailwind CSS, the application provides a modern responsive dashboard for managing enterprise workflow tasks with role-based access control.

---

# Tech Stack

- React
- Vite
- Tailwind CSS
- Axios
- React Router DOM

---

# Features

## Authentication

- User Login
- User Registration
- JWT Token Handling
- Protected Routes

---

## Dashboard

- Modern responsive UI
- Task statistics cards
- Task management interface
- Empty state handling

---

## Task Management

- Create Task
- Edit Task
- Delete Task
- Update Task Status
- Role-Based UI Access

---

# Role-Based Access

## Admin
- Full task management access

## Manager
- Create and assign tasks to employees

## Employee
- View assigned tasks
- Update task status

---

# UI Features

- Responsive Design
- Tailwind CSS Styling
- Gradient Theme
- Modal-based Editing
- Interactive Dashboard Cards

---

# Folder Structure

```bash
frontend/
│
├── src/
│   ├── api/
│   ├── components/
│   ├── pages/
│   ├── routes/
│   └── App.jsx
│
├── public/
├── package.json
└── README.md
```

---

# Setup Instructions

## Install Dependencies

```bash
npm install
```

---

# Start Frontend Server

```bash
npm run dev
```

---

# Frontend URL

```bash
http://localhost:5173
```

---

# Backend Requirement

Backend server must be running before starting frontend.

Backend API:

```bash
http://127.0.0.1:8000
```

---