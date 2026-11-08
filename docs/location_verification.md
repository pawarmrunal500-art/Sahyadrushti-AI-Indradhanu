# Location Coordinates & Elevation Verification | SAHYADRUSHTI AI (PralaySense AI)

## 1. Elevation Mismatch Summary (|Seed Elev - DEM Elev| > 50 m)
The following locations exhibited elevation discrepancies greater than 50 meters between the initial seed configuration and the Copernicus GLO-30 DEM. **Either the coordinates or the seed elevation require ground truth confirmation. In accordance with platform integrity rules, seed data has NOT been modified.**

| Location ID | Stored Lat, Lon | Seed Elev (m) | DEM Elev (m) | Discrepancy Magnitude | Diagnostic Assessment |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **monkey_hill** | 18.7750, 73.3500 | 540.0 m | 109.9 m | **-430.1 m** | Bhor Ghat railway descent: coordinates locate the track level on the lower gorge flank, whereas seed elevation represented the upper ghat crest. |
| **adoshi_tunnel** | 18.7850, 73.3350 | 490.0 m | 162.6 m | **-327.4 m** | Highway tunnel approach near Khalapur/Khopoli exit: coordinates reflect the lower Konkan approach grade. |
| **thakurwadi** | 18.8252, 73.3421 | 410.0 m | 141.6 m | **-268.4 m** | Base of Bhor Ghat railway section near Thakurwadi cabin: coordinates sit at 142m in the valley floor. |
| **rajmachi_route** | 18.8250, 73.3980 | 780.0 m | 626.3 m | **-153.7 m** | Forest trail traverse below the Rajmachi fort plateau (Shrivardhan / Manaranjan peaks reach ~800m). |
| **tiger_point** | 18.7183, 73.3831 | 725.0 m | 627.7 m | **-97.3 m** | Cliff viewing platform edge over Khandala/Amba valley gorge. |
| **kune_falls** | 18.7618, 73.3854 | 622.0 m | 537.2 m | **-84.8 m** | Base of upper tier waterfall plunge pool in deep ravine. |

---

## 2. Actionable User Verification Checklist (TODO-USER)

> [!CAUTION]
> The items below represent spatial ambiguities in seed configuration that must be confirmed with local district authorities (SDM Maval / Raigad Disaster Management) or field GPS surveys.

- [ ] **TODO-USER (Patan Village Coordinate Ambiguity):**
  - **Issue:** Stored coordinates `[18.7303, 73.3855]` show DEM point slope $1.2^\circ$ and 300m relief $26.5\text{m}$ (flat valley shelf), whereas seed slope is configured as $29.0^\circ$.
  - **Recommendation:** Confirm whether the monitoring target is the village residential center (`[18.7303, 73.3855]`, low slope) or the vulnerable hillside escarpment immediately east/south of Patan (`~18.7285, 73.3895`, steep colluvium slope).

- [ ] **TODO-USER (Bhor Ghat Elevation & Administrative District Assignment):**
  - **Issue:** Sites `monkey_hill` (109.9m), `adoshi_tunnel` (162.6m), and `thakurwadi` (141.6m) sit below 200m elevation.
  - **Recommendation:** Verify whether these sites are under Pune District (Maval Taluka) or Raigad District (Khalapur Taluka) disaster management jurisdiction for alert dispatch routing.

- [ ] **TODO-USER (IMD Weather Station Benchmark Calibration):**
  - **Issue:** Open-Meteo reanalysis archive (9–11 km grid) underestimates localized orographic extremes in the ghats.
  - **Recommendation:** When official IMD AWS station data for Lonavala / Khandala becomes available, calibrate the `bias_multiplier` (currently default `1.0`) against observed 24h totals.
