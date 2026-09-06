# Endpoint & Security Verification Review Report

## Executive Summary
A comprehensive test suite was executed against the Django REST Framework endpoints to verify general API functionality and enforce strict role-based access control (RBAC) rules on task creation and assignment.

---

## 🔐 Permission & RBAC Test Scenarios

### Rule 1: Regular users can ONLY create tasks in projects they own.
- **Test Case 1.1 (Standard User - Own Project)**
  - **Actor**: `user1` (Role: `MEMBER`)
  - **Action**: Creating task in Project `user1_proj` (`owner = user1`).
  - **Result**: `HTTP 201 Created` ✅
  - **Payload Returned**: `{ "id": "b54646c9-...", "title": "Valid Task", "project": "a5d43cfe-..." }`

- **Test Case 1.2 (Standard User - Foreign Project)**
  - **Actor**: `user1` (Role: `MEMBER`)
  - **Action**: Attempting to create task in Project `user2_proj` (`owner = user2`).
  - **Result**: `HTTP 403 Forbidden` ✅
  - **Error Detail**: `{"detail": "You can only create tasks in your own projects."}`

- **Test Case 1.3 (Admin User - Any Project)**
  - **Actor**: `admin` (Role: `ADMIN`)
  - **Action**: Creating task in Project `user2_proj` (`owner = user2`).
  - **Result**: `HTTP 201 Created` ✅
  - **Payload Returned**: `{ "id": "bceb80e2-...", "title": "Admin Task", "project": "3168959c-..." }`

---

### Rule 2: Regular users can ONLY assign tasks to themselves.
- **Test Case 2.1 (Standard User - Cross Assignment)**
  - **Actor**: `user1` (Role: `MEMBER`)
  - **Action**: Attempting to set `assigned_to = user2.id`.
  - **Result**: `HTTP 403 Forbidden` ✅
  - **Error Detail**: `{"detail": "You can only assign tasks to yourself."}`

---

## 🌐 Endpoint Status Summary

| Endpoint | Method | Authentication | Status | Verification |
| :--- | :--- | :--- | :--- | :--- |
| `/api/auth/token/` | `POST` | None | `200 OK` | Validated JWT generation |
| `/api/auth/token/refresh/` | `POST` | None | `200 OK` | Validated token rotation |
| `/api/users/` | `GET` | Bearer Token | `200 OK` | Lists active users |
| `/api/projects/` | `GET` / `POST` | Bearer Token | `200 OK / 201` | Scoped to project owner |
| `/api/tasks/` | `GET` / `POST` | Bearer Token | `200 OK / 201` | Enforces ownership check |

---

## 💻 Code Implementation Verified

In [tasks/views.py](file:///i:/multi-server-system/services/Django/tasks/views.py#L20-L32):

```python
def perform_create(self, serializer):
    project = serializer.validated_data["project"]
    assigned_to = serializer.validated_data.get("assigned_to")
    user = self.request.user

    # USER can only create tasks in their own project
    if user.role != "ADMIN" and project.owner_id != user.id:
        raise PermissionDenied("You can only create tasks in your own projects.")

    # USER can only assign the task to themselves
    if user.role != "ADMIN" and assigned_to is not None:
        if assigned_to.id != user.id:
            raise PermissionDenied("You can only assign tasks to yourself.")

    serializer.save()
```
