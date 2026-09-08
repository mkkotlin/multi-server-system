# 🛡️ Django API & Security Audit Report

**Service Name**: Django Task Management Service  
**Location**: [`services/Django`](file:///f:/multi-server-system/services/Django)  
**Port**: `8000`  
**Framework**: Django REST Framework + PostgreSQL (`triserver`)  

---

## 1. Executive Summary

The Django service serves as the core authentication authority and domain controller for Users, Projects, and Tasks. It publishes asynchronous state change events to the Node.js Event Server whenever task lifecycle transitions occur (`TASK_CREATED`, `TASK_STATUS_CHANGED`, `TASK_COMPLETED`, `TASK_REOPENED`).

---

## 2. Security & RBAC Enforcements

| User Role | Operations Allowed | Restrictions Enforced |
| :--- | :--- | :--- |
| **ADMIN** | Full access to all projects, tasks, and users | Can create/assign tasks across any project or user |
| **USER** | Access restricted to owned projects and tasks | Cannot view/create tasks in foreign projects; can only assign tasks to self |

### Key Security Implementations:
- **JWT Authentication**: Enforced using `rest_framework_simplejwt`.
- **Project Scoping**: [`perform_create`](file:///f:/multi-server-system/services/Django/tasks/views.py#L21) validates that non-admin users only create tasks in projects where `project.owner_id == request.user.id`.
- **Assignment Validation**: Prevents regular users from assigning tasks to other team members.

---

## 3. API Endpoint Inventory

| Endpoint | Method | Auth | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| `/api/auth/token/` | `POST` | Public | Obtains JWT pair (Access & Refresh) | `200 OK` ✅ |
| `/api/auth/token/refresh/` | `POST` | Public | Refreshes expired access tokens | `200 OK` ✅ |
| `/api/users/` | `GET` | Bearer JWT | Returns list of registered users | `200 OK` ✅ |
| `/api/projects/` | `GET` / `POST` | Bearer JWT | Project management (Scoped by owner) | `200 OK / 201 Created` ✅ |
| `/api/tasks/` | `GET` / `POST` | Bearer JWT | Task list & creation with RBAC | `200 OK / 201 Created` ✅ |
| `/api/tasks/<id>/` | `PATCH` / `DELETE` | Bearer JWT | State updates (`COMPLETED`, `REOPENED`, etc.) | `200 OK / 204 No Content` ✅ |

---

## 4. Lifecycle Event Publishing

When task mutations occur in [`tasks/views.py`](file:///f:/multi-server-system/services/Django/tasks/views.py), Django dispatches event payloads to Node.js (`http://127.0.0.1:8001/internal/events`):

```json
{
  "eventType": "TASK_COMPLETED",
  "entityType": "TASK",
  "entityId": "<TASK_UUID>",
  "payload": {
    "title": "Build Dashboard",
    "project_id": "<PROJECT_UUID>",
    "assigned_to": "<USER_UUID>",
    "completed_by": "<USER_UUID>",
    "created_at": "2026-09-08T10:00:00Z",
    "completed_at": "2026-09-08T10:45:00Z"
  }
}
```

---

## 5. Audit Verification & Status

- **Database Integrity**: PostgreSQL connection verified (`triserver`).
- **RBAC Unit Scenarios**: Pass (`403 Forbidden` on unauthorized project access).
- **CORS Setup**: `corsheaders` configured for frontend cross-origin requests.
