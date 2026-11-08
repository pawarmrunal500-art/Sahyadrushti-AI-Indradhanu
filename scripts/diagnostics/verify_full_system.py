"""
Full System & Dashboard Verification Script
Tests all backend API endpoints, security mechanisms, data flows, and frontend assets.
"""
import sys
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:5173"

def make_req(path, method="GET", data=None, headers=None):
    url = f"{BASE_URL}{path}"
    h = headers or {}
    body = None
    if data is not None:
        if isinstance(data, dict):
            body = json.dumps(data).encode("utf-8")
            h["Content-Type"] = "application/json"
        elif isinstance(data, (bytes, bytearray)):
            body = data
        elif isinstance(data, str):
            body = data.encode("utf-8")
            
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace"), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace"), e.headers
    except Exception as e:
        return 0, str(e), {}

def test_frontend():
    req = urllib.request.Request(FRONTEND_URL)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            content = resp.read().decode("utf-8", errors="replace")
            has_root = '<div id="root">' in content or '<div id="app">' in content
            has_script = '<script type="module"' in content
            return status == 200, f"Status: {status}, has_root: {has_root}, has_script: {has_script}"
    except Exception as e:
        return False, str(e)

def run_tests():
    results = []
    
    # 1. Health
    s, b, _ = make_req("/api/health")
    j = json.loads(b) if s == 200 else {}
    results.append({
        "component": "Backend Core",
        "feature": "Health Check & Database Link",
        "endpoint": "GET /api/health",
        "passed": s == 200 and j.get("status") == "HEALTHY",
        "details": f"model: {j.get('model_version')}, db: {j.get('db_status')}"
    })

    # 2. Locations
    s, b, _ = make_req("/api/locations")
    j = json.loads(b) if s == 200 else []
    results.append({
        "component": "Location Subsystem",
        "feature": "12 Pilot Monitoring Stations",
        "endpoint": "GET /api/locations",
        "passed": s == 200 and len(j) == 12,
        "details": f"Retrieved {len(j)} locations; sample: {j[0].get('name') if j else ''}"
    })

    # 3. Weather Current
    s, b, _ = make_req("/api/weather/current")
    j = json.loads(b) if s == 200 else []
    results.append({
        "component": "Weather Subsystem",
        "feature": "Current Telemetry / Infiltration Tracking",
        "endpoint": "GET /api/weather/current",
        "passed": s == 200 and len(j) >= 12,
        "details": f"Telemetry records: {len(j)}"
    })

    # 4. Compare Endpoint (Spatial Differentiation)
    s, b, _ = make_req("/api/compare?rain_24h_mm=100")
    j = json.loads(b) if s == 200 else {}
    ranking = j.get("ranking", [])
    scores = [item["risk_score"] for item in ranking] if isinstance(ranking, list) else []
    spread_raw = j.get("spread", 0)
    spread = spread_raw.get("score_differential", 0) if isinstance(spread_raw, dict) else spread_raw
    results.append({
        "component": "ML / Geotechnical Engine",
        "feature": "Spatial Risk Comparison (R1 - Same Rain, Different Risk)",
        "endpoint": "GET /api/compare?rain_24h_mm=100",
        "passed": s == 200 and spread >= 30,
        "details": f"{len(ranking)} sites scored, spread: {spread} (min={min(scores) if scores else 0}, max={max(scores) if scores else 0})"
    })

    # 5. Risk Spot Evaluation
    s, b, _ = make_req("/api/risk?lat=18.75&lon=73.38")
    j = json.loads(b) if s == 200 else {}
    risk_eval = j.get("risk_evaluation", {})
    factors = risk_eval.get("contributing_factors", [])
    results.append({
        "component": "ML / Geotechnical Engine",
        "feature": "Hyperlocal Spot Risk & Explanation (R4)",
        "endpoint": "GET /api/risk?lat=18.75&lon=73.38",
        "passed": s == 200 and "risk_score" in risk_eval and len(factors) >= 3,
        "details": f"Nearest: {j.get('nearest_pilot_location', {}).get('name')}, Score: {risk_eval.get('risk_score')}, Band: {risk_eval.get('risk_band')}, Factors: {len(factors)}"
    })

    # 6. Risk Forecast
    s, b, _ = make_req("/api/risk/forecast?location_id=khandala_expressway")
    j = json.loads(b) if s == 200 else {}
    fc_list = j.get("projections", [])
    results.append({
        "component": "ML / Geotechnical Engine",
        "feature": "Hyperlocal Threat Forecast (R3 - 72h Projections)",
        "endpoint": "GET /api/risk/forecast?location_id=khandala_expressway",
        "passed": s == 200 and len(fc_list) > 0,
        "details": f"Forecast points: {len(fc_list)}, max future risk: {max([f['risk_score'] for f in fc_list]) if fc_list else 'N/A'}"
    })

    # 7. Vulnerable Zones
    s, b, _ = make_req("/api/vulnerable-zones")
    j = json.loads(b) if s == 200 else {}
    features = j.get("features", [])
    top_feature = features[0].get("properties", {}) if features else {}
    results.append({
        "component": "Hazard & Corridor Analysis",
        "feature": "Vulnerable Zones Ranking (R5 - GeoJSON)",
        "endpoint": "GET /api/vulnerable-zones",
        "passed": s == 200 and len(features) >= 12,
        "details": f"Ranked {len(features)} zones; Top hazard: {top_feature.get('name')} (Score: {top_feature.get('risk_score')})"
    })

    # 8. Replay System (Continuous 17-Day History)
    s, b, _ = make_req("/api/replay")
    j = json.loads(b) if s == 200 else {}
    timeline = j.get("timeline", [])
    results.append({
        "component": "Simulation & Audit Replay",
        "feature": "17-Day July Storm Replay (R3/C3 Timeline)",
        "endpoint": "GET /api/replay",
        "passed": s == 200 and len(timeline) >= 30,
        "details": f"Frames available: {len(timeline)} (Model: {j.get('model_version')}, Calibrated: {j.get('calibration_status')})"
    })

    # 9. Alerts Public & CAP 1.2
    s1, b1, _ = make_req("/api/alerts")
    j1 = json.loads(b1) if s1 == 200 else []
    has_cap = any(a.get("cap_format") and "urn:oasis:names:tc:emergency:cap:1.2" in a.get("cap_format") for a in j1)
    results.append({
        "component": "Public Warning Feeds",
        "feature": "CAP 1.2 Common Alerting Protocol (R6)",
        "endpoint": "GET /api/alerts",
        "passed": s1 == 200 and len(j1) > 0 and has_cap,
        "details": f"Alerts count: {len(j1)}, Verified CAP 1.2 OASIS XML payload present: {has_cap}"
    })

    # 10. Incident Reporting (Citizen Submission)
    test_incident = {
        "hazard_type": "landslide",
        "location_name": "Khandala Ghat Exit (KM 42)",
        "lat": 18.761,
        "lon": 73.375,
        "description": "Loose basalt fragments on shoulder lane following rain shower.",
        "observed_time": "2026-11-08T12:00:00Z",
        "reporter_name": "Citizen Observer"
    }
    s_post, b_post, _ = make_req("/api/incidents", method="POST", data=test_incident)
    s_get, b_get, _ = make_req("/api/incidents")
    incidents = json.loads(b_get) if s_get == 200 else []
    results.append({
        "component": "Citizen Reporting Hub",
        "feature": "Hazard Reporting & Feed",
        "endpoint": "POST & GET /api/incidents",
        "passed": s_post in (200, 201) and s_get == 200 and len(incidents) > 0,
        "details": f"Submit HTTP {s_post}, Total incidents in feed: {len(incidents)}"
    })

    # 11. Security & Four-Eyes Governance
    # A. Operator login and draft creation
    login_op = {"username": "demo_operator", "password": "OperatorPass123!"}
    s_auth, b_auth, _ = make_req("/api/auth/login", method="POST", data=login_op)
    token_op = json.loads(b_auth).get("access_token") if s_auth == 200 else None
    
    draft_data = {
        "title": "EOC Precautionary Caution - Khandala Slopes",
        "title_mr": "खंडाळा उतारांवर दक्षता इशारा",
        "message": "Continuous rainfall expected; avoid parking near unstable rock faces.",
        "message_mr": "सलग पावसामुळे दरड कोसळण्याची शक्यता; धोकादायक उतारांजवळ थांबू नका.",
        "severity": "MODERATE",
        "geographic_coverage": "Khandala Ghat Escarpment",
        "target_locations": ["khandala_expressway", "monkey_hill"]
    }
    s_draft, b_draft, _ = make_req(
        "/api/authority/alerts/draft",
        method="POST",
        data=draft_data,
        headers={"Authorization": f"Bearer {token_op}"}
    )
    draft_resp = json.loads(b_draft) if s_draft in (200, 201) else {}
    draft_id = draft_resp.get("alert_id")

    # B. Test Operator approval attempt (MUST fail with 403 Forbidden - RBAC enforcement)
    s_op_appr, _, _ = make_req(
        f"/api/authority/alerts/{draft_id}/approve",
        method="POST",
        headers={"Authorization": f"Bearer {token_op}"}
    )
    rbac_enforced = (s_op_appr == 403)

    # C. Approver login
    login_sup = {"username": "demo_approver", "password": "ApproverPass123!"}
    s_sup, b_sup, _ = make_req("/api/auth/login", method="POST", data=login_sup)
    token_sup = json.loads(b_sup).get("access_token") if s_sup == 200 else None

    # D. Test Approver drafting an alert and self-approving (MUST fail with 409 Conflict - Four-Eyes enforcement)
    s_draft2, b_draft2, _ = make_req(
        "/api/authority/alerts/draft",
        method="POST",
        data=draft_data,
        headers={"Authorization": f"Bearer {token_sup}"}
    )
    draft_id2 = json.loads(b_draft2).get("alert_id") if s_draft2 in (200, 201) else None
    s_self_appr, _, _ = make_req(
        f"/api/authority/alerts/{draft_id2}/approve",
        method="POST",
        headers={"Authorization": f"Bearer {token_sup}"}
    )
    four_eyes_enforced = (s_self_appr == 409)

    # E. Approver approves operator's draft (Separate users -> 200 OK)
    s_sup_appr, b_sup_appr, _ = make_req(
        f"/api/authority/alerts/{draft_id}/approve",
        method="POST",
        headers={"Authorization": f"Bearer {token_sup}"}
    )

    results.append({
        "component": "EOC Authority Governance",
        "feature": "RBAC (403) & Four-Eyes Principle (409 Conflict) (C5)",
        "endpoint": "POST /api/authority/alerts/{id}/approve",
        "passed": rbac_enforced and four_eyes_enforced and s_sup_appr in (200, 204),
        "details": f"Operator approval: {s_op_appr} (403 RBAC), Self-approval: {s_self_appr} (409 Conflict), Dual-control approval: {s_sup_appr} (200 OK)"
    })

    # 12. Frontend Web Dashboard
    fe_ok, fe_details = test_frontend()
    results.append({
        "component": "Frontend SPA UI",
        "feature": "Vite React Dashboard (localhost:5173)",
        "endpoint": "GET http://localhost:5173",
        "passed": fe_ok,
        "details": fe_details
    })

    return results

if __name__ == "__main__":
    test_results = run_tests()
    print("=" * 80)
    print("SAHYADRUSHTI AI - SYSTEM & DASHBOARD FEATURE VERIFICATION RUN")
    print("=" * 80)
    all_pass = True
    for r in test_results:
        status_str = "[PASS]" if r["passed"] else "[FAIL]"
        if not r["passed"]:
            all_pass = False
        print(f"{status_str} {r['component']} | {r['feature']}")
        print(f"       Endpoint: {r['endpoint']}")
        print(f"       Details:  {r['details']}")
        print("-" * 80)
    print("OVERALL RESULT:", "ALL SYSTEMS OPERATIONAL" if all_pass else "FAILURES DETECTED")
    print("=" * 80)
    sys.exit(0 if all_pass else 1)
