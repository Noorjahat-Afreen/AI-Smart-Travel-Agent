
import requests
from datetime import date

from config import REQUEST_TIMEOUT, USER_AGENT


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_forecast(
    latitude,
    longitude,
    start_date=None,
    end_date=None
):
    headers = {
        "User-Agent": USER_AGENT
    }

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "weather_code"
        ),
        "timezone": "auto",
        "forecast_days": 7
    }

    try:
        response = requests.get(
            WEATHER_URL,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()
        data = response.json()

        return {
            "source": "Open-Meteo",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "current_weather": data.get("current", {}),
            "daily_forecast": data.get("daily", {}),
            "note": (
                "Forecast is limited to the dates "
                "provided by the API."
            )
        }

    except requests.RequestException as error:
        return {
            "error": "Weather data unavailable",
            "details": str(error)
        }

    except (ValueError, TypeError):
        return {
            "error": "Unable to process weather response."
        }
