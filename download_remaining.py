import os
import time
import json
import urllib.request
from PIL import Image, ImageOps

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'public')
IMG_DIR = os.path.join(PUBLIC_DIR, 'images')

FILES_TO_FETCH = {
    'locations/lions_point.jpg': 'File:Lions Point - India.jpg',
    'locations/amrutanjan_bridge.jpg': 'File:Lonavala Near Amrutanjan Bridge.jpg',
    'locations/lonavala_valleys.jpg': 'File:KHANDALA AND LONAVALA VALLEYS 1.jpg',
    'features/feat_landslide.jpg': 'File:Gasquet Landslide CALTRANS.jpg',
    'features/feat_flashflood.jpg': 'File:Sahyadri Waterfall.jpg',
    'features/feat_corridor.jpg': 'File:Mumbai-Pune Expressway 1.JPG',
}

def get_thumburl(title):
    url = f'https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&iiurlwidth=1200&format=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'SahyadrushtiPilotApp/1.0 (edu: dev@sahyadrushti.org)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        d = json.loads(resp.read().decode())
        p = list(d['query']['pages'].values())[0]
        ii = p.get('imageinfo', [{}])[0]
        return ii.get('thumburl') or ii.get('url')

for rel_path, wiki_title in FILES_TO_FETCH.items():
    dest = os.path.join(IMG_DIR, rel_path)
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print(f"Skipping {rel_path}, already exists.")
        continue
    
    print(f"Resolving {wiki_title}...")
    try:
        thumb_url = get_thumburl(wiki_title)
        if not thumb_url:
            print(f"Could not get thumb for {wiki_title}")
            continue
        print(f"Downloading {rel_path} from {thumb_url}...")
        time.sleep(1.5)
        
        req = urllib.request.Request(thumb_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        temp_file = dest + '.tmp'
        with urllib.request.urlopen(req, timeout=20) as r:
            with open(temp_file, 'wb') as f:
                f.write(r.read())
        
        with Image.open(temp_file) as im:
            im = ImageOps.exif_transpose(im)
            im = im.convert('RGB')
            im.thumbnail((1200, 800), Image.Resampling.LANCZOS)
            im.save(dest, 'JPEG', quality=85, optimize=True)
        if os.path.exists(temp_file):
            os.remove(temp_file)
        print(f"Successfully saved {rel_path} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"Error processing {rel_path}: {e}")
    time.sleep(2.0)

print("Remaining downloads complete!")

