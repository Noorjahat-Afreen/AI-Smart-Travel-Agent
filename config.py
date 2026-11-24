
import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = "AI-Powered Smart Travel Agent - India"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

REQUEST_TIMEOUT = 20
USER_AGENT = "SmartTravelAgentIndia/1.0"
PORT = int(os.environ.get("PORT", 7860))
