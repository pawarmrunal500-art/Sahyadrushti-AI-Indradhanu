# DEM Verification Report | SAHYADRUSHTI AI (PralaySense AI)

## 1. Provenance & Dataset Information
- **Dataset:** Copernicus GLO-30 Digital Elevation Model (`COPERNICUS/DEM/GLO30`) via Google Earth Engine.
- **Spatial Resolution:** 1 arc-second (~30 meters).
- **Run Date:** 2026-11-08.
- **Source Files:** `data/dem_check.csv` (Point & 60m focal max) and `data/dem_check_extended.csv` (Extended buffers: 150m, 300m focal max, 300m relief).

> [!IMPORTANT]
> **Authoritative Elevation Baseline:**
> All elevation, slope, and terrain relief metrics are validated strictly against Copernicus GLO-30 (GEE export). Open-Meteo elevation stencils or coarse reanalysis rasters are deprecated.
> **Honesty & Integrity Policy:** Seed coordinates, elevations, and slopes are never silently overwritten. All discrepancies are categorized and documented with explicit user follow-up items (`TODO-USER`).

---

## 2. Evaluation Rules & Criteria
1. **Elevation Mismatch:** $|Seed Elevation - DEM Elevation| > 50\text{ m}$. Indicates either coordinates or seed elevations need field ground-truthing.
2. **Slope Mismatch:** $|Seed Slope - DEM Slope_{max60m}| > 15^\circ$. Indicates point coordinates fall on a shelf or bench, while escarpment slope is located within immediate or extended proximity.
3. **Terrain Buffer Analysis (Extended):**
   - $Slope_{pt}$: Slope angle exactly at the 30m grid cell containing the coordinates.
   - $Slope_{max60m}$: Steepest 30m cell within 60 meters.
   - $Slope_{max150m}$: Steepest 30m cell within 150 meters.
   - $Slope_{max300m}$: Steepest 30m cell within 300 meters.
   - $Relief_{300m}$: Total vertical elevation difference (Max - Min) within a 300-meter radius.

---

## 3. Comprehensive Verification Matrix (Extended Analysis)

| Location ID | Stored Lat, Lon | Seed Elev (m) | DEM Elev (m) | $\Delta$ Elev (m) | Seed Slope ($^\circ$) | DEM Pt ($^\circ$) | Max 60m ($^\circ$) | Max 150m ($^\circ$) | Max 300m ($^\circ$) | Relief 300m (m) | Status Classification |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **bhushi_dam** | 18.7364, 73.3965 | 638.0 | 622.9 | -15.1 | 24.5 | 1.9 | 6.5 | 10.0 | 10.7 | 16.9 | **slope mismatch** (water body basin) |
| **kune_falls** | 18.7618, 73.3854 | 622.0 | 537.2 | **-84.8** | 38.0 | 5.1 | 11.5 | 25.2 | 27.3 | 65.9 | **elevation mismatch** (waterfall drop) |
| **tiger_point** | 18.7183, 73.3831 | 725.0 | 627.7 | **-97.3** | 46.0 | 8.4 | 10.8 | 21.9 | **36.9** | 125.2 | **elevation mismatch** (cliff edge) |
| **lions_point** | 18.7112, 73.3860 | 718.0 | 729.6 | +11.6 | 41.0 | 13.0 | 25.2 | **32.8** | **33.0** | 146.0 | **slope mismatch** (viewpoint plateau) |
| **rajmachi_route** | 18.8250, 73.3980 | 780.0 | 626.3 | **-153.7** | 32.0 | 11.7 | 19.1 | 28.4 | **33.7** | 125.7 | **elevation mismatch** (ridge trail) |
| **khandala_expressway** | 18.7611, 73.3644 | 585.0 | 551.9 | -33.1 | 36.5 | 3.6 | **38.1** | **44.1** | **51.1** | **180.0** | **OK** (engineered rock cutting) |
| **adoshi_tunnel** | 18.7850, 73.3350 | 490.0 | 162.6 | **-327.4** | 31.0 | 6.9 | 17.1 | 26.7 | **29.6** | 134.5 | **elevation mismatch** (ghat descent) |
| **monkey_hill** | 18.7750, 73.3500 | 540.0 | 109.9 | **-430.1** | 44.0 | 12.1 | **31.0** | **34.5** | **41.4** | 100.7 | **elevation mismatch** (railway cutting) |
| **thakurwadi** | 18.8252, 73.3421 | 410.0 | 141.6 | **-268.4** | 35.0 | **30.6** | **33.6** | **33.6** | **33.6** | **175.4** | **elevation mismatch** (foothill transition) |
| **patan_village** | 18.7303, 73.3855 | 665.0 | 622.7 | -42.3 | 29.0 | 1.2 | 2.3 | 6.1 | 18.8 | 26.5 | **slope mismatch** (flat village shelf) |
| **valvan_dam** | 18.7600, 73.4280 | 625.0 | 619.8 | -5.2 | 14.0 | 2.8 | 5.7 | 7.8 | 8.4 | 10.8 | **OK** (reservoir impoundment) |
| **lonavala_town** | 18.7500, 73.4050 | 624.0 | 626.5 | +2.5 | 6.5 | 1.3 | 4.7 | 16.4 | 19.4 | 33.8 | **OK** (urban valley plateau) |

---

## 4. Key Diagnostic Insights from Extended Buffers

1. **Escarpment Slope Capture in Extended Buffers:**
   - At **khandala_expressway**, the point slope is only $3.6^\circ$ (roadbed asphalt), but within 60m slope rises to $38.1^\circ$, within 150m to $44.1^\circ$, and within 300m reaches $51.1^\circ$ with **180m vertical relief**. This physically confirms the massive engineered rock cut above the expressway.
   - At **tiger_point** and **lions_point**, coordinates sit on tourist viewing platforms ($8.4^\circ$ and $13.0^\circ$), but the terrain drops precipitously into the Konkan gorge with $33.0^\circ - 36.9^\circ$ slopes and $>125\text{m}$ relief within 300m.
   - At **monkey_hill**, the 300m slope reaches $41.4^\circ$, verifying steep railway cuttings.

2. **The Patan Village Discrepancy:**
   - Seed slope is $29.0^\circ$, but DEM slope at point is $1.2^\circ$, 60m is $2.3^\circ$, 150m is $6.1^\circ$, and 300m relief is only $26.5\text{m}$.
   - **Conclusion:** Coordinates `[18.7303, 73.3855]` place the point directly in the flat agricultural valley/village center rather than on the steep escarpment backing the village. Marked as `TODO-USER`.

3. **Bhor Ghat Elevation Step-Down:**
   - Sites `monkey_hill` (110m), `adoshi_tunnel` (163m), and `thakurwadi` (142m) sit at the base / lower flanks of the Bhor Ghat scarp, whereas seed elevations (410m–540m) reflected the mid-to-upper ghat pass. Marked as `TODO-USER`.
