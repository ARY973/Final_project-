# -------------------------------------------------------
# FINAL PROJECT - Global Aviation CO₂ Emissions Analysis
# -------------------------------------------------------
# This program:
#   1. Fetches global airborne flights from OpenSky API
#   2. Estimates aircraft type using callsigns
#   3. Loads ICAO emissions factors per aircraft type
#   4. Estimates hourly CO₂ emissions for each aircraft
#   5. Stores data in flights.csv (append-only)
#   6. Computes total global CO₂ emissions and top emitters
#   7. Saves results in results.json
# -------------------------------------------------------

import requests
import csv
import os
import json
from datetime import datetime, timezone
CSV_FILE = "flights.csv"
#📂 FUNCTION: Create CSV if missing
def create_csv_if_needed():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "icao24",
                "callsign",
                "aircraft_type",
                "latitude",
                "longitude",
                "altitude_meters",
                "velocity_m_s",
                "estimated_co2_kg"
            ])

# ------------------------------
# STEP 1: Load ICAO emissions dataset
# ------------------------------

def load_emissions_data():
    with open("icao_emissions.json", "r") as f:
        return json.load(f)


# ------------------------------
# STEP 2: Fetch global flight data
# ------------------------------

OPENSKY_URL = "https://opensky-network.org/api/states/all"

#✈️ FUNCTION: Fetch global flight data
def fetch_global_flights():
    """
    Fetch all airborne flights globally from OpenSky API.
    Returns a list of dicts with cleaned data: id, callsign, lat, lon, altitude, velocity.
    """
    response = requests.get(OPENSKY_URL)
    data = response.json()

    flights = []

    for state in data.get("states", []):
        flights.append({
            "icao24": state[0],
            "callsign": (state[1] or "").strip(),
            "origin_country": state[2],
            "longitude": state[5],
            "latitude": state[6],
            "altitude": state[7],
            "velocity": state[9]
        })

    return flights

# TEMPORARY TEST
if __name__ == "__main__":
    sample = fetch_global_flights()
    print("Number of flights currently airborne:", len(sample))
    print("First 3 flights:", sample[:3])
#🛩️ FUNCTION: Estimate aircraft type
def estimate_aircraft_type(callsign):
    if not callsign:
        return "DEFAULT"
    
    cs = callsign.upper()

    # Airline fleet heuristics
    if cs.startswith(("UAL",)): return "B737"
    if cs.startswith(("AAL",)): return "B737"
    if cs.startswith(("DAL",)): return "A320"
    if cs.startswith(("SWR",)): return "A320"
    if cs.startswith(("AFR",)): return "A320"
    if cs.startswith(("BAW",)): return "A320"
    if cs.startswith(("QFA",)): return "B787"
    if cs.startswith(("JAL",)): return "B787"
    if cs.startswith(("ANA",)): return "B787"
    
    # Regional airlines
    if cs.startswith(("SKW", "ENY")): return "E175"
    if cs.startswith(("ASH",)): return "CRJ7"
#🌫️ FUNCTION: Estimate CO₂ emissions
    return "DEFAULT"
def estimate_co2(emissions_db, aircraft_type, velocity_kmh):
    """
    Estimate CO₂ emissions using ICAO per-km values.
    velocity_kmh = current speed; we assume 1 hour of travel.
    """
    if not velocity_kmh:
        return 0.0

    co2_factor = emissions_db.get(aircraft_type, emissions_db["DEFAULT"])["co2_kg_per_km"]

    distance_km = velocity_kmh  # velocity * 1 hour
    return round(distance_km * co2_factor, 2)
if __name__ == "__main__":
    flights = fetch_global_flights()
    emissions_db = load_emissions_data()

    print("Sample flight:", flights[0])
    
    cs = flights[0]["callsign"]
    plane = estimate_aircraft_type(cs)
    print("Estimated aircraft:", plane)

    speed = flights[0]["velocity"] * 3.6  # convert m/s → km/h
    co2 = estimate_co2(emissions_db, plane, speed)
    print("Estimated CO₂ for 1 hour:", co2, "kg")
#➕ FUNCTION: Append flight data to CSV    
def append_flight_data(flights, emissions_db):
    from datetime import timezone
...
now = datetime.now(timezone.utc).isoformat()



with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        for flight in flights:
            callsign = flight["callsign"]
            aircraft_type = estimate_aircraft_type(callsign)

            # convert m/s → km/h
            velocity_kmh = (flight["velocity"] or 0) * 3.6

            co2 = estimate_co2(emissions_db, aircraft_type, velocity_kmh)

            writer.writerow([
                now,
                flight["icao24"],
                callsign,
                aircraft_type,
                flight["latitude"],
                flight["longitude"],
                flight["altitude"],
                flight["velocity"],
                co2
            ])
#📊 FUNCTION: Analyze global CO₂
def analyze_global_emissions():
    total_co2 = 0
    aircraft_counts = {}
    type_co2 = {}

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            co2 = float(row["estimated_co2_kg"])
            atype = row["aircraft_type"]

            total_co2 += co2

            aircraft_counts[atype] = aircraft_counts.get(atype, 0) + 1
            type_co2[atype] = type_co2.get(atype, 0) + co2

    top_emitters = sorted(type_co2.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "total_global_co2_kg": round(total_co2, 2),
        "top_5_aircraft_types_by_emissions": top_emitters,
        "most_common_aircraft_type": max(aircraft_counts, key=aircraft_counts.get)
    }
#💾 FUNCTION: Save JSON results
def save_results(results):
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)
#▶️ MAIN EXECUTION BLOCK
if __name__ == "__main__":
    print("Fetching flights...")
    flights = fetch_global_flights()
    print("Flights fetched:", len(flights))

    emissions_db = load_emissions_data()

    print("Preparing CSV...")
    create_csv_if_needed()

    print("Appending flight data...")
    append_flight_data(flights, emissions_db)

    print("Running analysis...")
    results = analyze_global_emissions()

    print("Saving results.json...")
    save_results(results)

    print("DONE!")
    print(results)


