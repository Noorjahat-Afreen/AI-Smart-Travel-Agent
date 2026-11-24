
import json

from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL
from agents.specialized_agents import SpecializedAgents
from agents.verification_agent import VerificationAgent
from services.database import save_travel_plan, save_places


class MasterTravelAgent:

    def __init__(self):

        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key is missing.")

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.agents = SpecializedAgents()
        self.verifier = VerificationAgent()

    def plan_trip(self, request):

        source = request["source"]
        destination = request["destination"]

        # 1. Destination Agent
        destination_data = self.agents.destination.run(
            destination
        )

        if destination_data.get("error"):
            return {
                "Destination": destination_data["error"]
            }

        location = destination_data["location"]
        latitude = location["lat"]
        longitude = location["lon"]

        # 2. Hotel Agent
        hotels = self.agents.hotel.run(
            latitude, longitude
        )

        # 3. Restaurant Agent
        restaurants = self.agents.restaurant.run(
            latitude, longitude
        )

        # 4. Weather Agent
        weather = self.agents.weather.run(
            latitude,
            longitude,
            request.get("departure_date"),
            request.get("return_date")
        )

        # 5. Transport Agent
        transport = self.agents.transport.run(
            source,
            destination,
            request.get("travel_mode", "Train")
        )

        # 6. Budget Agent
        budget = self.agents.budget.run(
            request.get("budget", 0),
            request.get("travellers", 1)
        )

        # 7. Verification Agent
        hotel_check = self.verifier.verify_places(hotels)
        restaurant_check = self.verifier.verify_places(
            restaurants
        )

        verified_hotels = hotel_check["verified_places"]
        verified_restaurants = restaurant_check["verified_places"]

        collected_data = {
            "destination": destination_data,
            "hotels": verified_hotels,
            "restaurants": verified_restaurants,
            "weather": weather,
            "transport": transport,
            "budget": budget
        }

        # 8. Save collected places
        all_places = (
            verified_hotels + verified_restaurants
        )

        save_places(all_places)

        # 9. Generate final plan
        prompt = f"""
You are the Master AI Agent of
AI-Powered Smart Travel Agent - India.

Create a personalized travel plan using
ONLY the collected data below.

USER REQUEST:
{json.dumps(request, indent=2, default=str)}

COLLECTED DATA:
{json.dumps(collected_data, indent=2, default=str)}

RULES:
1. Never invent hotel or restaurant details.
2. Never invent ticket fares or seat availability.
3. Never claim that a booking is confirmed.
4. Use only collected destination information.
5. Missing details must be written exactly:
   details unavailable in collected data
6. Clearly distinguish verified data from estimates.
7. Organize the itinerary day by day.
8. Respect the user's budget and preferences.
9. Mention when live transport data is unavailable.

OUTPUT:
- Trip Summary
- Destination Overview
- Transport Information
- Hotel Recommendations
- Restaurant Recommendations
- Tourist Attractions
- Day-wise Itinerary
- Budget Information
- Weather Information
- Data Verification Notes
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        final_plan = {
            "Complete Travel Plan": response.text,
            "Collected Data": collected_data,
            "Verification": {
                "hotels": hotel_check,
                "restaurants": restaurant_check
            }
        }

        # 10. Save final travel plan
        save_travel_plan(request, final_plan)

        return final_plan

    def chat(self, message):

        prompt = f"""
You are an India Travel Assistant.

Answer the user's travel question clearly.
Do not invent prices, availability or bookings.
If information is missing, say so.

Question: {message}
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text
