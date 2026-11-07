# सह्यादृष्टी | SAHYADRUSHTI AI
### पावसाआधी नव्हे, धोक्याआधी सावध!
**English Tagline:** *See the danger before it becomes a disaster.*

> **UN Sustainable Development Goal Alignment:**  
> **SDG 13.1:** Strengthen resilience and adaptive capacity to climate-related hazards and natural disasters.  
> **SDG 11.5:** Reduce the adverse impacts of natural disasters on human lives, transport lifelines, and settlements.

---

## 1. Executive Summary & Problem Statement

Conventional weather forecasts and emergency bulletins issue broad, district-wide alerts (e.g., *"Orange Alert for Pune District"* covering >15,000 km²). In mountainous terrain like the Western Ghats (Sahyadris), this broad-area model fails local decision-makers. 

**The same 150 mm of rain produces radically divergent risk across different spots:**
- **Location A (Lonavala Civic Plateau):** Low slope (6.5°), well-drained loam → **Low Risk (16/100)**. Safe & Stable.
- **Location B (Amrutanjan Bridge / Bhor Ghat):** 36.5° steep fractured basalt cut slope, 86% soil saturation → **Critical Landslide & Rockfall Hazard (84/100)**.
- **Location C (Bhushi Dam Downstream Cascade):** 24.5° slope receiving runoff from a 4.8 km² steep upstream catchment → **Lethal Flash Surge Danger (88/100)**.

**SAHYADRUSHTI AI** answers the fundamental question:  
**Not just *"How much rain will fall?"* but *"Which exact slope, stream, or corridor is dangerous, why, and what action to take?"***

---

## 2. 12-Item Pilot Feature Checklist (Lonavala, Khandala & Maval)

- [x] **1. Real, Working Lonavala Geospatial Map:** Interactive Leaflet map centered on Lonavala-Khandala (18.755°N, 73.395°E), real coordinates, zoom, pan, reset, Topographic relief contour layer, and selectable location markers.
- [x] **2. Local Tourist Danger Monitoring:** Bhushi Dam, Kune Falls, Tiger Point, Lion's Point, and Rajmachi Trek Route with transparently labelled live, modelled, or unavailable status and upstream catchment surge analysis.
- [x] **3. Landslide-Prone Corridors:** Georeferenced segments along the Mumbai–Pune Expressway (Amrutanjan Bridge, Adoshi Tunnel) and Central Railway Bhor Ghat (Monkey Hill, Thakurwadi), explicitly distinguishing natural rockfall from traffic/freight accidents.
- [x] **4. Actual Terrain Intelligence:** Real digital elevation model metrics (SRTM 30m / Copernicus DEM): slope angles (6.5° to 46°), elevation (410m to 780m MSL), upstream catchment basins (1.2 to 14.2 km²), and drainage proximity.
- [x] **5. Rainfall & Soil Saturation:** Recent rainfall (1h, 3h, 24h, 48h accumulation), forecast precipitation, multi-depth soil moisture (`0_to_1cm`, `3_to_9cm`, `9_to_27cm`), Antecedent Precipitation Index ($API = \sum k^i P_{t-i}$), observation source, and freshness timestamps in IST (`Asia/Kolkata`).
- [x] **6. Hyperlocal Risk Model:** Physics-informed geotechnical ensemble (infinite-slope Factor of Safety with pore-pressure & jointing, Rational Method runoff, and Platt sigmoid calibration) with local perturbation (SHAP-proxy) feature importances.
- [x] **7. Lonavala Incident History:** Sourced, dated historical catalog including the June 30, 2024 Bhushi Dam waterfall surge tragedy (5 fatalities, Times of India / Pune Police records), July 2025 Expressway boulder falls, July 2026 Patan escarpment fissures, and February 2026 Adoshi hazardous tanker stoppage.
- [x] **8. Safe Action & Evacuation Support:** Verified disaster relief shelters (Lonavala Municipal Council Hall, Khandala ZP School, Ryewood Administrative Complex), official contacts (Pune DDMA 1077, Lonavala Police 02114-273033, Highway Patrol 9822498224), and survival guidelines.
- [x] **9. Tourist & Resident Interfaces:** Full trilingual support (**मराठी (mr)**, **English (en)**, **हिंदी (hi)**), public citizen view, tourist spot-check directory, and comprehensive authority control room dashboard.
- [x] **10. Historical Storm Replay & Simulator:** 24-hour storm progression timeline slider backfilled with hourly Open-Meteo reanalysis of the July 6–8, 2026 extreme monsoon event + interactive "What If the Storm Intensifies?" scenario simulator + 1-click deterministic 3-location comparison.
- [x] **11. Offline Resilience:** Fully client-side cached dataset fallbacks, offline status banner, and graceful error handling if backend or sensors disconnect.
- [x] **12. Enterprise Authority Operations & Four-Eyes RBAC:** Role-Based Access Control (`operator`, `approver`, `admin`) using Argon2 and rotating JWTs; strict Four-Eyes Rule (alert drafter cannot approve own advisory); high-entropy `X-Device-Key` sensor ingestion authentication; rate-limited endpoints (`slowapi`); Common Alerting Protocol (CAP v1.2) XML dissemination.

