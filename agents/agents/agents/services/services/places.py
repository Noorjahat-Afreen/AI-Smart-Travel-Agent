
import requests
import time

from config import REQUEST_TIMEOUT, USER_AGENT


OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]


CATEGORY_FILTERS = {
    "hotel": """
        node["tourism"="hotel"](around:{radius},{lat},{lon});
        way["tourism"="hotel"](around:{radius},{lat},{lon});
        relation["tourism"="hotel"](around:{radius},{lat},{lon});
        node["tourism"="guest_house"](around:{radius},{lat},{lon});
        way["tourism"="guest_house"](around:{radius},{lat},{lon});
    """,

    "food": """
        node["amenity"="restaurant"](around:{radius},{lat},{lon});
        way["amenity"="restaurant"](around:{radius},{lat},{lon});
        node["amenity"="cafe"](around:{radius},{lat},{lon});
        node["amenity"="fast_food"](around:{radius},{lat},{lon});
    """,

    "tourism": """
        node["tourism"~"attraction|museum|viewpoint"](around:{radius},{lat},{lon});
        way["tourism"~"attraction|museum|viewpoint"](around:{radius},{lat},{lon});
        node["historic"](around:{radius},{lat},{lon});
    """
}


def find_places(latitude, longitude, category, radius=5000):

    if category not in CATEGORY_FILTERS:
        return []

    query = f"""
    [out:json][timeout:25];
    (
        {CATEGORY_FILTERS[category].format(
            radius=int(radius),
            lat=float(latitude),
            lon=float(longitude)
        )}
    );
    out center tags;
    """

    headers = {
        "User-Agent": USER_AGENT
    }

    for endpoint in OVERPASS_URLS:

        try:
            response = requests.post(
                endpoint,
                data={"data": query},
                headers=headers,
                timeout=REQUEST_TIMEOUT + 10
            )

            response.raise_for_status()
            elements = response.json().get("elements", [])

            places = []

            for item in elements:

                tags = item.get("tags", {})

                name = tags.get("name")

                if not name:
                    continue

                center = item.get("center", {})

                lat = item.get("lat", center.get("lat"))
                lon = item.get("lon", center.get("lon"))

                places.append({
                    "name": name,
                    "category": category,
                    "latitude": lat,
                    "longitude": lon,
                    "address": tags.get("addr:full")
                    or tags.get("addr:street")
                    or "details unavailable in collected data",
                    "website": tags.get("website")
                    or "details unavailable in collected data",
                    "cuisine": tags.get("cuisine")
                    or "details unavailable in collected data",
                    "source": "OpenStreetMap"
                })

            return places

        except requests.RequestException:
            time.sleep(1)
            continue

        except (ValueError, TypeError):
            continue

    return []
