# DEM Verification Report | SAHYADRUSHTI AI

## 1. Provenance & Dataset Information
- **Dataset:** Copernicus GLO-30 Digital Elevation Model (`COPERNICUS/DEM/GLO30`) via Google Earth Engine.
- **Spatial Resolution:** 1 arc-second (~30 meters).
- **Extraction Method:** Point sampling at stored coordinates (`elev`, `slope_pt`) and focal maximum filter over a 60-meter radius (`slope_max_60m`).
- **Run Date:** 2026-11-08.
- **Source File:** `data/dem_check.csv` (GEE export).

> [!IMPORTANT]
> **Invalidation of Previous Open-Meteo Elevation Stencil:**
> Any earlier elevation and slope comparison performed using the Open-Meteo elevation endpoint is **INVALID**. The Open-Meteo endpoint used a coarse reanalysis raster (likely 90m or interpolated reanalysis grid) where a local 30m centered difference stencil produced artifacts (including 0.0° slopes at Lion's Point and Rajmachi). All authoritative terrain benchmarks must exclusively use Google Earth Engine Copernicus GLO-30.

## 2. Evaluation Rules
1. **Elevation Status:** Flagged as **`elevation mismatch`** if `|seed elevation - DEM elevation| > 50 m`. *This indicates either the stored coordinates or the seed elevation are wrong; no automated assumptions are made as to which.*
2. **Slope Status:**
   - **`supported`**: `slope_max_60m` is within 8° of `seed slope`.
   - **`unsupported at 30 m`**: `slope_max_60m` is more than 8° below `seed slope`. A 30m DEM cell averages elevation over a 900 m² footprint and cannot resolve rock cliffs, vertical scarps, or roadside retaining cuts narrower than ~30 m. Documented as *cannot be verified at this resolution* (not 'wrong').
   - **`steeper than seed`**: `slope_max_60m` is more than 8° steeper than `seed slope`.
3. **Non-Destructive Replacement Policy:** No stored seed values are overwritten. Proposed replacements are presented in separate columns and explicitly tagged as `(DEM-derived)`.

## 3. Comprehensive DEM Comparison Table

| Location ID | Coordinates (Lat, Lon) | Seed Elev (m) | DEM Elev (m) | Diff (m) | Elev Status | Seed Slope (°) | DEM Slope Pt (°) | DEM Slope Max 60m (°) | Slope Status | Proposed Elevation | Proposed Slope |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **bhushi_dam** | 18.7364, 73.3965 | 638.0 | 622.9 | -15.1 | `consistent (<= 50m)` | 24.5° | 1.9° | 6.5° | `unsupported at 30 m` | 622.9 m (DEM-derived) | Keep seed 24.5° (cannot be verified at 30m; cliff narrower than ~30m) |
| **kune_falls** | 18.7618, 73.3854 | 622.0 | 537.2 | -84.8 | `elevation mismatch` | 38.0° | 5.1° | 11.5° | `unsupported at 30 m` | 537.2 m (DEM-derived) | Keep seed 38.0° (cannot be verified at 30m; cliff narrower than ~30m) |
| **tiger_point** | 18.7077, 73.3881 | 725.0 | 627.7 | -97.3 | `elevation mismatch` | 46.0° | 8.4° | 10.8° | `unsupported at 30 m` | 627.7 m (DEM-derived) | Keep seed 46.0° (cannot be verified at 30m; cliff narrower than ~30m) |
| **lions_point** | 18.7122, 73.3912 | 718.0 | 729.6 | +11.6 | `consistent (<= 50m)` | 41.0° | 13.0° | 25.2° | `unsupported at 30 m` | 729.6 m (DEM-derived) | Keep seed 41.0° (cannot be verified at 30m; cliff narrower than ~30m) |
| **rajmachi_route** | 18.8262, 73.4005 | 780.0 | 626.3 | -153.7 | `elevation mismatch` | 32.0° | 11.7° | 19.1° | `unsupported at 30 m` | 626.3 m (DEM-derived) | Keep seed 32.0° (cannot be verified at 30m; cliff narrower than ~30m) |
| **khandala_expressway** | 18.7758, 73.3592 | 585.0 | 551.9 | -33.1 | `consistent (<= 50m)` | 36.5° | 3.6° | 38.1° | `supported` | 551.9 m (DEM-derived) | 38.1° (DEM-derived) |
| **adoshi_tunnel** | 18.7792, 73.3441 | 490.0 | 162.6 | -327.4 | `elevation mismatch` | 31.0° | 6.9° | 17.1° | `unsupported at 30 m` | 162.6 m (DEM-derived) | Keep seed 31.0° (cannot be verified at 30m; cliff narrower than ~30m) |
| **monkey_hill** | 18.7845, 73.3610 | 540.0 | 109.9 | -430.1 | `elevation mismatch` | 44.0° | 12.1° | 31.0° | `unsupported at 30 m` | 109.9 m (DEM-derived) | Keep seed 44.0° (cannot be verified at 30m; cliff narrower than ~30m) |
| **thakurwadi** | 18.8023, 73.3458 | 410.0 | 141.6 | -268.4 | `elevation mismatch` | 35.0° | 30.6° | 33.6° | `supported` | 141.6 m (DEM-derived) | 33.6° (DEM-derived) |
| **patan_village** | 18.7291, 73.4350 | 665.0 | 622.7 | -42.3 | `consistent (<= 50m)` | 29.0° | 1.2° | 2.3° | `unsupported at 30 m` | 622.7 m (DEM-derived) | Keep seed 29.0° (cannot be verified at 30m; cliff narrower than ~30m) |
| **valvan_dam** | 18.7634, 73.4215 | 625.0 | 619.8 | -5.2 | `consistent (<= 50m)` | 14.0° | 2.8° | 5.7° | `unsupported at 30 m` | 619.8 m (DEM-derived) | Keep seed 14.0° (cannot be verified at 30m; cliff narrower than ~30m) |
| **lonavala_town** | 18.7512, 73.4082 | 624.0 | 626.5 | +2.5 | `consistent (<= 50m)` | 6.5° | 1.3° | 4.7° | `supported` | 626.5 m (DEM-derived) | 4.7° (DEM-derived) |

## 4. Detailed Slope Assessment & Resolution Limits

### bhushi_dam
- **Coordinates:** `18.7364, 73.3965`
- **Elevation:** Seed = 638.0m | DEM GLO-30 = 622.9m (Difference: -15.1m) -> `consistent (<= 50m)`
- **Slope:** Seed = 24.5° | Point = 1.9° | Max within 60m = 6.5° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (6.5°) is 18.0° below seed (24.5°); cannot be verified at this resolution.

### kune_falls
- **Coordinates:** `18.7618, 73.3854`
- **Elevation:** Seed = 622.0m | DEM GLO-30 = 537.2m (Difference: -84.8m) -> `elevation mismatch`
- **Slope:** Seed = 38.0° | Point = 5.1° | Max within 60m = 11.5° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (11.5°) is 26.5° below seed (38.0°); cannot be verified at this resolution.

### tiger_point
- **Coordinates:** `18.7077, 73.3881`
- **Elevation:** Seed = 725.0m | DEM GLO-30 = 627.7m (Difference: -97.3m) -> `elevation mismatch`
- **Slope:** Seed = 46.0° | Point = 8.4° | Max within 60m = 10.8° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (10.8°) is 35.2° below seed (46.0°); cannot be verified at this resolution.

### lions_point
- **Coordinates:** `18.7122, 73.3912`
- **Elevation:** Seed = 718.0m | DEM GLO-30 = 729.6m (Difference: +11.6m) -> `consistent (<= 50m)`
- **Slope:** Seed = 41.0° | Point = 13.0° | Max within 60m = 25.2° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (25.2°) is 15.8° below seed (41.0°); cannot be verified at this resolution.

### rajmachi_route
- **Coordinates:** `18.8262, 73.4005`
- **Elevation:** Seed = 780.0m | DEM GLO-30 = 626.3m (Difference: -153.7m) -> `elevation mismatch`
- **Slope:** Seed = 32.0° | Point = 11.7° | Max within 60m = 19.1° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (19.1°) is 12.9° below seed (32.0°); cannot be verified at this resolution.

### khandala_expressway
- **Coordinates:** `18.7758, 73.3592`
- **Elevation:** Seed = 585.0m | DEM GLO-30 = 551.9m (Difference: -33.1m) -> `consistent (<= 50m)`
- **Slope:** Seed = 36.5° | Point = 3.6° | Max within 60m = 38.1° -> `supported`
- **Analysis:** DEM 60m focal max (38.1°) within ±8° of seed (36.5°).

### adoshi_tunnel
- **Coordinates:** `18.7792, 73.3441`
- **Elevation:** Seed = 490.0m | DEM GLO-30 = 162.6m (Difference: -327.4m) -> `elevation mismatch`
- **Slope:** Seed = 31.0° | Point = 6.9° | Max within 60m = 17.1° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (17.1°) is 13.9° below seed (31.0°); cannot be verified at this resolution.

### monkey_hill
- **Coordinates:** `18.7845, 73.361`
- **Elevation:** Seed = 540.0m | DEM GLO-30 = 109.9m (Difference: -430.1m) -> `elevation mismatch`
- **Slope:** Seed = 44.0° | Point = 12.1° | Max within 60m = 31.0° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (31.0°) is 13.0° below seed (44.0°); cannot be verified at this resolution.

### thakurwadi
- **Coordinates:** `18.8023, 73.3458`
- **Elevation:** Seed = 410.0m | DEM GLO-30 = 141.6m (Difference: -268.4m) -> `elevation mismatch`
- **Slope:** Seed = 35.0° | Point = 30.6° | Max within 60m = 33.6° -> `supported`
- **Analysis:** DEM 60m focal max (33.6°) within ±8° of seed (35.0°).

### patan_village
- **Coordinates:** `18.7291, 73.435`
- **Elevation:** Seed = 665.0m | DEM GLO-30 = 622.7m (Difference: -42.3m) -> `consistent (<= 50m)`
- **Slope:** Seed = 29.0° | Point = 1.2° | Max within 60m = 2.3° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (2.3°) is 26.7° below seed (29.0°); cannot be verified at this resolution.

### valvan_dam
- **Coordinates:** `18.7634, 73.4215`
- **Elevation:** Seed = 625.0m | DEM GLO-30 = 619.8m (Difference: -5.2m) -> `consistent (<= 50m)`
- **Slope:** Seed = 14.0° | Point = 2.8° | Max within 60m = 5.7° -> `unsupported at 30 m`
- **Analysis:** DEM 60m focal max (5.7°) is 8.3° below seed (14.0°); cannot be verified at this resolution.

### lonavala_town
- **Coordinates:** `18.7512, 73.4082`
- **Elevation:** Seed = 624.0m | DEM GLO-30 = 626.5m (Difference: +2.5m) -> `consistent (<= 50m)`
- **Slope:** Seed = 6.5° | Point = 1.3° | Max within 60m = 4.7° -> `supported`
- **Analysis:** DEM 60m focal max (4.7°) within ±8° of seed (6.5°).
