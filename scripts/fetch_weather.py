import requests
import json
from datetime import datetime

# Villes à suivre : Nantes et Paris
CITIES = {
    "Nantes": {"lat": 47.2184, "lon": -1.5536},
    "Paris": {"lat": 48.8566, "lon": 2.3522},
    "Dublin": {"lat": 53.3498, "lon": -6.2603}
}

def get_weather_data(city_name: str) -> dict:
    """Interroge l'API Open-Meteo pour une ville donnée."""
    if city_name not in CITIES:
        raise ValueError(f"Ville inconnue : {city_name}")

    lat = CITIES[city_name]["lat"]
    lon = CITIES[city_name]["lon"]
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    payload = response.json()
    current = payload.get("current_weather", {})
    
    return {
        "city": city_name,
        "latitude": lat,
        "longitude": lon,
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "weathercode": current.get("weathercode"),
        "fetched_at": datetime.utcnow().isoformat()
    }