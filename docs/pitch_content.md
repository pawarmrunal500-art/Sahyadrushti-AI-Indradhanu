# Presentation & Pitch Deck Content: PralaySense AI
### AI-for-Climate-Change Hackathon / Disaster Management Track

---

## Slide 1: Title & Hook
- **Title:** PralaySense AI (सह्यादृष्टी | SAHYADRUSHTI AI)
- **Subtitle:** Physics-Informed Hyperlocal Landslide & Flash-Flood Early Warning System for the Western Ghats
- **The Problem:** When heavy rain hits the Sahyadri mountains, district-wide red alerts trigger widespread panic or warnings fatigue without pinpointing which highway cut, village escarpment, or waterfall gorge is dangerous.
- **The Solution:** A physics-grounded, multi-factor intelligence platform that models geotechnical stability and flash-flood runoff at 30-meter terrain resolution.

---

## Slide 2: The Core Thesis: Same Rain, Different Risk
- **The Myth:** Landslide risk is simply a function of daily rainfall amount.
- **The Reality:** 150 mm of rain at the flat Lonavala Town Center (6.5° slope) yields manageable stormwater runoff (Risk Index 25), while that exact same storm at Amrutanjan Bridge on the Mumbai-Pune Expressway (36.5° slope, 180m vertical relief within 300m) destabilizes weathered basalt overburden, reducing the geotechnical Factor of Safety below critical equilibrium ($FS < 1.0$).
- **Evidence from Copernicus GLO-30 DEM:**
  - Highway rock cuts exhibit local slope angles exceeding $38^\circ\text{–}51^\circ$.
  - Plateau viewpoints sit directly above 120m sheer escarpment cliffs.

---

## Slide 3: Antecedent Memory Variable $W(t)$
- **Why Timing Matters:** Severe landslides in the Western Ghats (e.g., Malin 2014, Irshalwadi 2023) almost never happen on Day 1 of the monsoon; they occur when weeks of antecedent rain saturate deep saprolite fractures.
- **Physics-Informed Formulation:**
  - Drained Water Store $W(t)$ with a 60-hour drainage recession constant ($\tau = 60\text{h}$) models joint water retention.
  - Multi-depth soil moisture integration ($0\text{–}1\text{cm}, 3\text{–}9\text{cm}, 9\text{–}27\text{cm}$) continuously calculates perched pore-water pressures.
  - Replay of the July 2026 storm demonstrates continuous risk escalation over a 17-day window without artificial score jumps.

---

## Slide 4: Operational Governance & Four-Eyes Protection
- **Disaster Risk Governance:** Emergency broadcasts cannot rely on unverified automated predictions or single-operator panic.
- **Four-Eyes Rule Enforced:**
  - An operator drafts an evacuation alert.
  - The backend strictly enforces authorization separation: if the drafting operator attempts approval, the system rejects it with `HTTP 409 Conflict`.
  - Authorized approver validates and signs the alert.
  - Automatically emits standard **Common Alerting Protocol (CAP 1.2)** XML for NDRF / SDRF / state emergency communication networks.

---

## Slide 5: Scientific Integrity & Honest Boundaries
- **Clear Honesty Policy:**
  - Evaluated as a **Risk Index (0–100)**, not empirical probability.
  - Explicit disclosure of uncalibrated parameters (basalt cohesion, friction angle, drainage recession constant).
  - Acknowledgment of reanalysis grid smoothing (9–11 km cells) and lower-bound rainfall estimates.
  - Documented spatial discrepancies (Patan Village flat shelf vs escarpment) awaiting field ground-truthing.

---

## Slide 6: Roadmap & Production Scale-Up
- **Phase 1 (Achieved):** 12 pilot locations across Lonavala, Khandala, and Bhor Ghat; continuous geotechnical FS; Four-Eyes CAP 1.2 alerts; multilingual (en/mr/hi) support.
- **Phase 2 (Immediate Next Steps):** Calibration of precipitation bias multipliers against IMD AWS station data; high-resolution UAV/LiDAR slope mapping for highway cuts.
- **Phase 3 (Regional Expansion):** Expansion to high-risk Konkan and Western Ghats corridors (Mahabaleshwar, Tamhini Ghat, Varandha Ghat, Malshej Ghat).

