import requests
import json
from datetime import datetime
import pytz

# ---------------------------------------------------------
# 🛡️ BACKUP CHANNELS (Jab Internet Scan Fail Ho)
# ---------------------------------------------------------
BACKUP_MATCHES = [
    {
        "id": "bak-hotstar-1",
        "title": "Star Sports 1 Hindi (Backup)",
        "status": "LIVE",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Star_Sports_1_Hindi_logo.png",
        "url": "https://prod-sports-eng-Linear-jit-wsp-partner-stats.hotstar.com/hls/ss1hindi/index.m3u8", # Aksar dead hota hai par try kar sakte hain
        "platform": "Star Sports",
        "is_drm": False
    },
    {
        "id": "bak-willow-1",
        "title": "Willow Cricket HD",
        "status": "LIVE",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Willow_TV_logo.svg/1200px-Willow_TV_logo.svg.png",
        "url": "http://tv.digitalview.live:8080/live/willow/willow/1000.m3u8",
        "platform": "Willow TV",
        "is_drm": False
    },
    {
        "id": "bak-sky-1",
        "title": "Sky Sports Cricket",
        "status": "LIVE",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Sky_Sports_Cricket_logo.svg/1200px-Sky_Sports_Cricket_logo.svg.png",
        "url": "http://tv.digitalview.live:8080/live/skycricket/skycricket/1000.m3u8",
        "platform": "Sky Sports",
        "is_drm": False
    },
    {
        "id": "bak-astro-1",
        "title": "Astro Cricket",
        "status": "LIVE",
        "logo": "https://upload.wikimedia.org/wikipedia/en/7/7a/Astro_Cricket_Logo.png",
        "url": "http://tv.digitalview.live:8080/live/astrocrick/astrocrick/1000.m3u8",
        "platform": "Astro",
        "is_drm": False
    }
]

# ---------------------------------------------------------
# 🔥 LIVE SOURCES
# ---------------------------------------------------------
SOURCES = [
    {"name": "Tata Play Binge", "url": "https://raw.githubusercontent.com/ForceGT/Tata-Sky-IPTV/master/code_samples/all.m3u"},
    {"name": "Mikes1278 Sports", "url": "https://raw.githubusercontent.com/Mikes1278/IPTV/main/playlist.m3u"}
]

KEYWORDS = [
    "star sports", "hotstar", "prime video", "sony liv", 
    "astro cricket", "willow", "sky sports", "fox cricket"
]

def parse_m3u(text, source_name):
    matches = []
    lines = text.splitlines()
    current_name = ""
    current_logo = ""

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            name = line.split(",")[-1].strip()
            if 'tvg-logo="' in line:
                current_logo = line.split('tvg-logo="')[1].split('"')[0]
            else:
                current_logo = "https://ui-avatars.com/api/?name=TV"
            current_name = name
            
        elif line.startswith("http") and current_name:
            if any(k in current_name.lower() for k in KEYWORDS):
                matches.append({
                    "id": f"vip-{len(matches)}",
                    "title": current_name,
                    "status": "LIVE",
                    "logo": current_logo,
                    "url": line,
                    "platform": "Hotstar/VIP",
                    "is_drm": "hmac" in line or "key" in line
                })
            current_name = ""
            
    return matches

def fetch_group_b():
    print("🚀 Fetching Hotstar & VIP Content...")
    all_matches = []

    # 1. Internet Scan
    for source in SOURCES:
        try:
            print(f"📡 Scanning: {source['name']}...")
            res = requests.get(source['url'], timeout=15)
            if res.status_code == 200:
                matches = parse_m3u(res.text, source['name'])
                print(f"   Found {len(matches)} streams")
                all_matches.extend(matches)
        except Exception as e:
            print(f"⚠️ Failed {source['name']}: {e}")

    # 2. Add Backup if list is small
    if len(all_matches) < 3:
        print("⚠️ Scan weak. Adding Backup Channels.")
        all_matches.extend(BACKUP_MATCHES)

    return all_matches

def main():
    matches = fetch_group_b()
    
    output = {
        "updated_at": datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M:%S %p"),
        "total_matches": len(matches),
        "matches": matches
    }

    with open('live_matches_B.json', 'w') as f:
        json.dump(output, f, indent=4)
    
    print(f"✅ Group B Update Complete! {len(matches)} matches saved.")

if __name__ == "__main__":
    main()
