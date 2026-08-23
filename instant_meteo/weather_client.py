import requests
from datetime import datetime, timezone

CITIES = {
    "Nantes": {"lat": 47.2184, "lon": -1.5536},
}

WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather_for_city(city_name: str = "Nantes") -> dict:
    city_name = city_name.strip().title()
    if city_name not in CITIES:
        raise ValueError(f"Ville inconnue : {city_name}")

    city = CITIES[city_name]
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": city["lat"],
            "longitude": city["lon"],
            "current_weather": "true",
            "timezone": "auto",
        },
        timeout=10,
    )
    response.raise_for_status()

    payload = response.json()
    current = payload.get("current_weather", {})
    weather_code = current.get("weathercode")

    return {
        "city": city_name,
        "temperature_celsius": current.get("temperature"),
        "windspeed_kmh": current.get("windspeed"),
        "weather_code": weather_code,
        "weather_description": WEATHER_DESCRIPTIONS.get(weather_code, "Weather conditions"),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
