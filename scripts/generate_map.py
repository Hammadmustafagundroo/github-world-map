import urllib.request
import json
import random
import xml.etree.ElementTree as ET
from cities import CITIES

USERNAME = "Hammadmustafagundroo"
DOT_COLOR = "#22c55e"

SVG_WIDTH = 2000
SVG_HEIGHT = 1001

def latlon_to_xy(lat, lon):
    x = (lon + 180) * (SVG_WIDTH / 360)
    y = (90 - lat) * (SVG_HEIGHT / 180)
    return x, y

# Fetch GitHub events (NO requests, built-in only)
url = f"https://api.github.com/users/{USERNAME}/events/public"

with urllib.request.urlopen(url) as response:
    events = json.loads(response.read().decode())

# Count commits
commit_count = sum(
    1 for e in events if e.get("type") == "PushEvent"
)

print(f"Commits found: {commit_count}")

# Load SVG
tree = ET.parse("assets/world.svg")
root = tree.getroot()

# Choose random cities
chosen_cities = random.sample(CITIES, min(commit_count, len(CITIES)))

for city, lat, lon in chosen_cities:
    x, y = latlon_to_xy(lat, lon)
    ET.SubElement(
        root,
        "circle",
        {
            "cx": str(x),
            "cy": str(y),
            "r": "4",
            "fill": DOT_COLOR,
            "fill-opacity": "0.85"
        }
    )

# Save output
tree.write("assets/world-map.svg")
print("✅ world-map.svg generated successfully")
