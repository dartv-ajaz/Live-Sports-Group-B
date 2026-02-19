import requests
import json
from datetime import datetime
import pytz

# ---------------------------------------------------------
# 🔥 HOTSTAR & PRIME SOURCE
# ---------------------------------------------------------
# Hum "Tata Sky" aur "JioTV" ke links use karenge jo Hotstar content dikhate hain
SOURCES = [
    {"name": "Tata Play Binge", "url": "https://raw.githubusercontent.com/ForceGT/Tata-Sky-IPTV/master/code_samples/all.m3u"},
    {"name": "JioTV Specials", "url": "https://raw.githubusercontent.com/ForceGT/JioTV/master/user_data/playlist.m3u"}
]

KEYWORDS = [
    "star sports", "hotstar", "prime video", "sony liv", 
    "astro cricket", "willow", "sky sports"
]

def parse_m3u(text, source_name):
    matches = []
    lines = text.splitlines()
    current_name = ""
    current_logo = ""

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            # Name extraction
            name = line.split(",")[-1].strip()
            # Logo extraction
            if 'tvg-logo="' in line:
                current_logo = line.split('tvg-logo="')[1].split('"')[0]
            else:
                current_logo = "https://ui-avatars.com/api/?name=Hotstar"
            current_name = name
            
        elif line.startswith("http") and current_name:
            # CHECK: Kya ye hamare kaam ka channel hai?
            if any(k in current_name.lower() for k in KEYWORDS):
                matches.append({
                    "id": f"vip-{len(matches)}",
                    "title": current_name,
                    "status": "LIVE",
                    "logo": current_logo,
                    "url": line,
                    "platform": "Hotstar/VIP",
                    "is_drm": "hmac" in line or "key" in line # Basic DRM check
                })
            current_name = ""
            
    return matches

def fetch_group_b():
    print("🚀 Fetching Hotstar & VIP Content...")
    all_matches = []

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

    return all_matches

def main():
    matches = fetch_group_b()
    
    # Empty Check
    if not matches:
        print("⚠️ Warning: Koi VIP match nahi mila.")
        # Hum file save karenge bhale hi khali ho, taake App crash na ho
    
    output = {
        "updated_at": datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M:%S %p"),
        "total_matches": len(matches),
        "matches": matches  # App.tsx is key ko dhoondta hai
    }

    # NOTE: File ka naam 'live_matches_B.json' hai
    with open('live_matches_B.json', 'w') as f:
        json.dump(output, f, indent=4)
    
    print(f"✅ Group B Update Complete! Saved to 'live_matches_B.json'")

if __name__ == "__main__":
    main()
