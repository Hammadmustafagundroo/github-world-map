import urllib.request
import json
import random
import xml.etree.ElementTree as ET
from cities import CITIES
import os

USERNAME = "Hammadmustafagundroo"
TOKEN = os.getenv("GH_TOKEN")

SVG_FILE = "assets/world.svg"
OUTPUT_FILE = "assets/world-map.svg"
DOT_COLOR = "#22c55e"

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

def github_api(url):
    req = urllib.request.Request(url)
    if TOKEN:
        req.add_header("Authorization", f"token {TOKEN}")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode()), r.headers

# ─────────────────────────────
# 1️⃣ Get all public repos
# ─────────────────────────────
repos, _ = github_api(
    f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
)

total_commits = 0

for repo in repos:
    name = repo["name"]
    commits_url = f"https://api.github.com/repos/{USERNAME}/{name}/commits?per_page=1"
    _, headers = github_api(commits_url)

    link = headers.get("Link", "")

    # Safe commit counting
    if 'rel="last"' in link:
        try:
            last_page = int(link.split("page=")[-1].split(">")[0])
            total_commits += last_page
        except Exception:
            total_commits += 1
    else:
        total_commits += 1

print(f"Total commits found: {total_commits}")

# ─────────────────────────────
# 2️⃣ Load SVG + viewBox
# ─────────────────────────────
tree = ET.parse(SVG_FILE)
root = tree.getroot()

viewBox = root.attrib.get("viewBox")
min_x, min_y, width, height = map(float, viewBox.split())

def latlon_to_xy(lat, lon):
    x = min_x + (lon + 180) * (width / 360)
    y = min_y + (90 - lat) * (height / 180)
    return x, y

# ─────────────────────────────
# 3️⃣ Draw commit dots
# ─────────────────────────────
random.seed(total_commits)
dot_count = min(total_commits, len(CITIES) * 6)

for _ in range(dot_count):
    city, lat, lon = random.choice(CITIES)
    x, y = latlon_to_xy(lat, lon)

    ET.SubElement(
        root,
        f"{{{SVG_NS}}}circle",
        {
            "cx": str(x),
            "cy": str(y),
            "r": "3",
            "fill": DOT_COLOR,
            "fill-opacity": "0.85"
        }
    )

tree.write(OUTPUT_FILE)
print("✅ World map generated successfully")
