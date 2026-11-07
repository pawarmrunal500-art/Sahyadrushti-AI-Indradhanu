# सह्यादृष्टी | SAHYADRUSHTI AI
### पावसाआधी नव्हे, धोक्याआधी सावध!
**English Tagline:** *See the danger before it becomes a disaster.*

> **UN Sustainable Development Goal Alignment:**  
> **SDG 13.1:** Strengthen resilience and adaptive capacity to climate-related hazards and natural disasters.  
> **SDG 11.5:** Reduce the adverse impacts of natural disasters on human lives, transport lifelines, and settlements.

---

## 1. Executive Summary & Problem Statement

Conventional weather forecasts and emergency bulletins issue broad, district-wide alerts (e.g., *"Orange Alert for Pune District"* covering >15,000 km²). In mountainous terrain like the Western Ghats (Sahyadris), this broad-area model fails local decision-makers. 

**Three locations receiving the exact same 150mm rainfall can face radically divergent hazards:**
- **Location A (Lonavala Civic Plateau):** Low slope (6.5°), well-drained loam → **Safe & Stable**.
- **Location B (Amrutanjan Bridge / Bhor Ghat):** 36.5° steep fractured basalt cut slope, 86% soil saturation → **Critical Landslide & Rockfall Hazard**.
- **Location C (Bhushi Dam Downstream Cascade):** 24.5° slope receiving runoff from a 4.8 km² steep upstream catchment → **Lethal Flash Surge Danger**.

**SAHYADRUSHTI AI** answers the fundamental question:  
**Not just *"How much rain will fall?"* but *"Which exact locations may become dangerous, why, and what should people do?"***

---

## 2. 12-Item Pilot Feature Checklist (Lonavala, Khandala & Maval)

- [x] **1. Real, Working Lonavala Geospatial Map:** Interactive Leaflet map centered on Lonavala-Khandala (18.755°N, 73.395°E), real coordinates, zoom, pan, reset, Topographic relief contour layer, and selectable location markers.
- [x] **2. Local Tourist Danger Monitoring:** Bhushi Dam, Kune Falls, Tiger Point, Lion's Point, and Rajmachi Trek Route with transparently labelled live, modelled, or unavailable status and upstream catchment surge analysis.
- [x] **3. Landslide-Prone Corridors:** Georeferenced segments along the Mumbai–Pune Expressway (Amrutanjan Bridge, Adoshi Tunnel) and Central Railway Bhor Ghat (Monkey Hill, Thakurwadi), explicitly distinguishing natural rockfall from traffic/freight accidents.
- [x] **4. Actual Terrain Intelligence:** Real digital elevation model metrics (SRTM 30m / Copernicus DEM): slope angles (6.5° to 46°), elevation (410m to 780m MSL), upstream catchment basins (1.2 to 14.2 km²), and drainage proximity.
- [x] **5. Rainfall & Soil Saturation:** Recent rainfall (1h, 3h, 24h, 48h accumulation), forecast precipitation, soil saturation % (FDR probe / Antecedent Precipitation Index), observation source, and freshness timestamps.
- [x] **6. Hyperlocal Risk Model:** Calibrated risk classifications: Low (0-25), Moderate (25-55), High (55-78), Very High (78-100), with local perturbation (SHAP-proxy) feature importance weights and uncertainty indicators.
- [x] **7. Lonavala Incident History:** Sourced, dated historical catalog including the June 30, 2024 Bhushi Dam waterfall surge tragedy (5 fatalities, Times of India / Pune Police records), July 2025 Expressway boulder falls, July 2026 Patan escarpment fissures, and February 2026 Adoshi hazardous tanker stoppage.
- [x] **8. Safe Action & Evacuation Support:** Verified disaster relief shelters (Lonavala Municipal Council Hall, Khandala ZP School, Ryewood Administrative Complex), official contacts (Pune DDMA 1077, Lonavala Police 02114-273033, Highway Patrol 9822498224), and survival guidelines.
- [x] **9. Tourist & Resident Interfaces:** Full trilingual support (**मराठी (mr)**, **English (en)**, **हिंदी (hi)**), public citizen view, tourist spot-check directory, and comprehensive authority control room dashboard.
- [x] **10. Historical Storm Replay & Simulator:** 24-hour storm progression timeline slider (July 2026 event) + interactive "What If the Storm Intensifies?" scenario simulator + 1-click deterministic 3-location comparison.
- [x] **11. Offline Resilience:** Fully client-side cached dataset fallbacks, offline status banner, and graceful error handling if backend or sensors disconnect.
- [x] **12. Responsible Alerting:** Official Government Warnings (IMD / NDMA) strictly segregated from AI-generated platform advisories; Common Alerting Protocol (CAP v1.2) XML exporter; authority draft-and-approve moderation audit workflow.

---

## 3. Technology Stack & Architecture

