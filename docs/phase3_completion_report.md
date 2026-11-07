# सह्यादृष्टी | SAHYADRUSHTI AI — Phase 3 & Security Completion Report

## 1. Executive Summary

Phase 3 (Authentication, Authorization & RBAC) and Phase 3.5 (Security Hardening & Refinements) are fully implemented and verified across the codebase.

- **Phase 0 (Safety Net):** Golden contract fixtures recorded (26/26 green), backend modularized into `app/`, backward-compatibility preserved.
- **Phase 1 (Database Persistence):** SQLite in Write-Ahead Logging (`WAL`) mode with foreign keys, SQLModel schemas, Alembic migrations, atomic repositories, and append-only audit logging.
- **Phase 2 (Live Weather & Resilient Scheduler):** Batched Open-Meteo live API integration, multi-depth soil moisture (`0_to_1cm`, `3_to_9cm`, `9_to_27cm`), Antecedent Precipitation Index ($API$), configurable bias-correction layer (`bias_multiplier = 1.0` default), single-worker APScheduler, and July 6–8, 2026 storm backfill replay.
- **Phase 3 & 3.5 (Enterprise Security & Four-Eyes RBAC):** 
  - Argon2 password hashing (`pwdlib`) with anti-timing dummy hash checks.
  - Scoped account lockout per `(username, client_ip)` after 5 consecutive failures, protecting legitimate users from denial-of-service by distributed attackers.
  - JWT HS256 access tokens (30 min) + rotating refresh tokens with DB revocation.
  - Strict Four-Eyes rule enforced via user primary key (`alerts.created_by_id == current_user.id`) returning HTTP 409 Conflict.
  - Per-device high-entropy `X-Device-Key` sensor ingestion authentication.
  - Configurable rate limiting (`slowapi`) with distinct limits for login, refresh, incident reporting, and a high-throughput `DEMO_MODE` for evaluations.
  - Interactive/masked password provisioning via CLI (`python -m app.cli create-user`).
  - Open-Meteo attribution without uncalibrated claims.

---

## 2. Endpoint Access-Level & Security Matrix

All 22 existing API endpoints remain backward-compatible (all 26 contract fixtures green):

| Endpoint Path | HTTP Method | Auth Type | Required Role | Rate Limit (Default) | Rate Limit (Demo Mode) | Behavior & Security Rule |
|---|---|---|---|---|---|---|
| `/api/locations` | `GET` | Public | None | None | None | Monitored locations with terrain & catchment metrics. |
| `/api/weather/current` | `GET` | Public | None | None | None | Live cached weather observations in IST (`Asia/Kolkata`). |
| `/api/weather/forecast` | `GET` | Public | None | None | None | 24h & 48h precipitation & multi-depth soil moisture forecasts. |
| `/api/alerts` | `GET` | Public | None | None | None | Public broadcast alerts (**strictly filters to approved only**; drafts never leak). |
| `/api/alerts/cap` | `GET` | Public | None | None | None | Disseminates approved alerts formatted in OASIS Common Alerting Protocol (CAP v1.2) XML. |
| `/api/incidents` | `GET` | Public | None | None | None | Crowd-sourced and verified incident records. |
| `/api/incidents` | `POST` | Public | None | `10/min` | `10/min` | Public citizen hazard report. Stored as `Unverified report`; excluded from model inputs. |
| `/api/shelters` | `GET` | Public | None | None | None | Designated cyclone/flood relief centers & contact directory. |
| `/api/corridors` | `GET` | Public | None | None | None | Expressway and railway ghat corridor risk segments. |
| `/api/replay` | `GET` | Public | None | None | None | 9-step storm progression backfilled from Open-Meteo reanalysis of the July 6–8, 2026 event. |
| `/api/simulate` | `POST` | Public | None | `20/min` | `100/min` | Dynamic what-if rainfall & soil saturation simulation. |
| `/api/predict` | `POST` | Public | None | `30/min` | `120/min` | Raw ML geotechnical risk evaluation. |
| `/api/demo/scenario` | `GET` | Public | None | None | None | Deterministic 3-location comparison scenario. |
| `/api/sensors/status` | `GET` | Public | None | None | None | Field IoT sensor network health diagnostics & battery levels. |
| `/api/sensors/ingest` | `POST` | Header | Valid Device Key | None | None | Requires `X-Device-Key` header matching high-entropy SHA-256 hash in DB. Rejects unauthenticated with 401. |
| `/api/auth/login` | `POST` | Public | None | `5/min` | `5/min` | Argon2 verification, anti-timing dummy hash, lockout per `(username, client_ip)`. Returns JWT & refresh token. |
| `/api/auth/refresh` | `POST` | Public | None | `10/min` | `10/min` | Token rotation: revokes presented refresh token and issues a new pair. Rate-limited. |
| `/api/auth/logout` | `POST` | Public/Bearer | None | None | None | Revokes refresh token in DB and appends `LOGOUT` to audit log. |
| `/api/auth/me` | `GET` | Bearer JWT | Any authenticated | None | None | Returns caller's username, role, and ID. |
| `/api/authority/alerts/draft` | `POST` | Bearer JWT | `operator`, `approver`, `admin` | None | None | Creates draft alert, records `created_by_id` in DB for Four-Eyes enforcement. |
| `/api/authority/alerts/{id}/approve` | `POST` | Bearer JWT | `approver`, `admin` | None | None | Approves alert. **Enforces Four-Eyes: returns 409 Conflict if caller was the drafter (`created_by_id == current_user.id`).** |
| `/api/authority/queue` | `GET` | Bearer JWT | `operator`, `approver`, `admin` | None | None | Lists locations with latest risk score ≥ 70 that lack an active approved alert. |
| `/api/authority/audit` | `GET` | Bearer JWT | `approver`, `admin` | None | None | Append-only audit log with timestamp, action, entity, user ID, and JSON details. |
| `/api/health` | `GET` | Public | None | None | None | Additive health status: database connection, last weather fetch, scheduler status. |

---

## 3. Four-Eyes Principle Enforcement

To prevent erroneous or unilateral dissemination of emergency sirens to the public:
1. When an advisory is drafted via `POST /api/authority/alerts/draft`, the author's primary key (`id`) is persisted in `alerts.created_by_id`.
2. When approval is attempted via `POST /api/authority/alerts/{alert_id}/approve`:
   - Role check verifies caller is `approver` or `admin` (`operator` receives `403 Forbidden`).
   - Four-eyes validation checks whether `alert.created_by_id == current_user.id`. If true, the server aborts with **HTTP 409 Conflict**:
     `"Four-Eyes Principle violation: user '<username>' cannot approve an advisory they drafted."`
   - Even administrators cannot self-approve their own drafts.
3. The legacy `approver_role` query parameter is retained for backward compatibility, but ignored in favor of the JWT token identity.

---

## 4. Edge IoT Device Key Authentication

Field rain gauges and geotechnical sensors report to `POST /api/sensors/ingest`:
1. Provisioned via CLI: `python -m app.cli create-device-key --node-id <node_id>`.
2. Revoked via CLI: `python -m app.cli revoke-device-key --node-id <node_id>`.
3. Stored in `sensor_nodes.api_key_hash` using SHA-256. Plaintext is displayed only once.
4. Missing or invalid keys return **HTTP 401 Unauthorized** using constant-time comparison (`secrets.compare_digest`).
