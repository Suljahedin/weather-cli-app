
from unittest.mock import Mock, patch

import pytest, requests

from weather_cli.weather import (
    fetch_json,
    get_city_weather,
    get_coordinates,
    get_weather,
)

@patch("weather_cli.weather.requests.get")
def test_get_coordinates_returns_city_data(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Sarajevo",
                "country": "Bosnia and Herzegovina",
                "latitude": 43.8563,
                "longitude": 18.4131,
            }
        ]
    }

    mock_get.return_value = mock_response

    result = get_coordinates("Sarajevo")

    assert result["name"] == "Sarajevo"
    assert result["country"] == "Bosnia and Herzegovina"
    assert result["latitude"] == 43.8563
    assert result["longitude"] == 18.4131


@patch("weather_cli.weather.requests.get")
def test_get_coordinates_raises_error_when_city_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"results": None}
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="was not found"):
        get_coordinates("NonexistentCity")



@patch("weather_cli.weather.requests.get")
def test_get_weather_returns_current_weather(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "current": {
            "temperature_2m": 18.5,
            "relative_humidity_2m": 60,
            "apparent_temperature": 17.9,
            "is_day": 1,
            "precipitation": 0.0,
            "weather_code": 2,
            "wind_speed_10m": 12.0,
        }
    }

    mock_get.return_value = mock_response

    result = get_weather(43.8563, 18.4131)

    assert result["temperature_2m"] == 18.5
    assert result["relative_humidity_2m"] == 60
    assert result["weather_code"] == 2

    mock_get.assert_called_once()


@patch("weather_cli.weather.get_weather")
@patch("weather_cli.weather.get_coordinates")
def test_get_city_weather_combines_location_and_weather(
    mock_coordinates,
    mock_weather,
):
    mock_coordinates.return_value = {
        "name": "Sarajevo",
        "country": "Bosnia and Herzegovina",
        "latitude": 43.8563,
        "longitude": 18.4131,
    }

    mock_weather.return_value = {
        "temperature_2m": 18.5,
        "relative_humidity_2m": 60,
        "apparent_temperature": 17.9,
        "is_day": 1,
        "precipitation": 0.0,
        "weather_code": 2,
        "wind_speed_10m": 12.0,
    }

    result = get_city_weather("Sarajevo")

    assert result["location"]["name"] == "Sarajevo"
    assert result["weather"]["temperature_2m"] == 18.5

    mock_coordinates.assert_called_once_with("Sarajevo")
    mock_weather.assert_called_once_with(43.8563, 18.4131)


@patch("weather_cli.weather.requests.get")
def test_fetch_json_returns_response_data(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"status": "ok"}
    mock_get.return_value = mock_response

    result = fetch_json(
        "https://example.com/api",
        {"city": "Sarajevo"},
    )

    assert result == {"status": "ok"}
    mock_response.raise_for_status.assert_called_once()


@patch("weather_cli.weather.requests.get")
def test_fetch_json_raises_error_for_invalid_json(mock_get):
    mock_response = Mock()
    mock_response.json.side_effect = (
        requests.exceptions.JSONDecodeError(
            "Invalid JSON",
            "invalid",
            0,
        )
    )
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="invalid JSON"):
        fetch_json("https://example.com/api", {})
