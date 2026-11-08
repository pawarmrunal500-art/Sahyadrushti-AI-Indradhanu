# 5-Minute Evaluation & Hackathon Demo Script: PralaySense AI

## Objective
Demonstrate the end-to-end workflow of PralaySense AI in 5 focused minutes:
1. Spatial differentiation under identical storm rain.
2. 14-day antecedent memory tracking $W(t)$.
3. Four-eyes emergency alert governance with CAP 1.2 XML output.
4. Multilingual citizen and community guidance.

---

### Step 1: Same Storm, Different Risk (Minute 0:00 - 1:15)
- **Goal:** Show that district-level rainfall creates vastly different localized hazards.
- **Action:** Open `http://localhost:5173/` on the main map.
- **Talking Point:**
  > *"When 150 mm of rain falls across Lonavala and Khandala, a district red alert treats them identically. But in PralaySense AI, Amrutanjan Bridge on the Expressway jumps to an elevated risk score because of its 38° engineered rock cut and high shear stress, whereas Lonavala Town Center remains at low risk (score 25) because of its flat terrain and gentle runoff gradient."*
- **Verification:** Click on **Amrutanjan Bridge / Bhor Ghat Expressway** to display its continuous Factor of Safety (FS ~0.62) and cut-slope vulnerability factors. Then click **Lonavala Civic Center** to observe the flat plain rating.

---

### Step 2: Antecedent Memory Variable $W(t)$ (Minute 1:15 - 2:30)
- **Goal:** Demonstrate that antecedent soil wetness dictates catastrophic failure timing.
- **Action:** Navigate to the **Storm Replay** tab (`/replay`).
- **Talking Point:**
  > *"Landslides rarely occur on the first day of rain. Here we replay 17 days of 12-hourly telemetry from the historic July 2026 Western Ghats event. Notice how the antecedent store $W(t)$ builds gradually across late June with a 60-hour drainage time constant. By July 6th, when the 180 mm squall hits, the profile soil moisture is already at 85%, driving perched pore pressures up and triggering critical escarpment instability."*
- **Verification:** Scrub the replay slider from Frame 0 (June 22, calm baseline) to Frame 28 (July 6, storm peak). Point out the continuous risk escalation without artificial step-function cliffs.

---

### Step 3: Four-Eyes Alert Governance & CAP 1.2 (Minute 2:30 - 3:45)
- **Goal:** Prove operational safety against accidental or rogue emergency broadcasts.
- **Action:** Navigate to **Authority Dashboard** (`/authority`). Log in as `operator1`.
- **Talking Point:**
  > *"Disaster alerts must be reliable and accountable. An operator drafts an evacuation alert for Bhushi Dam spillway. If the operator tries to self-approve and publish it, the system immediately rejects the request with HTTP 409 Conflict under the mandatory Four-Eyes Rule. Only a separate authorized approver can publish the alert, generating standardized CAP 1.2 XML for national emergency dispatch."*
- **Verification:** Show the drafted alert in the review queue, attempt self-approval to show the rejection, then log in as `approver1` to authorize the alert. View the generated CAP 1.2 XML output.

---

### Step 4: Multilingual Citizen Safety & Closing (Minute 3:45 - 5:00)
- **Goal:** Demonstrate accessibility for local residents, trekkers, and district disaster teams.
- **Action:** Switch the language toggle between English, **मराठी (Marathi)**, and **हिन्दी (Hindi)**.
- **Talking Point:**
  > *"Early warnings are useless if communities cannot understand them. Every location provides real-time protective action guidance in Marathi and Hindi, advising villagers on ground fissure inspections and warning commuters on the Mumbai-Pune corridor."*
- **Closing Statement:**
  > *"PralaySense AI transforms blunt district weather bulletins into actionable, physics-grounded early warnings for complex mountain terrain."*

