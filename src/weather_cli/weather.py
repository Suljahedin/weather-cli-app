
import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_json(url: str, params: dict) -> dict:
    """Send an HTTP request and return the JSON response."""
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise ValueError(
            "The weather service returned invalid JSON."
        ) from error

    if not isinstance(data, dict):
        raise ValueError(
            "The weather service returned an unexpected response."
        )

    return data


def get_coordinates(city: str) -> dict:
    """Find a city's geographical coordinates."""
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    data = fetch_json(GEOCODING_URL, params)
    results = data.get("results")

    if not results:
        raise ValueError(f"City '{city}' was not found.")

    location = results[0]

    return {
        "name": location["name"],
        "country": location.get("country", "Unknown"),
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }


def get_weather(latitude: float, longitude: float) -> dict:
    """Retrieve current weather for geographical coordinates."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "is_day,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto",
    }

    data = fetch_json(WEATHER_URL, params)

    if "current" not in data:
        raise ValueError(
            "Weather data is unavailable for this location."
        )

    return data["current"]


def get_city_weather(city: str) -> dict:
    """Find a city and retrieve its current weather."""
    location = get_coordinates(city)

    weather = get_weather(
        location["latitude"],
        location["longitude"],
    )

    return {
        "location": location,
        "weather": weather,
    }
