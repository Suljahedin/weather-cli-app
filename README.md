# Weather CLI

A command-line weather application built with Python that retrieves current weather conditions for a city using the [Open-Meteo API](https://open-meteo.com/).

## Features

- Search for a city by name
- Retrieve geographical coordinates using the Open-Meteo Geocoding API
- Display current weather conditions
- Show temperature, feels-like temperature, humidity, wind speed, and precipitation
- Handle missing cities and HTTP errors
- Automated tests using `pytest`

## Technologies

- Python 3.12+
- Requests
- Open-Meteo API
- pytest
- Git

## Requirements

- Python 3.12 or newer
- Internet connection

## Installation

Clone the repository:

```bash
git clone https://github.com/Suljahedin/weather-cli-app.git
cd weather-cli-app
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Install the project and its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Usage

Run the application:

```bash
python -m weather_cli
```

Enter the name of a city when prompted.

Example:

```text
=== WEATHER CLI ===
Enter a city: Sarajevo

--- Current Weather ---
Location: Sarajevo, Bosnia and Herzegovina
Condition: Partly cloudy
Temperature: 18.5 °C
Feels like: 17.9 °C
Humidity: 60%
Wind speed: 12.0 km/h
Precipitation: 0.0 mm
```

_The values above are illustrative. Actual weather conditions change over time._

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The tests use mocks to simulate API responses, so they do not require live weather data.

## API

This project uses the free [Open-Meteo API](https://open-meteo.com/):

- [Geocoding API](https://open-meteo.com/en/docs/geocoding-api) — finds geographical coordinates for a city.
- [Weather API](https://open-meteo.com/en/docs) — retrieves current weather conditions.

No API key is required for this project's basic use.

## Project Structure

```text
weather-cli-app/
├── src/
│   └── weather_cli/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── weather.py
├── tests/
│   ├── __init__.py
│   └── test_weather.py
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

## License

See the [LICENSE](LICENSE) file for details.