---

## 3. Technology Stack & Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│               FRONTEND (React 19 + TypeScript + Vite)                  │
│  - Leaflet Map with OpenTopoMap / OSM Relief Tiles                     │
│  - Trilingual UI (मराठी / English / हिंदी)                             │
│  - In-Memory JWT Authentication State (No sensitive localStorage)      │
│  - Open-Meteo Attribution & Real-time Live Weather Integration         │
│  - 10 Modules: Home, Map, Spot-Check, Corridors, Alerts, Incidents,    │
│    Safety, Replay, Authority Console (RBAC-gated), Research, About     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST /api/*
┌───────────────────────────────────▼────────────────────────────────────┐
│               BACKEND (Python 3.12+ + FastAPI + SQLModel)              │
│  - Modular Router Architecture (`app/routers/*`, `app/services/*`)     │
│  - SQLite Database with Write-Ahead Logging (WAL) & Foreign Keys       │
│  - Alembic Database Schema Migrations                                  │
│  - Argon2 Password Hashing (pwdlib) & Anti-Timing Enumeration Checks   │
│  - JWT HS256 Access Tokens + Rotating Refresh Tokens in DB             │
│  - SlowAPI Rate Limiting (Login, Incidents, Simulation, Predictions)   │
│  - Single-Worker APScheduler (30-min live Open-Meteo weather fetch)    │
│  - CAP 1.2 XML Serializer & Append-Only Audit Logging                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│               GEOTECHNICAL & AI / ML PIPELINE                          │
│  - Sahyadri-GeoRisk Ensemble (v2.1)                                    │
│  - Landslide Factor of Safety (FS) & Basalt Overburden Shear (Infinite)│
│  - Hydrograph Catchment Convergence Model & Antecedent Precipitation   │
│  - Platt Sigmoid Calibration & SHAP-Proxy Perturbation Weights         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Setup, Environment & Deployment

### Prerequisites
- **Node.js**: v18+
- **Python**: v3.12+ (verified on Python 3.12.10)

### Environment Variables (`.env`)
Create a `.env` file in the project root:
```ini
# Environment & Debugging
DEBUG=False
APP_VERSION=2.1.0

# Database Connection (SQLite with WAL by default; seamless Postgres switch)
DATABASE_URL=sqlite:///./sahyadrushti.db

# Authentication & Security
# WARNING: In production (DEBUG=False), JWT_SECRET must be set to a high-entropy secret!
JWT_SECRET=production_high_entropy_secret_change_me_in_real_deployment_1234567890
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_MINUTES=30
JWT_REFRESH_TOKEN_DAYS=7

# Rate Limiting
RATELIMIT_ENABLED=True
RATE_LIMIT_LOGIN=5/minute
RATE_LIMIT_INCIDENTS=10/minute
RATE_LIMIT_ML=20/minute

# Weather Ingestion & Scheduler
WEATHER_MODE=live
WEATHER_LATITUDE=18.755
WEATHER_LONGITUDE=73.395
WEATHER_FETCH_INTERVAL_MINUTES=30
WEATHER_CACHE_TTL_MINUTES=15
BIAS_MULTIPLIER=1.0

# Background Job Runner
SCHEDULER_ENABLED=True
```

### Database Migrations (Alembic)
Initialize or upgrade the persistent database:
```bash
# Apply all schema revisions to head
python -m alembic upgrade head
```

### User & Device Key Provisioning CLI
Passwords can be provided via flag, interactive prompt, or `SAHYADRUSHTI_USER_PASSWORD` environment variable.

```bash
# 1. Create an Emergency Operations Room Operator
python -m app.cli create-user --username operator1 --role operator --password operatorpass123

# 2. Create an Emergency Cell Approving Officer
python -m app.cli create-user --username approver1 --role approver --password approverpass123

# 3. Create a System Administrator
python -m app.cli create-admin --username admin1 --password adminsecret123

# 4. Generate high-entropy per-device API key for IoT Edge Sensor node
python -m app.cli create-device-key --node-id SAHYA-RAIN-01
```

---

## 5. Running the Application

### 1. Start the FastAPI Backend Server
> [!IMPORTANT]
> The background weather and risk evaluation scheduler (`APScheduler`) must run in a **single worker process** (`--workers 1`). If running multiple uvicorn workers behind a reverse proxy in production, set `SCHEDULER_ENABLED=False` on worker nodes and run a dedicated standalone cron worker process.

```bash
python run_backend.py
```
*Backend will start on `http://127.0.0.1:8000`.*  
*API Swagger Documentation available at `http://127.0.0.1:8000/docs`.*

### 2. Start the Frontend Development Server
```bash
cd frontend
npm install
npm run dev
```
*Frontend opens on `http://127.0.0.1:5173/`.*

### 3. Build Frontend for Production
```bash
cd frontend
npm run build
```

---

## 6. Verification & Automated Test Suite

The platform includes comprehensive test suites covering API contracts, database persistence, weather scheduling, and security RBAC:

```bash
# 1. Run all unit and integration tests (51 tests)
python -m pytest tests/

# 2. Run API backward-compatibility golden contract tests (26 fixtures)
python -m pytest tests/test_contract.py

# 3. Run database persistence and WAL verification tests
python -m pytest tests/test_phase1_db.py

# 4. Run Open-Meteo weather client & scheduler tests
python -m pytest tests/test_phase2_weather.py

# 5. Run Auth, Argon2, JWT, Rate-Limiting & Four-Eyes RBAC tests
python -m pytest tests/test_phase3_auth.py

# 6. Run live network test against real Open-Meteo API (opt-in)
python -m pytest tests/test_phase2_weather.py -m live

# 7. Run Real OS Subprocess Restart Persistence Test
python scripts/test_real_process_restart.py

# 8. Run End-to-End Workflow Verification Demo Script
python scripts/demo_e2e_flow.py
```

---

## 7. Security Architecture & RBAC Matrix

| Endpoint | Method | Authentication | Required Role | Rate Limit | Description |
|---|---|---|---|---|---|
| `/api/locations` | `GET` | Public | None | None | Monitored pilot points with terrain attributes |
| `/api/weather/current` | `GET` | Public | None | None | Live cached weather observations (IST) |
| `/api/weather/forecast` | `GET` | Public | None | None | 24h & 48h rain and soil moisture forecasts |
| `/api/alerts` | `GET` | Public | None | None | Public broadcast alerts (**approved only**) |
| `/api/alerts/cap` | `GET` | Public | None | None | Common Alerting Protocol 1.2 XML feed |
| `/api/incidents` | `GET` | Public | None | None | Verified + unverified incident reports |
| `/api/incidents` | `POST` | Public | None | 10 / min | Citizen incident submission (marked unverified) |
| `/api/simulate` | `POST` | Public | None | 20 / min | Physics-based rainfall what-if scenario |
| `/api/predict` | `POST` | Public | None | 20 / min | Raw ML geotechnical risk evaluation |
| `/api/auth/login` | `POST` | Public | None | 5 / min | Authenticate user, issue JWT & refresh token |
| `/api/auth/refresh` | `POST` | Public | None | None | Rotate refresh token and issue new JWT |
| `/api/auth/logout` | `POST` | Public / Bearer | None | None | Revoke refresh token and log out |
| `/api/auth/me` | `GET` | Bearer JWT | Any valid user | None | Get identity and role of current caller |
| `/api/authority/alerts/draft` | `POST` | Bearer JWT | `operator`, `approver`, `admin` | None | Create early-warning advisory draft |
| `/api/authority/alerts/{id}/approve` | `POST` | Bearer JWT | `approver`, `admin` | None | Publish draft advisory (**Four-Eyes enforced: creator cannot approve, 409 Conflict**) |
| `/api/authority/queue` | `GET` | Bearer JWT | `operator`, `approver`, `admin` | None | Locations with risk ≥ 70 pending advisories |
| `/api/authority/audit` | `GET` | Bearer JWT | `approver`, `admin` | None | Append-only security and operational audit trail |
| `/api/sensors/status` | `GET` | Public | None | None | IoT edge sensor telemetry diagnostics |
| `/api/sensors/ingest` | `POST` | `X-Device-Key` | Valid sensor key | None | Ingest edge rain gauge / tilt sensor telemetry |

---

## 8. Authoritative Data Provenance & Limitations

### External Data Attribution & Terms of Service
- **Weather Data:** Powered by [Open-Meteo](https://open-meteo.com/). Used under the Creative Commons Attribution 4.0 International (CC BY 4.0) license for non-commercial educational, scientific, and research purposes.
- **Topographic Data:** Copernicus DEM 30m / NASA SRTM 1-Arc-Second via OpenTopoMap and OpenStreetMap contributors.

### Grid Resolution & Bias-Correction Architecture
- **Grid Resolution Notice:** Open-Meteo reanalysis operates at ~9–11 km spatial resolution. Several pilot monitoring locations (e.g. Lonavala Town, Kune Falls, Bhushi Dam) share the same underlying numerical model grid cell and receive identical raw rainfall inputs.
- **Micro-Terrain Differentiation:** Risk score variations between these spots (e.g. 16/100 at Lonavala Town vs 88/100 at Bhushi Dam) are driven by local slope, upstream catchment concentration, drainage proximity, and jointing — not rainfall alone.
- **Calibration Notice:** Global reanalysis models are suspected to underestimate peak extreme rainfall pulses in the narrow Sahyadri crest (e.g., during the extreme July 6–8, 2026 monsoon event). The system stores raw observations (`rain_mm_raw`) and corrected observations (`rain_mm_corrected`) separately with `bias_multiplier = 1.0` by default. The pipeline is designed so non-linear quantile mapping or IMD station calibrations can be applied modularly without modifying ingested raw datasets.
