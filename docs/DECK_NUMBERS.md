# Deck Numbers & Live Platform Measurements
### Verified Read-Only Telemetry from Live Backend API (`submit-fix`)
**Model Version:** `Sahyadri-GeoRisk-v3.0`  
**Query Timestamp:** 2026-11-08T12:04:30+05:30  
**Attribution Note:** All numbers below were retrieved live from the running FastAPI application and local Copernicus GLO-30 dataset. No figures from memory or previous reports.

---

## 1. Terrain Evidence Table (Copernicus GLO-30 DEM)
Source: `data/dem_check_extended.csv`

| Metric | Lonavala Civic Center (`lonavala_town`) | Amrutanjan Bridge / Bhor Ghat (`khandala_expressway`) | Physical Significance |
| :--- | :---: | :---: | :--- |
| **Point Coordinates** | `[18.7500, 73.4050]` | `[18.7611, 73.3644]` | Urban town plateau vs 6-lane mountain expressway pass |
| **GLO-30 Elevation** | $626.5\text{ m}$ | $551.9\text{ m}$ | $74.6\text{ m}$ elevation step-down into Bhor Ghat |
| **Point Slope ($Slope_{pt}$)** | $1.3^\circ$ | $3.6^\circ$ | Both point pins fall on flat infrastructure surfaces |
| **Steepest Slope within 60m** | $4.7^\circ$ | **$38.1^\circ$** | Highway road cut rises steeply within 60m of corridor |
| **Steepest Slope within 300m** | $19.4^\circ$ | **$51.1^\circ$** | Extreme escarpment rock scarp towering over expressway |
| **Vertical Relief within 300m** | $33.8\text{ m}$ | **$180.0\text{ m}$** | Massive gravitational potential energy above expressway cut |

---

## 2. Same Storm, Different Risk (/api/compare)
Endpoint: `GET /api/compare?rain_24h_mm=150.0&antecedent_mm={W}`  
Evaluates all 12 pilot locations under identical hypothetical 150mm/24h rainfall across three distinct antecedent wetness states:

### A. Dry Antecedent State ($W = 15.0\text{ mm}$, Profile Saturation $\approx 47\%$)
- **Score Differential:** $63\text{ points}$ (Max: 75, Min: 12)
- **Top 5 Vulnerable:**
  1. `valvan_dam`: Score **75** (Level: high, Hazard: waterlogging)
  2. `bhushi_dam`: Score **57** (Level: high, Hazard: flash_flood)
  3. `tiger_point`: Score **56** (Level: high, Hazard: landslide)
  4. `monkey_hill`: Score **53** (Level: moderate, Hazard: landslide)
  5. `lions_point`: Score **46** (Level: moderate, Hazard: landslide)
- **Baseline Comparison:** `khandala_expressway` scores **34** (moderate); `lonavala_town` scores **22** (low).

### B. Moderate Antecedent State ($W = 120.0\text{ mm}$, Profile Saturation $\approx 63\%$)
- **Score Differential:** $77\text{ points}$ (Max: 95, Min: 18)
- **Top 5 Vulnerable:**
  1. `valvan_dam`: Score **95** (Level: very_high, Hazard: waterlogging)
  2. `bhushi_dam`: Score **71** (Level: high, Hazard: flash_flood)
  3. `tiger_point`: Score **63** (Level: high, Hazard: landslide)
  4. `monkey_hill`: Score **60** (Level: high, Hazard: landslide)
  5. `lions_point`: Score **54** (Level: moderate, Hazard: landslide)
- **Baseline Comparison:** `khandala_expressway` scores **42** (moderate); `lonavala_town` scores **27** (moderate).

### C. Wet / Saturated Antecedent State ($W = 260.0\text{ mm}$, Profile Saturation $\approx 84\%$)
- **Score Differential:** $62\text{ points}$ (Max: 96, Min: 34)
- **Top 5 Vulnerable:**
  1. `bhushi_dam`: Score **96** (Level: very_high, Hazard: flash_flood) [Capped at 96]
  2. `valvan_dam`: Score **96** (Level: very_high, Hazard: waterlogging) [Capped at 96]
  3. `tiger_point`: Score **80** (Level: very_high, Hazard: landslide)
  4. `monkey_hill`: Score **78** (Level: very_high, Hazard: landslide)
  5. `lions_point`: Score **73** (Level: high, Hazard: landslide)
- **Baseline Comparison:** `khandala_expressway` reaches **64** (high); `lonavala_town` remains at **34** (moderate).

