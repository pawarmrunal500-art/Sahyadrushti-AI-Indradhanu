# PralaySense AI (SAHYADRUSHTI AI / सह्यादृष्टी)
### Hyperlocal Landslide & Flash-Flood Early Warning Platform for the Western Ghats

> [!IMPORTANT]
> **Platform Maturity Status:** Demo-ready, pilot-stage, synthetic-calibrated model.
> Risk scores represent a relative physical vulnerability **risk index (0–100)**, NOT empirical probability of occurrence. Geotechnical factor of safety (FS) and hydrological routing are physically grounded on Deccan Trap basalt overburden mechanics with generic global empirical thresholds (e.g., Caine 1980 Intensity-Duration trigger). **Parameters have NOT been calibrated against field instrumentation or IMD station records.**

---

## 1. System Overview & Problem Statement
Landslides and flash floods in mountainous regions depend heavily on local topography: terrain slope, overburden curvature, soil moisture profile, bedrock fracturing, drainage convergence, and antecedent rainfall history. District-wide warnings (such as broad district red alerts) fail to differentiate which specific slope, road cutting, or stream channel is vulnerable.

**PralaySense AI** addresses this gap by:
1. **Hyperlocal Spatial Differentiation:** Evaluating distinct geotechnical Factor of Safety (FS) and rational runoff responses across 12 pilot locations spanning Lonavala, Khandala, and the Bhor Ghat corridor.
2. **Antecedent Memory Variable $W(t)$:** Tracking slow drainage recession (time constant $\tau = 60\text{h}$) and profile soil moisture ($0\text{–}1\text{cm}, 3\text{–}9\text{cm}, 9\text{–}27\text{cm}$) across 14-day lookback windows.
3. **Four-Eyes Operational Governance:** Requiring mandatory secondary authorization before emergency alerts can be published (HTTP 409 Conflict enforcement on self-approval), producing Common Alerting Protocol (CAP 1.2) XML.
4. **Honest Multi-Lingual Guidance:** Delivering actionable, clear recommendations in English, Marathi (मराठी), and Hindi (हिन्दी) for citizens, tourists, and district emergency operations centers (EOC).

---

## 2. Pilot Locations (Lonavala–Khandala–Bhor Ghat)
The pilot monitoring network encompasses 12 high-vulnerability points across multiple hazard classes:
- **Expressway & Rail Corridors:** Amrutanjan Bridge (`khandala_expressway`), Adoshi Tunnel (`adoshi_tunnel`), Monkey Hill (`monkey_hill`), Thakurwadi (`thakurwadi`).
- **Escarpments & Hillside Habitations:** Kune Falls (`kune_falls`), Tiger Point (`tiger_point`), Lion's Point (`lions_point`), Rajmachi Route (`rajmachi_route`), Patan Village (`patan_village`).
- **Water Bodies & Urban Drainage:** Bhushi Dam (`bhushi_dam`), Valvan Dam (`valvan_dam`), Lonavala Civic Center (`lonavala_town`).

---

## 3. Quick Start Guide (Windows / Linux)

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Node.js 18+ and npm
- Git

### Installation & Environment Setup
```powershell
# 1. Clone repository
git clone <repo-url>
cd SAHYADRUSHTI

# 2. Set up Python virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Linux/macOS: source .venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env to set application parameters.
# In development (DEBUG=true), a secure fallback key is used automatically.

# 5. Initialize database & seed pilot data
python -m backend.data_layer
```

### Running the Test Suite
```powershell
# Run full unit, contract, auth, and regression suite (69 tests)
python -m pytest tests/ -v

# Run the automated problem statement & honesty verification harness (C1-C8)
python scripts/ps_check.py
```

### Running the Application Locally
```powershell
# Terminal 1: Backend API server (runs on port 8000)
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend client (runs on port 5173)
cd frontend
npm install
npm run dev
```
Open your browser to `http://localhost:5173`.

---

## 4. Operational Governance & User Management
User creation and role-based access control (RBAC) are managed via the administrative CLI:
```powershell
# Create admin / approver / operator securely via interactive prompt:
python scripts/create_user.py --username admin_officer --role admin
# When prompted, enter a secure password (minimum 8 characters).
```
> [!NOTE]
> Passwords must never be passed as plaintext command-line arguments. In production, `DEBUG=false` enforces a minimum 32-character `JWT_SECRET`.

---

## 5. Known Limitations & Transparency Disclosure
In accordance with scientific integrity standards, the following platform boundaries are explicitly disclosed:
1. **Uncalibrated Model Parameters:** All geotechnical parameters (effective cohesion $c' = 2.5\text{–}16\text{ kPa}$, internal friction angle $\phi = 30^\circ\text{–}34^\circ$, colluvium thickness $z = 2.2\text{m}$, saprolite drainage recession time constant $\tau = 60\text{h}$) are physical estimates based on Deccan Trap basalt literature, not fitted to localized slope inclinometer or piezometer records.
2. **Reanalysis Spatial Grid Resolution:** Weather inputs are retrieved from Open-Meteo's 9–11 km reanalysis raster. Multiple pilot locations share identical regional rainfall figures; local risk differences arise from slope, DEM relief, soil saturation, and catchment geometry.
3. **Suspected Extreme Rainfall Underestimation:** 9–11 km reanalysis grids tend to smooth sharp orographic cloudburst peaks. Peak rainfall values in steep ghats should be considered lower-bound estimates until calibrated against IMD station data.
4. **Digital Elevation Model (DEM) Spatial Resolution:** Terrain slopes are derived from the Copernicus GLO-30 30-meter DEM. Narrow highway cuts or vertical retaining structures smaller than 30m may not be fully resolved in point slopes, though extended buffer filters (60m, 150m, 300m) capture the broader escarpment relief.
5. **Coordinate Ground-Truthing Requirements (`TODO-USER`):** Several pilot sites (e.g., Patan Village, Monkey Hill) require ground-truthing to verify whether monitoring targets refer to valley floor habitations or upper escarpment headwalls.

---

## 6. Attributions & Data Sources
- **Weather Data:** Weather data by [Open-Meteo.com](https://open-meteo.com/) (CC BY 4.0).
- **Elevation Model:** Copernicus GLO-30 Digital Elevation Model (`COPERNICUS/DEM/GLO30`) accessed via Google Earth Engine.
- **Cartography:** Base maps by OpenStreetMap contributors & OpenTopoMap.
