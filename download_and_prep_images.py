import os
import time
import urllib.request
from PIL import Image, ImageOps, ImageDraw, ImageFont

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'public')
IMG_DIR = os.path.join(PUBLIC_DIR, 'images')
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(os.path.join(IMG_DIR, 'locations'), exist_ok=True)
os.makedirs(os.path.join(IMG_DIR, 'features'), exist_ok=True)

IMAGE_URLS = {
    # Locations
    'locations/bhushi_dam.jpg': 'https://upload.wikimedia.org/wikipedia/commons/7/72/Bhushi_Dam_-_Lonavala.jpg',
    'locations/tiger_point.jpg': 'https://upload.wikimedia.org/wikipedia/commons/9/9b/Tiger_Point%2C_Lonavala.jpg',
    'locations/lions_point.jpg': 'https://upload.wikimedia.org/wikipedia/commons/5/52/Lions_Point_-_India.jpg',
    'locations/kune_falls.jpg': 'https://upload.wikimedia.org/wikipedia/commons/f/fb/A_waterfall_on_the_way_to_Lonavala%2C_Maharashtra.jpg',
    'locations/rajmachi.jpg': 'https://upload.wikimedia.org/wikipedia/commons/2/26/Rajmachi_Fort.JPG',
    'locations/amrutanjan_bridge.jpg': 'https://upload.wikimedia.org/wikipedia/commons/d/d5/Lonavala_Near_Amrutanjan_Bridge.jpg',
    'locations/lonavala_valleys.jpg': 'https://upload.wikimedia.org/wikipedia/commons/d/dd/KHANDALA_AND_LONAVALA_VALLEYS_1.jpg',
    'locations/adoshi_tunnel.jpg': 'https://upload.wikimedia.org/wikipedia/commons/b/b5/Mumbai-Pune_Expressway_1.JPG',
    'locations/tiger_valley.jpg': 'https://upload.wikimedia.org/wikipedia/commons/6/60/Tiger_Valley_Bridge_view_3.jpg',
    
    # Feature headers
    'features/feat_flashflood.jpg': 'https://upload.wikimedia.org/wikipedia/commons/7/7f/Sahyadri_Waterfall.jpg',
    'features/feat_weather.jpg': 'https://upload.wikimedia.org/wikipedia/commons/c/c0/Monsoon_clouds_in_Western_ghats.jpg',
    'features/feat_landslide.jpg': 'https://upload.wikimedia.org/wikipedia/commons/9/9b/Gasquet_Landslide_CALTRANS.jpg',
    'features/feat_rescue.jpg': 'https://upload.wikimedia.org/wikipedia/commons/6/66/Indian_NDRF_team_carry_out_rescue_operation_in_Gaziantep.jpg',
    'features/feat_corridor.jpg': 'https://upload.wikimedia.org/wikipedia/commons/b/b5/Mumbai-Pune_Expressway_1.JPG',
}

def download_and_optimize(rel_path, url):
    dest_path = os.path.join(IMG_DIR, rel_path)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        print(f"Already exists: {rel_path} ({os.path.getsize(dest_path)} bytes)")
        return True

    print(f"Downloading {rel_path} from {url} ...")
    temp_path = dest_path + '.tmp'
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SahyadrushtiEdu/1.0'}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(temp_path, 'wb') as f:
                f.write(resp.read())
        
        # Optimize with PIL
        with Image.open(temp_path) as img:
            img = ImageOps.exif_transpose(img)
            img = img.convert('RGB')
            # Resize if too large
            max_w, max_h = 1200, 800
            img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            img.save(dest_path, 'JPEG', quality=85, optimize=True)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Saved & optimized {rel_path} ({os.path.getsize(dest_path)} bytes)")
        return True
    except Exception as e:
        print(f"Failed to download {rel_path}: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

# Run downloads
for rel_path, url in IMAGE_URLS.items():
    download_and_optimize(rel_path, url)
    time.sleep(1.0)

# Also generate customized banner and remaining specific visuals from sahyadri_landscape.jpg
sahyadri_src = os.path.join(PUBLIC_DIR, 'sahyadri_landscape.jpg')
if os.path.exists(sahyadri_src):
    with Image.open(sahyadri_src) as base_img:
        base_img = base_img.convert('RGB')
        
        # 1. Overview Banner: 1200x380 aspect ratio crop for the dashboard overview
        w, h = base_img.size
        target_h = int(w * 360 / 1200)
        top = (h - target_h) // 2
        banner = base_img.crop((0, max(0, top), w, min(h, top + target_h)))
        banner_path = os.path.join(IMG_DIR, 'banner_lonavala_overview.jpg')
        banner.save(banner_path, 'JPEG', quality=88, optimize=True)
        print(f"Created banner_lonavala_overview.jpg ({banner.size})")

        # 2. Monkey Hill / Railway cutting: fallback if not downloaded
        mh_path = os.path.join(IMG_DIR, 'locations', 'monkey_hill.jpg')
        if not os.path.exists(mh_path):
            mh_crop = base_img.crop((0, int(h * 0.2), int(w * 0.7), int(h * 0.85)))
            mh_crop.save(mh_path, 'JPEG', quality=85)
            print("Created monkey_hill.jpg")

        # 3. Thakurwadi: fallback if not downloaded
        tw_path = os.path.join(IMG_DIR, 'locations', 'thakurwadi.jpg')
        if not os.path.exists(tw_path):
            tw_crop = base_img.crop((int(w * 0.3), int(h * 0.15), w, int(h * 0.8)))
            tw_crop.save(tw_path, 'JPEG', quality=85)
            print("Created thakurwadi.jpg")

        # 4. Patan Village
        pv_path = os.path.join(IMG_DIR, 'locations', 'patan_village.jpg')
        if not os.path.exists(pv_path):
            pv_crop = base_img.crop((int(w * 0.2), int(h * 0.3), int(w * 0.85), h))
            pv_crop.save(pv_path, 'JPEG', quality=85)
            print("Created patan_village.jpg")

print("All base images prepared!")

