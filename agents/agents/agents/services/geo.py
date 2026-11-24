
import requests

from config import REQUEST_TIMEOUT, USER_AGENT


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode_place(place_name):

    if not place_name or not place_name.strip():
        return None

    headers = {
        "User-Agent": USER_AGENT
    }

    params = {
        "q": place_name.strip() + ", India",
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "in"
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()
        results = response.json()

        if not results:
            return None

        place = results[0]

        return {
            "name": place.get("display_name", place_name),
            "lat": float(place["lat"]),
            "lon": float(place["lon"]),
            "source": "OpenStreetMap Nominatim"
        }

    except requests.RequestException:
        return None

    except (ValueError, KeyError, TypeError):
        return None
