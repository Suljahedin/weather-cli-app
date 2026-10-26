
from requests.exceptions import RequestException

from weather_cli.weather import get_city_weather


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}


def run_cli():
    print("\n=== WEATHER CLI ===")

    city = input("Enter a city: ").strip()

    if not city:
        print("Error: City name cannot be empty.")
        return

    try:
        result = get_city_weather(city)
    except ValueError as error:
        print(f"Error: {error}")
        return
    except RequestException:
        print("Error: Could not connect to the weather service.")
        return

    location = result["location"]
    weather = result["weather"]

    weather_code = weather["weather_code"]
    description = WEATHER_CODES.get(
        weather_code,
        "Unknown weather conditions",
    )

    print("\n--- Current Weather ---")
    print(f"Location: {location['name']}, {location['country']}")
    print(f"Condition: {description}")
    print(f"Temperature: {weather['temperature_2m']} °C")
    print(f"Feels like: {weather['apparent_temperature']} °C")
    print(f"Humidity: {weather['relative_humidity_2m']}%")
    print(f"Wind speed: {weather['wind_speed_10m']} km/h")
    print(f"Precipitation: {weather['precipitation']} mm")
