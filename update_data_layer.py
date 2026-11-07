with open('backend/data_layer.py', 'r', encoding='utf-8') as f:
    content = f.read()

mapping = {
    '"id": "bhushi_dam",': '"id": "bhushi_dam",\n        "image_url": "/images/locations/bhushi_dam.jpg",',
    '"id": "kune_falls",': '"id": "kune_falls",\n        "image_url": "/images/locations/kune_falls.jpg",',
    '"id": "tiger_point",': '"id": "tiger_point",\n        "image_url": "/images/locations/tiger_point.jpg",',
    '"id": "lions_point",': '"id": "lions_point",\n        "image_url": "/images/locations/lions_point.jpg",',
    '"id": "rajmachi_route",': '"id": "rajmachi_route",\n        "image_url": "/images/locations/rajmachi.jpg",',
    '"id": "khandala_expressway",': '"id": "khandala_expressway",\n        "image_url": "/images/locations/amrutanjan_bridge.jpg",',
    '"id": "adoshi_tunnel",': '"id": "adoshi_tunnel",\n        "image_url": "/images/locations/adoshi_tunnel.jpg",',
    '"id": "monkey_hill",': '"id": "monkey_hill",\n        "image_url": "/images/locations/monkey_hill.jpg",',
    '"id": "thakurwadi",': '"id": "thakurwadi",\n        "image_url": "/images/locations/thakurwadi.jpg",',
    '"id": "patan_village",': '"id": "patan_village",\n        "image_url": "/images/locations/patan_village.jpg",',
    '"id": "valvan_dam",': '"id": "valvan_dam",\n        "image_url": "/images/locations/lonavala_valleys.jpg",',
    '"id": "lonavala_town",': '"id": "lonavala_town",\n        "image_url": "/images/locations/lonavala_valleys.jpg",',
}

inc_mapping = {
    '"id": "INC-2024-0630-BHUSHI",': '"id": "INC-2024-0630-BHUSHI",\n        "image_url": "/images/locations/bhushi_dam.jpg",',
    '"id": "INC-2025-0718-EXPRESSWAY",': '"id": "INC-2025-0718-EXPRESSWAY",\n        "image_url": "/images/locations/amrutanjan_bridge.jpg",',
    '"id": "INC-2026-0712-PATAN",': '"id": "INC-2026-0712-PATAN",\n        "image_url": "/images/locations/patan_village.jpg",',
    '"id": "INC-2026-0724-THAKURWADI",': '"id": "INC-2026-0724-THAKURWADI",\n        "image_url": "/images/locations/monkey_hill.jpg",',
    '"id": "INC-2026-0210-ADOSHI",': '"id": "INC-2026-0210-ADOSHI",\n        "image_url": "/images/locations/adoshi_tunnel.jpg",',
}

for k, v in {**mapping, **inc_mapping}.items():
    if k in content and '"image_url"' not in content[content.find(k):content.find(k)+120]:
        content = content.replace(k, v, 1)

with open('backend/data_layer.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated backend/data_layer.py!')

