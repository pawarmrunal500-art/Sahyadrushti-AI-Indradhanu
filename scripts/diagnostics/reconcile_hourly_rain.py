"""
scripts/diagnostics/reconcile_hourly_rain.py
Step 3: Reproducibility & Hourly Rainfall Reconciliation
Prints the raw hourly rainfall array per location directly from extended_archive_cache.json
for frames 2026-06-24 12:00, 2026-06-26 12:00, and 2026-06-30 12:00 IST.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.data_layer import LOCATIONS_DATA

CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts", "extended_archive_cache.json")

def print_hourly_reconciliation():
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    times = data[0]["hourly"]["time"]
    target_frames = ["2026-06-24T12:00", "2026-06-26T12:00", "2026-06-30T12:00"]

    print("=" * 110)
    print("STEP 3: HOURLY RAINFALL ARRAYS PER LOCATION (DIRECTLY FROM RAW ARCHIVE CACHE)")
    print("=" * 110)

    for target_t in target_frames:
        idx = times.index(target_t)
        print(f"\n>>> FRAME: {target_t} (Archive index {idx})")
        print("-" * 110)
        print(f"{'Location ID':<22} {'Grid Cell Group':<26} {'24h Sum (mm)':<14} {'Raw Hourly Precipitation Array [T-23 to T] (mm)':<50}")
        print("-" * 110)
        
        for i, loc in enumerate(LOCATIONS_DATA):
            precip = data[i]["hourly"]["precipitation"]
            w24 = precip[idx-23:idx+1]
            total = sum(p for p in w24 if p is not None)
            lid = loc["id"]
            
            # Identify grid cell group
            if lid in ("adoshi_tunnel", "thakurwadi"):
                cell = "Cell 1 (Khopoli/North Ghat)"
            elif lid in ("bhushi_dam", "kune_falls"):
                cell = "Cell 2 (Lonavala W / Kune)"
            elif lid in ("khandala_expressway", "monkey_hill"):
                cell = "Cell 3 (Bhor Ghat Cutting)"
            elif lid in ("tiger_point", "lions_point", "patan_village"):
                cell = "Cell 4 (South Escarpment)"
            else:
                cell = "Cell 5 (Lonavala Civic/Valvan)"

            arr = [round(p, 1) if p is not None else 0.0 for p in w24]
            print(f"{lid:<22} {cell:<26} {total:6.1f} mm       {arr}")

if __name__ == "__main__":
    print_hourly_reconciliation()
