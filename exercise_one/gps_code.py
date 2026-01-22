# Generated this code with Chat GPT, upon suggestion by professor!

import math
import pandas as pd
import numpy as np

def parse_coord(value, is_lat: bool):
    """
    Parses coordinates like:
      40.7128° N, 74.0060° W, 48.8566 N, -0.1278, 151.2093 E, etc.
    Returns a signed float.
    """
    if pd.isna(value):
        return np.nan

    s = str(value).strip().upper()
    s = s.replace("°", "").replace(",", " ")

    # Detect hemisphere letter if present
    hemi = None
    for h in ("N", "S", "E", "W"):
        if h in s.split() or s.endswith(h) or f" {h}" in s:
            hemi = h
            s = s.replace(h, " ")
            break

    # Extract the first float-looking token
    tokens = s.split()
    num = None
    for t in tokens:
        try:
            num = float(t)
            break
        except ValueError:
            continue

    if num is None:
        raise ValueError(f"Could not parse coordinate: {value}")

    # Apply hemisphere sign if given
    if hemi:
        if is_lat and hemi not in ("N", "S"):
            raise ValueError(f"Latitude has invalid hemisphere '{hemi}' in value: {value}")
        if (not is_lat) and hemi not in ("E", "W"):
            raise ValueError(f"Longitude has invalid hemisphere '{hemi}' in value: {value}")

        if hemi in ("S", "W"):
            num = -abs(num)
        else:
            num = abs(num)

    return num

def haversine_km(lat1, lon1, lat2, lon2):
    """Vectorized haversine distance (km). lat2/lon2 can be arrays."""
    R = 6371.0
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def nearest_airport_for_cities(cities_csv, airports_csv, output_csv):
    # --- Read files ---
    cities = pd.read_csv(cities_csv)
    airports = pd.read_csv(airports_csv)

    # --- Cities: parse mixed-format lat/lon ---
    if "Latitude" not in cities.columns or "Longitude" not in cities.columns:
        raise ValueError("Cities CSV must have columns: Latitude, Longitude (case-sensitive in this script).")

    cities["lat"] = cities["Latitude"].apply(lambda v: parse_coord(v, is_lat=True))
    cities["lon"] = cities["Longitude"].apply(lambda v: parse_coord(v, is_lat=False))

    # --- Airports: numeric lat/lon + names/iata ---
    required_airport_cols = ["airport", "iata", "latitude", "longitude"]
    for col in required_airport_cols:
        if col not in airports.columns:
            raise ValueError(f"Airports CSV must have column: {col}")

    airports["lat"] = pd.to_numeric(airports["latitude"], errors="coerce")
    airports["lon"] = pd.to_numeric(airports["longitude"], errors="coerce")

    airports = airports.dropna(subset=["lat", "lon"]).reset_index(drop=True)

    airport_lats = airports["lat"].to_numpy()
    airport_lons = airports["lon"].to_numpy()

    nearest_iata = []
    nearest_airport_name = []
    nearest_dist_km = []

    # --- For each city row, compute distances to all airports and pick min ---
    for _, row in cities.iterrows():
        lat, lon = row["lat"], row["lon"]

        if pd.isna(lat) or pd.isna(lon):
            nearest_iata.append(np.nan)
            nearest_airport_name.append(np.nan)
            nearest_dist_km.append(np.nan)
            continue

        dists = haversine_km(lat, lon, airport_lats, airport_lons)
        idx = int(np.argmin(dists))

        nearest_iata.append(airports.loc[idx, "iata"])
        nearest_airport_name.append(airports.loc[idx, "airport"])
        nearest_dist_km.append(float(dists[idx]))

    # --- Output ---
    out = cities.copy()
    out["nearest_airport_iata"] = nearest_iata
    out["nearest_airport_name"] = nearest_airport_name
    out["distance_to_airport_km"] = nearest_dist_km

    out.to_csv(output_csv, index=False)
    print(f"Wrote: {output_csv}")

if __name__ == "__main__":
    nearest_airport_for_cities(
        cities_csv="cities.csv",
        airports_csv="airports.csv",
        output_csv="cities_with_nearest_airport.csv",
    )
