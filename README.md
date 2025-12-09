# Final_project-
# Global Aviation CO₂ Emissions Analyzer  
### Final Project – Data Analytics & Python Programming  
### Ryan Mudhole (ARY973)

---

## 📌 Overview
This project analyzes **global aviation CO₂ emissions in real time** using two data sources:

1. **OpenSky Network API** – live flight positions worldwide  
2. **ICAO Aircraft Emissions Dataset** – CO₂ per km per aircraft type  

Each time the program runs, it:

- Fetches 10,000+ airborne flights  
- Estimates aircraft type from callsigns  
- Calculates hourly CO₂ emissions for each aircraft  
- Stores results in a growing CSV dataset  
- Computes global emissions statistics  
- Saves results to `results.json`

This project demonstrates API consumption, JSON parsing, CSV storage, loops, functions, environmental analytics, and reproducible data pipelines.

---

## 🌍 Data Sources

### ✈️ 1. OpenSky Network – Live Aircraft States  
Public endpoint (no API key required):
https://opensky-network.org/api/states/all


This returns ~10,000+ live aircraft including:

- aircraft ID (icao24)  
- callsign  
- latitude & longitude  
- altitude  
- velocity  

### 🛩 2. ICAO Emissions Factors  
Stored locally as:
icao_emissions.json


This file includes CO₂ emissions per km for:

- A320, A321, A330, A350  
- B737, B747, B757, B767, B777, B787  
- E175, E190, CRJ series  
- DEFAULT fallback  

---

## 📂 Folder Structure
final_project/
│
├── final_project.py # Main program logic
├── icao_emissions.json # Emissions factors per aircraft type
├── flights.csv # Appended flight dataset (grows each run)
├── results.json # Latest global analysis output
└── README.md # Project documentation


---

## 🔧 How to Run

Inside the `final_project` folder:

This will:

- Fetch live flight data  
- Append to `flights.csv`  
- Compute global CO₂ totals  
- Save results in `results.json`  

---

## 📊 Example Output (`results.json`)

{
"total_global_co2_kg": 1086342833.96,
"top_5_aircraft_types_by_emissions": [
["DEFAULT", 871782102.0],
["B737", 102532974.39],
["A320", 76489760.97],
["E175", 21827970.21],
["B787", 11086716.47]
],
"most_common_aircraft_type": "DEFAULT"
}


