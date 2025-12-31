import urllib.request
import json
import random
import xml.etree.ElementTree as ET
from cities import CITIES
import os

USERNAME = "Hammadmustafagundroo"
TOKEN = os.getenv("GH_TOKEN")
DOT_COLOR = "#22c55e"

SVG_WIDTH = 2000
SVG_HEIGHT = 1001

def latlon_to_xy(lat, lon):
    x = (lon + 180) * (SVG_WIDTH / 360)
    y = (90 - lat) * (SVG_HEIGHT / 180)
    return x, y

def github_api(url):
    req = urllib.request.Request(url)
    if TOKEN:
        req.add_header("Authorization", f"token {TOKEN}")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

# 1️⃣ Get all repositories
repos = github_api(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")

total_commits = 0

# 2️⃣ Count commits in each repo
for repo in repos:
    name = repo["name"]
    commits_url = f"https://api.github.com/repos/{USERNAME}/{name}/commits?per_page=1"
    req = urllib.request.Request(commits_url)
    if TOKEN:
        req.add_header("Authorization", f"token {TOKEN}")
    with urllib.request.urlopen(req) as response:
        link = response.headers.get("Link")
        if link and 'rel="last"' in link:
            last_page = int(link.split("page=")[-1].split(">")[0])
            total_commits += last_page
        else:
            total_commits += 1

print(f"Total commits found: {total_commits}")

# 3️⃣ Generate dots
tree = ET.parse("assets/world.svg")
root = tree.getroot()

random.seed(total_commits)
dots = min(total_commits, len(CITIES) * 5)

for _ in range(dots):
    city, lat, lon = random.choice(CITIES)
    x, y = latlon_to_xy(lat, lon)
    ET.SubElement(
        root,
        "circle",
        {
            "cx": str(x),
            "cy": str(y),
            "r": "3",
            "fill": DOT_COLOR,
            "fill-opacity": "0.75"
        }
    )

tree.write("assets/world-map.svg")
print("✅ World map generated from FULL commit history")
