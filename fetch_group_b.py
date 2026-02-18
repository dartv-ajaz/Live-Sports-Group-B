import requests
import json
from datetime import datetime
import pytz

def get_hotstar_matches():
    print("Fetching Hotstar...")
    url = "https://api.hotstar.com/o/v1/page/1558?app_version=9.15.0"
    headers = {
        "x-hs-platform": "android",
        "User-Agent": "Hotstar;in.startv.hotstar/9.15.0 (Android/10)"
    }

    allowed_sports = ['cricket', 'hockey', 'kabaddi']
    matches = []

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        items = data.get("body", {}).get("results", {}).get("items", [])

        for item in items:
            title = item.get("title", "").lower()
            if any(sport in title for sport in allowed_sports):
                matches.append({
                    "id": str(item.get("contentId")),
                    "platform": "Hotstar",
                    "sport": "Sports",
                    "title": item.get("title"),
                    "team_1": "Hotstar",
                    "team_2": "Live",
                    "url": f"https://www.hotstar.com/{item.get('contentId')}", # Needs parser on frontend
                    "license_url": "https://license.drm.hotstar.com/widevine/v1/play",
                    "type": "DRM",
                    "is_drm": True
                })
    except Exception as e:
        print(f"Hotstar Error: {e}")
    
    return matches

def main():
    hotstar = get_hotstar_matches()
    # Amazon Prime logic can be added here
    
    all_matches = hotstar
    
    output = {
        "updated_at": datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M:%S %p"),
        "matches": all_matches
    }

    with open('live_matches_B.json', 'w') as f:
        json.dump(output, f, indent=4)
    print(f"Saved {len(all_matches)} matches to live_matches_B.json")

if __name__ == "__main__":
    main()