---

## 3. Replay Time Series Progression (July 1 to July 8, 2026)
Source: `GET /api/replay` (ERA5/ECMWF coupled archive, 9–11 km grid resolution)  
*Attribution Note: Reanalysis-based archive; peak localized convective values in steep ghats are suspected underestimates to be calibrated against IMD station data.*

| Timestamp | Cumulative 24h Rain (mm) | Drained Store $W(t)$ (mm) | Lonavala Civic Center (`lonavala_town`) | Amrutanjan Bridge (`khandala_expressway`) | Differential |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **2026-07-01T00:00** | 44.6 | 59.1 | 12 (Low) | 56 (Moderate) | +44 |
| **2026-07-01T12:00** | 51.8 | 70.6 | 11 (Low) | 55 (Moderate) | +44 |
| **2026-07-02T00:00** | 72.8 | 100.1 | 14 (Low) | 57 (Moderate) | +43 |
| **2026-07-02T12:00** | 54.1 | 88.2 | 13 (Low) | 56 (Moderate) | +43 |
| **2026-07-03T00:00** | 22.2 | 86.3 | 12 (Low) | 57 (Moderate) | +45 |
| **2026-07-03T12:00** | 46.9 | 99.0 | 14 (Low) | 59 (Moderate) | +45 |
| **2026-07-04T00:00** | 54.5 | 102.1 | 14 (Low) | 58 (Moderate) | +44 |
| **2026-07-04T12:00** | 71.4 | 128.7 | 22 (Low) | 66 (High) | +44 |
| **2026-07-05T00:00** | 80.5 | 134.2 | 19 (Low) | 65 (High) | +46 |
| **2026-07-05T12:00** | 113.2 | 184.1 | 27 (Moderate) | 71 (High) | +44 |
| **2026-07-06T00:00** | 182.8 | 244.7 | 42 (Moderate) | 83 (Very High) | +41 |
| **2026-07-06T12:00** | 187.3 | 279.9 | 44 (Moderate) | **85 (Very High)** | +41 |
| **2026-07-07T00:00** | 189.8 | 321.6 | 45 (Moderate) | **86 (Very High)** | +41 |
| **2026-07-07T12:00** | 135.9 | 291.6 | 38 (Moderate) | 81 (Very High) | +43 |
| **2026-07-08T00:00** | 83.1 | 287.0 | 44 (Moderate) | 83 (Very High) | +39 |
| **2026-07-08T12:00** | 101.1 | 278.9 | 35 (Moderate) | 81 (Very High) | +46 |

---

## 4. Live API Response Fields Specification
Retrieved from live `/api/risk?lat=18.7611&lon=73.3644`:

- **Hyperlocal Evaluation Fields:**
  - `risk_score`: Relative physical risk index (0–100 integer)
  - `risk_level`: Severity class (`low`, `moderate`, `high`, `very_high`)
  - `score_capped`: Boolean indicating if score reached safety model ceiling (96 or 98)
  - `factor_of_safety`: Geotechnical infinite-slope Factor of Safety float ($FS$)
  - `susceptibility_class`: Static topographic category (`high_hazard_escarpment`, `moderate_hazard_slope`, `low_hazard_transition`, `low_relief_plain`)
  - `trigger_level`: Meteorological Caine trigger benchmark (`below`, `approaching`, `exceeding`)
  - `model_applicability`: Domain classification (`soil_slope`, `catchment_drainage_fluvial`, `rock_scarp_or_cut`)
  - `antecedent_store_w_mm`: Drained water volume $W(t)$ with $\tau=60\text{h}$
  - `contributing_factors`: Array of structured local factors with `factor`, `weight`, `direction`, and physical `description`.
  - `precautions`: Array of operational recommendations.
- **Action Guidance (Multilingual):**
  - `en`: Localized protective action advice in English.
  - `mr`: Localized protective action advice in Marathi (मराठी).
  - `hi`: Localized protective action advice in Hindi (हिन्दी).
- **Data Provenance & Disclaimers:**
  - `data_source`: `"Copernicus GLO-30 DEM & Open-Meteo API"`
  - `model_version`: `"Sahyadri-GeoRisk-v3.0"`
  - `uncalibrated_assumption`: `"Pore pressure driven by W(t) with tau=60h and n_drain=0.15 over z=2.2m saprolite; Caine (1980) global empirical rainfall trigger"`
  - `disclaimer`: `"Pilot-stage physics-informed risk index (0-100), not calibrated against field sensors."`
