# Location Coordinates & Elevation Verification | SAHYADRUSHTI AI

## 1. Elevation Mismatch Summary (|Seed Elev - DEM Elev| > 50 m)
The following locations exhibited elevation discrepancies greater than 50 meters between the initial seed configuration and the Copernicus GLO-30 DEM. **Either the coordinates or the seed elevation are wrong. These require manual verification against ground truth maps before operational sign-off.**

| Location ID | Stored Lat, Lon | Seed Elev (m) | DEM Elev (m) | Discrepancy Magnitude | Diagnostic Assessment |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **monkey_hill** | 18.7845, 73.3610 | 540.0 m | 109.9 m | **430.1 m** (-430.1 m) | Bhor Ghat railway/highway descent: seed elevation appears to reference the high plateau crest/ridge, whereas coordinates point to the railway/expressway grade on the gorge floor. |
| **adoshi_tunnel** | 18.7792, 73.3441 | 490.0 m | 162.6 m | **327.4 m** (-327.4 m) | Bhor Ghat railway/highway descent: seed elevation appears to reference the high plateau crest/ridge, whereas coordinates point to the railway/expressway grade on the gorge floor. |
| **thakurwadi** | 18.8023, 73.3458 | 410.0 m | 141.6 m | **268.4 m** (-268.4 m) | Bhor Ghat railway/highway descent: seed elevation appears to reference the high plateau crest/ridge, whereas coordinates point to the railway/expressway grade on the gorge floor. |
| **rajmachi_route** | 18.8262, 73.4005 | 780.0 m | 626.3 m | **153.7 m** (-153.7 m) | Trailhead/pass coordinate: seed elevation (780m) references Rajmachi Fort / Manaranjan peak rather than the valley saddle coordinate (626m). |
| **tiger_point** | 18.7077, 73.3881 | 725.0 m | 627.7 m | **97.3 m** (-97.3 m) | Tourist viewpoint escarpment: seed elevation (725m) vs DEM (628m) shows coordinates fall slightly west into the canyon floor rather than on the viewing deck. |
| **kune_falls** | 18.7618, 73.3854 | 622.0 m | 537.2 m | **84.8 m** (-84.8 m) | Waterfall plunge pool: seed elevation (622m) represents the upper cliff lip, whereas coordinates place it in the lower gorge (537m). |

## 2. Special Notice: Patan Village Coordinate Integrity
> [!WARNING]
> **Patan Village Coordinate Ground-Truth Requirement:**
> A landslide disaster was reported in Patan Village, Maval Taluka, around 2026-07-06. The back-test model evaluation and empirical validation depend directly upon these coordinates (`18.7303°N, 73.3855°E`).
> 
> **Discrepancy Note:** At the current stored coordinate, Copernicus GLO-30 DEM reports an elevation of 622.7 m and a 60m maximum slope of **2.3°** (essentially flat valley floor/farmland), whereas the seed slope is **29.0°** and historical records describe hillside/slope-toe detachment.
> 
> **Action Required:** Before running any definitive back-test or performance calibration, Patan Village coordinates MUST be verified and confirmed against official district disaster management maps, revenue village cadastre, or local disaster response records to confirm whether the point represents the residential settlement center or the specific failed hillside slope.

## 3. Location Verification Status Table
The table below pre-fills the stored coordinates and DEM measurements. The columns `Verified Against (Named Source)` and `Status` are reserved for human verification against survey maps, Survey of India toposheets, or GIS cadastres.

| Location ID | Stored Lat | Stored Lon | Seed Elev (m) | DEM Elev (m) | Elevation Mismatch Flag | Verified Against (Named Source) | Verification Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **bhushi_dam** | 18.7364 | 73.3965 | 638.0 | 622.9 | NO (<=50m) | | unverified |
| **kune_falls** | 18.7618 | 73.3854 | 622.0 | 537.2 | YES (>50m) | | unverified |
| **tiger_point** | 18.7077 | 73.3881 | 725.0 | 627.7 | YES (>50m) | | unverified |
| **lions_point** | 18.7122 | 73.3912 | 718.0 | 729.6 | NO (<=50m) | | unverified |
| **rajmachi_route** | 18.8262 | 73.4005 | 780.0 | 626.3 | YES (>50m) | | unverified |
| **khandala_expressway** | 18.7758 | 73.3592 | 585.0 | 551.9 | NO (<=50m) | | unverified |
| **adoshi_tunnel** | 18.7792 | 73.3441 | 490.0 | 162.6 | YES (>50m) | | unverified |
| **monkey_hill** | 18.7845 | 73.3610 | 540.0 | 109.9 | YES (>50m) | | unverified |
| **thakurwadi** | 18.8023 | 73.3458 | 410.0 | 141.6 | YES (>50m) | | unverified |
| **patan_village** | 18.7291 | 73.4350 | 665.0 | 622.7 | NO (<=50m) | | unverified |
| **valvan_dam** | 18.7634 | 73.4215 | 625.0 | 619.8 | NO (<=50m) | | unverified |
| **lonavala_town** | 18.7512 | 73.4082 | 624.0 | 626.5 | NO (<=50m) | | unverified |