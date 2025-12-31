# scripts/cities.py

CITIES = []

# Dense global grid biased toward habitable latitudes
LAT_RANGES = [
    (-55, -30),
    (-30, -10),
    (-10, 10),
    (10, 30),
    (30, 55),
    (55, 70),
]

for lat_min, lat_max in LAT_RANGES:
    lat = lat_min
    while lat <= lat_max:
        lon = -180
        while lon <= 180:
            CITIES.append((
                "city",
                lat,
                lon
            ))
            lon += 3     # longitude resolution
        lat += 2        # latitude resolution

# Final safety check (CI-safe)
TOTAL = len(CITIES)

# ~5000 global points is more than enough for all commits
if TOTAL < 5000:
    raise RuntimeError(
        f"City generation failed: only {TOTAL} points (need ~5000)"
    )

