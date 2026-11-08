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

