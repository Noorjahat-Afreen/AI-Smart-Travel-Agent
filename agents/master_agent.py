
import os
import json

from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL


class MasterTravelAgent:

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def plan_trip(self, request):

        prompt = f"""
You are the Master AI Agent of
AI-Powered Smart Travel Agent - India.

Your task is to coordinate travel planning.

USER REQUEST:
{json.dumps(request, indent=2)}

Follow these rules:

1. Understand the source and destination.
2. Consider travel dates, travellers and budget.
3. Respect the preferred transport mode.
4. Consider hotel and food preferences.
5. Organize the plan into clear sections.
6. Do not invent hotel prices, ticket fares,
   seat availability or opening hours.
7. Do not claim that bookings are confirmed.
8. Clearly mark information that has not
   been verified as unavailable.
9. Give a practical day-wise itinerary.
10. Keep the response easy to understand.

Return these sections:

- Trip Summary
- Destination Overview
- Transport Suggestions
- Hotel Recommendations
- Restaurant Recommendations
- Tourist Attractions
- Day-wise Itinerary
- Estimated Budget
- Weather Information
- Data Verification Notes

IMPORTANT:
You must not pretend to have accessed live
data sources unless their results are provided.
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    def chat(self, message):

        prompt = f"""
You are the AI Travel Assistant for India.

Answer the user's travel question clearly.
Do not invent live prices, bookings or availability.
If information is unavailable, say so.

User question:
{message}
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text