```
┌────────────────────────────────────────────────────────────────┐
│               FRONTEND (React 19 + TypeScript + Vite)          │
│  - Leaflet Map with OpenTopoMap / OSM Relief Tiles             │
│  - Trilingual UI (मराठी / English / हिंदी)                     │
│  - 10 Application Modules: Home, Map, Spot-Check, Corridors,   │
│    Alerts, Incidents, Safety, Replay, Authority, Research,     │
│    About Mission                                               │
└──────────────────────────────┬─────────────────────────────────┘
                               │ REST Proxy /api/*
┌──────────────────────────────▼─────────────────────────────────┐
│               BACKEND (Python 3.14 + FastAPI + Pydantic)       │
│  - RESTful Endpoints with full OpenAPI Swagger documentation   │
│  - Geotechnical Ingestion & Spatial Bounds Validation          │
│  - CORS Middleware, Audit Logging, CAP XML Serializer          │
└──────────────────────────────┬─────────────────────────────────┘
                               │
┌──────────────────────────────▼─────────────────────────────────┐
│               AI / ML PIPELINE (NumPy + Geotechnical Physics)  │
│  - Sahyadri-GeoRisk Ensemble (v2.1)                            │
│  - Landslide Factor of Safety (FS) & Basalt Overburden Shear   │
│  - Hydrograph Catchment Convergence Model                      │
│  - Platt Sigmoid Calibration & SHAP-Proxy Perturbation Weights │
└────────────────────────────────────────────────────────────────┘
```

---

## 4. Getting Started & Running Locally

### Prerequisites
- **Node.js**: v18+ (verified on v24.20.0)
- **Python**: v3.10+ (verified on v3.14.3)

### Installation

1. **Clone repository & navigate to folder:**
   ```bash
   cd c:\Users\pawar\OneDrive\Desktop\SAHYADRUSHTI
   ```

2. **Backend dependencies (FastAPI, Uvicorn, NumPy):**
   ```bash
   python -m pip install fastapi uvicorn pydantic numpy
   ```

3. **Frontend dependencies (React, Vite, Leaflet, Lucide):**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Full-Stack Application

1. **Start the FastAPI Backend Server:**
   ```bash
   python run_backend.py
   ```
   *Backend will start on `http://127.0.0.1:8000`.*  
   *API Swagger Docs available at `http://127.0.0.1:8000/docs`.*

2. **Start the Vite Frontend Development Server (in a separate terminal):**
   ```bash
   cd frontend
   npm run dev
   ```
   *Frontend will open on `http://127.0.0.1:5173/`.*

3. **Build Frontend for Production:**
   ```bash
   cd frontend
   npm run build
   ```

---

## 5. 3-Minute Hackathon Judge Demo Walkthrough

1. **Open `http://127.0.0.1:5173/`:**
   - Note the Sahyadri branding, Devanagari typography (`सह्यादृष्टी AI`), and official IMD Orange Alert notification.
2. **Click "⚡ DEMO MODE" in the top navbar:**
   - Opens the **Deterministic 3-Location Comparison**.
   - Show how a uniform 160mm rainfall produces:
     * *Location A (Town):* **Low (24/100)** due to flat 6.5° slope.
     * *Location B (Amrutanjan):* **Critical Landslide (82/100)** due to 36.5° cutting & 86% saturated basalt overburden.
     * *Location C (Bhushi Dam):* **High Flash-Surge (78/100)** due to upstream 4.8 km² catchment convergence.
3. **Explore the "हायपरलोकल नकाशा" (Map):**
   - Click on the Topo Relief button to observe the Sahyadri contours.
   - Click on **Bhushi Dam & Waterfall Catchment** marker. Observe the side panel display: 24.5° slope, 4.8 km² catchment, 74/100 flash flood index, and Section 144 restrictions.
4. **Visit "पर्यटन स्थळ तपासणी" (Spot-Check):**
   - Review tourist safety guidelines for Kune Falls, Tiger Point, Lion's Point, and Rajmachi trail.
5. **Visit "प्रशासन कक्ष" (Authority Desk):**
   - View escalating hotspots table, sensor health status, crowdsourced incident moderation queue, and CAP-format alert composer.
6. **Switch Languages (मराठी ↔ EN ↔ हिंदी):**
   - Experience the localized disaster risk communication.

---

## 6. Authoritative Data Provenance & Limitations

- **Topography & Elevation:** NASA SRTM 30m / Copernicus DEM.
- **Meteorology:** India Meteorological Department (IMD) Regional Radar & Meso-scale AWS Network.
- **Geotechnical Principles:** Based on Deccan Trap Basalt Overburden Shear Failure regimes and Caine (1980) rainfall-trigger thresholds ($I = \alpha D^{-\beta}$).
- **Historical Incidents:** Verified through Pune Rural Police, DDMA Pune, MSRDC, and Central Railway press logs.
- **Transparency Statement:** Field IoT sensors and in-situ FDR soil moisture stations are marked **[SIMULATED]** for this prototype. Official warnings are explicitly distinguished from model-generated advisories.
