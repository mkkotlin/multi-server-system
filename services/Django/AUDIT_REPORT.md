# 🛡️ Django API & Security Audit Report

**Generated Date**: 2026-09-05  
**Target Service**: Django REST Framework API (`services/Django`)

---

## 1. System Health Check
- **Django Configuration Check (`python manage.py check`)**:
  - Result: `0 Silenceable / 0 Errors` ✅
- **CORS Configuration**:
  - Middleware: `corsheaders.middleware.CorsMiddleware` configured.
  - Setting: `CORS_ALLOW_ALL_ORIGINS = True` (allows cross-origin requests from test interfaces & frontends).

---

## 2. Security & RBAC Audit Summary

| Feature / Scenario | Actor | Target Resource | Access Rule | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Task Creation in Own Project** | Member (`user1`) | Project owned by `user1` | Allowed | `201 Created` ✅ |
| **Task Creation in Foreign Project** | Member (`user1`) | Project owned by `user2` | Denied | `403 Forbidden` ✅ |
| **Task Creation (Admin Privilege)** | Admin (`admin`) | Project owned by `user2` | Allowed | `201 Created` ✅ |
| **Task Assignment (Self Assignment)** | Member (`user1`) | `assigned_to = user1` | Allowed | `201 Created` ✅ |
| **Task Assignment (Cross User)** | Member (`user1`) | `assigned_to = user2` | Denied | `403 Forbidden` ✅ |

---

## 3. End-to-End Endpoint Audit Matrix

| Endpoint | HTTP Method | Authentication | Scope / Permission Filter | Status |
| :--- | :--- | :--- | :--- | :--- |
| `/api/auth/token/` | `POST` | None | Public Token Issuance | `200 OK` |
| `/api/auth/token/refresh/` | `POST` | None | Public Token Refresh | `200 OK` |
| `/api/users/` | `GET` | Bearer Token | Authenticated Users | `200 OK` |
| `/api/users/<id>/` | `GET` | Bearer Token | Authenticated Users | `200 OK` |
| `/api/projects/` | `GET` | Bearer Token | Admins view all; Users view owned | `200 OK` |
| `/api/projects/` | `POST` | Bearer Token | Creates project with `owner = request.user` | `201 Created` |
| `/api/tasks/` | `GET` | Bearer Token | Admins view all; Users view owned project tasks | `200 OK` |
| `/api/tasks/` | `POST` | Bearer Token | Enforces project owner & self-assignment rules | `201 Created` |
| `/api/tasks/<id>/` | `PATCH` | Bearer Token | Auto-manages `completed_at` timestamp | `200 OK` |
| `/api/tasks/<id>/` | `DELETE` | Bearer Token | Scoped deletion | `204 No Content` |

---

## 4. Code Security Reference

Code snippet from `tasks/views.py`:

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
