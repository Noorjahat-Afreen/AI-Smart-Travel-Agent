
from services.geo import geocode_place
from services.places import find_places
from services.weather import get_weather_forecast
from services.wikipedia import get_destination_overview


class DestinationAgent:
    """Find destination coordinates and overview."""

    def run(self, destination):
        location = geocode_place(destination)

        if not location:
            return {
                "error": "Destination not found in OpenStreetMap data."
            }

        overview = get_destination_overview(destination)
        attractions = find_places(
            location["lat"],
            location["lon"],
            category="tourism"
        )

        return {
            "location": location,
            "overview": overview,
            "attractions": attractions
        }


class HotelAgent:
    """Discover hotels using OpenStreetMap."""

    def run(self, latitude, longitude):
        return find_places(
            latitude,
            longitude,
            category="hotel"
        )


class RestaurantAgent:
    """Discover restaurants using OpenStreetMap."""

    def run(self, latitude, longitude):
        return find_places(
            latitude,
            longitude,
            category="food"
        )


class WeatherAgent:
    """Get weather forecast using Open-Meteo."""

    def run(self, latitude, longitude, start_date=None, end_date=None):
        return get_weather_forecast(
            latitude,
            longitude,
            start_date,
            end_date
        )


class TransportAgent:
    """Transport information module."""

    def run(self, source, destination, travel_mode):
        return {
            "source": source,
            "destination": destination,
            "travel_mode": travel_mode,
            "status": "Live transport data not connected",
            "details": (
                "Verified fares, schedules and seat availability "
                "require a supported transport data provider."
            )
        }


class BudgetAgent:
    """Organize the user's travel budget."""

    def run(self, total_budget, travellers):
        return {
            "total_budget": total_budget,
            "travellers": travellers,
            "status": "Budget received",
            "note": (
                "Actual expense estimates will be calculated "
                "when verified transport and accommodation prices "
                "are available."
            )
        }


class SpecializedAgents:

    def __init__(self):
        self.destination = DestinationAgent()
        self.hotel = HotelAgent()
        self.restaurant = RestaurantAgent()
        self.weather = WeatherAgent()
        self.transport = TransportAgent()
        self.budget = BudgetAgent()
