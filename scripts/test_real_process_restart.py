"""
scripts/test_real_process_restart.py
Starts uvicorn as a separate real OS subprocess, POSTs a unique incident,
kills the uvicorn process, starts a new uvicorn process, and GETs the incident
to prove persistence across true OS process restarts.
"""
import subprocess
import time
import sys
import os
import urllib.request
import json
import uuid

PORT = 8009
BASE_URL = f"http://127.0.0.1:{PORT}"

def wait_for_server(url, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(f"{url}/api/health", timeout=2) as res:
                if res.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def run_test():
    print("=" * 65)
    print("SAHYADRUSHTI AI - Real OS Process Restart Persistence Verification")
    print("=" * 65)

    test_id = f"PROC-TEST-{uuid.uuid4().hex[:6].upper()}"
    test_title = f"Real OS Process Restart Hazard Report ({test_id})"

    # 1. Start Process 1
    print(f"\n[Step 1] Starting uvicorn on port {PORT} (PID 1)...")
    env = os.environ.copy()
    env["SCHEDULER_ENABLED"] = "false"
    p1 = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    try:
        assert wait_for_server(BASE_URL, timeout=15), "Server 1 failed to start!"
        print(f"  Server 1 running (PID: {p1.pid}). Submitting incident...")

        payload = json.dumps({
            "hazard_type": "rockfall",
            "location_name": "Adoshi Tunnel Approach",
            "lat": 18.756,
            "lon": 73.368,
            "description": f"Verified in test: {test_title}",
            "observed_time": "2026-10-24T18:00:00Z",
            "reporter_name": "Process Tester"
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/api/incidents",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            assert res.status == 201
            resp_data = json.loads(res.read().decode("utf-8"))
            incident_id = resp_data["incident_id"]
            print(f"  Incident posted successfully: ID={incident_id}, Status={resp_data['verification_status']}")
    finally:
        print("\n[Step 2] Terminating Server 1 process...")
        p1.terminate()
        try:
            p1.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p1.kill()
        print(f"  Server 1 (PID: {p1.pid}) killed.")

    time.sleep(3)

    # 2. Start Process 2 (Cold OS Reboot)
    print(f"\n[Step 3] Starting uvicorn on port {PORT} (PID 2 - Fresh Process)...")
    p2 = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        env=env
    )
    try:
        started = wait_for_server(BASE_URL, timeout=20)
        assert started, "Server 2 failed to start!"
        print(f"  Server 2 running (PID: {p2.pid}). Verifying incident persistence...")

        with urllib.request.urlopen(f"{BASE_URL}/api/incidents", timeout=5) as res:
            assert res.status == 200
            incidents = json.loads(res.read().decode("utf-8"))
            match = next((i for i in incidents if i["id"] == incident_id), None)
            assert match is not None, f"Incident {incident_id} not found after real process restart!"
            print(f"  [SUCCESS] Incident {incident_id} survived real process reboot!")
            print(f"            Title: {match['title']}")
            print(f"            Description: {match['description']}")
    finally:
        print("\n[Step 4] Terminating Server 2 process...")
        p2.terminate()
        try:
            p2.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p2.kill()
        print(f"  Server 2 (PID: {p2.pid}) killed.")

    print("\n" + "=" * 65)
    print("REAL OS PROCESS RESTART TEST: 100% PASSED")
    print("=" * 65)

if __name__ == "__main__":
    run_test()
