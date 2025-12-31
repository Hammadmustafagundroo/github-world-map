CITIES = []

# Land-only bounding boxes (lat_min, lat_max, lon_min, lon_max)
LAND_BOXES = [
    # North America
    (15, 70, -170, -50),

    # South America
    (-55, 15, -85, -35),

    # Europe
    (35, 70, -10, 40),

    # Africa
    (-35, 35, -20, 50),

    # Middle East
    (12, 40, 30, 65),

    # South Asia (India etc.)
    (5, 35, 65, 95),

    # East Asia
    (20, 50, 95, 145),

    # Southeast Asia
    (-10, 20, 95, 130),

    # Australia
    (-45, -10, 110, 155),

    # Russia / North Asia
    (50, 70, 40, 180),
]

LAT_STEP = 2
LON_STEP = 3

for lat_min, lat_max, lon_min, lon_max in LAND_BOXES:
    lat = lat_min
    while lat <= lat_max:
        lon = lon_min
        while lon <= lon_max:
            CITIES.append(("city", lat, lon))
            lon += LON_STEP
        lat += LAT_STEP

# Final safety check (CI-safe)
TOTAL = len(CITIES)
if TOTAL < 4200:
    raise RuntimeError(
        f"City generation failed: only {TOTAL} points (need ~4200)"
    )
