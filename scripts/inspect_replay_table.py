import json

with open("backend/backfilled_replay.json", "r", encoding="utf-8") as f:
    data = json.load(f)

timeline = data["timeline"]
first_points = timeline[0]["points_state"]
loc_ids = list(first_points.keys())

# Select primary pilot locations to keep table compact & readable
pilot_subset = [
    "lonavala_town", "bhushi_dam", "kune_falls", "tiger_point",
    "khandala_expressway", "amrutanjan_point", "adoshi_tunnel",
    "monkey_hill", "patan_village"
]
active_locs = [l for l in pilot_subset if l in loc_ids]
# If any not in loc_ids, add whatever is in loc_ids
for l in loc_ids:
    if l not in active_locs:
        active_locs.append(l)

header = ["Step", "Date/Time (IST)", "1h Rain (mm)", "24h Accum (mm)", "Soil Sat (%)"] + [l.replace("_", " ") for l in active_locs]
print("| " + " | ".join(header) + " |")
print("| " + " | ".join(["---"] * len(header)) + " |")

for f in timeline:
    pts = f["points_state"]
    row = [
        str(f["step_index"]),
        f["timestamp_label"],
        f"{f['rainfall_1h_mm']:.1f}",
        f"{f['cumulative_24h_mm']:.1f}",
        f"{f['soil_saturation_pct']:.1f}%"
    ] + [str(pts.get(lid, {}).get("score", "N/A")) for lid in active_locs]
    print("| " + " | ".join(row) + " |")
