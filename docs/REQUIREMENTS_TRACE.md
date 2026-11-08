# Requirements Traceability Matrix: PralaySense AI (SAHYADRUSHTI AI)

## Problem Statement to System Requirements Mapping

| ID | Requirement Area | System Capability / Feature | Implementation Reference | Status |
|:---|:---|:---|:---|:---|
| **R1** | **Multi-factor Local Risk** | Physics-informed geotechnical & hydrological engine evaluating slope, curvature, soil saturation (multi-layer), drainage, land cover, and rainfall pulses. | `backend/ml_engine.py`, `app/services/risk.py` | ACTIVE |
| **R2** | **Spatial Differentiation** | Distinct risk index at nearby locations receiving identical grid-cell rainfall (e.g., Lonavala Town flat vs Khandala steep slopes). | `backend/data_layer.py`, `backend/ml_engine.py` | ACTIVE |
| **R3** | **Continuous Time-Tracking** | Antecedent state $W(t)$ tracking, multi-day memory (48h, 72h, 7d), 12-hourly replay, and scheduled live refresh. | `app/services/weather.py`, `app/services/scheduler.py` | ACTIVE |
| **R4** | **Vulnerable Zone Identification** | Clear categorization of pilot locations into high/moderate/low susceptibility based on slope, DEM relief, and historical hazards. | `docs/dem_verification.md`, `backend/data_layer.py` | ACTIVE |
| **R5** | **Actionable Citizen & Authority Communication** | Multi-lingual actionable guidance (en/mr/hi), prioritized authority intervention queue, and standardized CAP 1.2 XML. | `app/routers/alerts.py`, `frontend/src/views/AuthorityView.tsx` | ACTIVE |
| **R6** | **Security & Integrity** | Strict JWT HS256 auth, RBAC (citizen/operator/approver/admin), four-eyes rule on alert publication, device key rotation, rate limiting. | `app/auth.py`, `app/routers/auth.py` | ACTIVE |
| **R7** | **Honesty & Transparency** | Clear labeling as "Risk Index (0-100)" rather than empirical probability; explicit disclaimers regarding uncalibrated parameters and GLO-30 DEM limitations. | `backend/schemas.py`, `README.md`, UI badges | ACTIVE |
| **R8** | **Extensibility & Modularity** | Additive schema architecture, modular bias correction layer, reproducible diagnostics, and station calibration readiness. | `backend/schemas.py`, `tests/test_contract.py` | ACTIVE |

---

## Diagnostic Check Harness Mapping (scripts/ps_check.py)
> [!NOTE]
> All checks in `scripts/ps_check.py` are internal sanity diagnostics. As documented in [`docs/CHANGES_AUDIT.md`](file:///c:/Documents/SAHYADRUSHTI_INDRADHANU/SAHYADRUSHTI/docs/CHANGES_AUDIT.md), code was modified interactively during development, so these checks must not be represented as independent field validation.

| Check | Name | Evaluation Basis | Status | Honesty & Limitations Note |
|:---|:---|:---|:---:|:---|
| **C1** | **Spatial Differentiation** | Max-Min score spread $\ge 30$, Lonavala Town $<$ Khandala Expressway under 150mm rain. | **PASS (Diagnostic)** | Spread is 47 points (16 to 63). Diagnostic check; code was modified while iterating, so this is not independent validation. |
| **C2** | **Antecedent Sensitivity** | Wet history ($W=250\text{mm}$, sat=85%) vs dry history ($W=10\text{mm}$, sat=40%) at 100mm 24h rain. | **PARTIAL** | 12/12 sites show higher risk when wet. Labeled PARTIAL because test sets $W$ and saturation directly rather than running distinct 14-day rainfall histories through the pipeline. |
| **C3** | **Continuous Time-Tracking** | Replay sequence contains $\ge 24$ timestamped frames, non-constant scores. | **PASS (Diagnostic)** | 34 frames across 17 days; Khandala Expressway exhibits 28 unique scores under model v3. |
| **C4** | **Actionable Communication** | Every location returns $\ge 3$ contributing factors and localized advice in en/mr/hi. | **PASS (Diagnostic)** | Multi-tier factors always evaluated for all 12 pilot locations. |
| **C5** | **Authority Governance** | Enforces Four-Eyes rule (HTTP 409 Conflict on self-approval) and generates CAP 1.2 XML. | **PASS (Diagnostic)** | Verified in unit and integration test suites. |
| **C6** | **Data Provenance & Flags** | Schema requires uncalibrated assumption and data origin indicators. | **PARTIAL** | Labeled PARTIAL because evidence was model fields in `PredictionResponse`, not provenance fields on every single raw telemetry response. |
| **C7** | **Calm Days Stability** | Maximum frame-to-frame score change $\le 25$ during consecutive quiet periods. | **PASS (Diagnostic)** | Max jump is 3 points across calm frames. Diagnostic check; code was modified while iterating, so this is not independent validation. |
| **C8** | **Honesty & Wording Scan** | Zero occurrences of forbidden claims ("calibrated", "validated", "probability"). | **PASS (Diagnostic)** | 0 violations found across all code, documentation, and UI components. |
