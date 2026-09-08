# ⚡ Node.js Event Server Audit Report

**Service Name**: Node.js Event & Notification Gateway  
**Location**: [`services/Node`](file:///f:/multi-server-system/services/Node)  
**Port**: `8001`  
**Stack**: Express.js + Prisma ORM + PostgreSQL (`triserver`)  

---

## 1. Service Overview

The Node.js server acts as an asynchronous event message router and persistence layer for system events and user notifications. It ingests internal events from Django, stores event history via Prisma ORM, and forwards relevant task analytics metrics downstream to FastAPI (`:8002`).

---

## 2. Architecture & Data Flow

```
[Django REST API :8000]
         │ (POST /internal/events)
         ▼
[Node.js Event Server :8001] ──► [PostgreSQL: events & notifications]
         │ (POST /internal/events + X-Service-Key)
         ▼
[FastAPI Analytics :8002]
```

---

## 3. Security & Authentication Audit

- **Internal Event Endpoint (`/internal/events`)**: Secured via service secret verification.
- **Service Key Protection**: Outbound requests to FastAPI attach header `X-Service-Key: <FASTAPI_SERVICE_KEY>`.
- **Database Access**: Managed via Prisma ORM client with parameterized raw queries for health checks.

---

## 4. API Inventory & Endpoints

| Route / Endpoint | Method | Access Level | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| `/health` | `GET` | Public | Service uptime status check | `200 OK` ✅ |
| `/health/db` | `GET` | Public | Database connection check via Prisma | `200 OK` ✅ |
| `/internal/events` | `POST` | Service Secret | Ingests Django events & proxies to FastAPI | `200 OK` ✅ |
| `/api/events` | `GET` | Bearer Auth | Retrieves persisted system event logs | `200 OK` ✅ |
| `/api/notifications` | `GET` | Bearer Auth | Retrieves user notification stream | `200 OK` ✅ |

---

## 5. Event Handling & Forwarding Matrix

| Received Event Type | Target Service | Forwarded Payload Key | Downstream Action |
| :--- | :--- | :--- | :--- |
| `TASK_CREATED` | FastAPI Analytics | `entityId`, `payload.owner_id` | Initializes task metrics baseline |
| `TASK_STATUS_CHANGED` | FastAPI Analytics | `entityId` | Increments `status_changes` count |
| `TASK_COMPLETED` | FastAPI Analytics | `entityId`, `created_at`, `completed_at` | Computes duration in seconds |
| `TASK_REOPENED` | FastAPI Analytics | `entityId`, `status` | Updates lifecycle state |

---

## 6. Audit & Health Check Verification

- **Express Server Uptime**: Healthy on port `8001`.
- **Prisma Integration**: Successfully connected to database schema (`triserver`).
- **CORS Middleware**: Enabled (`app.use(cors())`) for frontend consumption.
