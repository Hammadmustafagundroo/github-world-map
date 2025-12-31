import random

# Deterministic seed so locations stay stable across runs
random.seed(42)

CITIES = []

# Latitude bands that roughly match human population density
LAT_BANDS = [
    (-55, -30, 0.3),   # Southern mid
    (-30, -10, 0.6),
    (-10, 10, 1.2),    # Equatorial (dense)
    (10, 30, 1.3),
    (30, 50, 1.1),     # Europe / US / East Asia
    (50, 65, 0.6),
]

for lat_min, lat_max, density in LAT_BANDS:
    lat = lat_min
    while lat < lat_max:
        lon = -180
        while lon < 180:
            # Bias toward land / population centers
            if random.random() < 0.22 * density:
                jitter_lat = random.uniform(-1.2, 1.2)
                jitter_lon = random.uniform(-1.8, 1.8)

                CITIES.append((
                    "city",
                    lat + jitter_lat,
                    lon + jitter_lon
                ))

            lon += 4      # longitude resolution
        lat += 3          # latitude resolution

# Safety check
if len(CITIES) < 10000:
    raise RuntimeError(f"City generation failed: only {len(CITIES)} points")

