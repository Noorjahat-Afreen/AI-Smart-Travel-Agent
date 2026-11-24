
import os
import gradio as gr

from config import APP_TITLE, PORT

# -------------------------------
# 1. MASTER AI AGENT
# -------------------------------

def run_master_agent(
    source,
    destination,
    departure_date,
    return_date,
    travellers,
    budget,
    travel_mode,
    interests,
    hotel_preference,
    food_preference
):
    if not source.strip() or not destination.strip():
        return "Please enter source and destination."

    request = {
        "source": source,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "travellers": int(travellers or 1),
        "budget": float(budget or 0),
        "travel_mode": travel_mode,
        "interests": interests,
        "hotel_preference": hotel_preference,
        "food_preference": food_preference
    }

    # Connect the Master Agent when backend is ready.
    try:
        from agents.master_agent import MasterTravelAgent

        agent = MasterTravelAgent()
        result = agent.plan_trip(request)

        if isinstance(result, dict):
            return format_result(result)

        return str(result)

    except ImportError:
        return (
            "## Travel Request Received\n\n"
            f"**Journey:** {source} → {destination}\n\n"
            f"**Dates:** {departure_date} to {return_date}\n\n"
            f"**Travellers:** {int(travellers or 1)}\n\n"
            f"**Budget:** ₹{budget}\n\n"
            f"**Travel Mode:** {travel_mode}\n\n"
            "### Agent Status\n"
            "- User Interface: Active\n"
            "- Master AI Agent: Backend connection pending\n"
            "- Specialized Agents: Backend connection pending\n"
            "- Public Data Sources: Integration pending\n\n"
            "This is a project interface preview, not a live trip plan."
        )

    except Exception as error:
        return (
            "## Travel planning could not be completed\n\n"
            f"Error: {str(error)}\n\n"
            "Please check the agent backend and API configuration."
        )


def format_result(result):
    if isinstance(result, dict):
        lines = []
        for key, value in result.items():
            lines.append(f"### {str(key).replace('_', ' ').title()}\n\n{value}")
        return "\n\n".join(lines)

    return str(result)


# -------------------------------
# 2. IMAGE / VISION AGENT
# -------------------------------

def analyze_image(image):
    if image is None:
        return "Please upload an image first."

    try:
        from services.vision import analyze_image as vision_analysis
        result = vision_analysis(image)
        return str(result)

    except ImportError:
        return (
            "OpenCV Vision Agent backend is not connected yet. "
            "The image was received successfully."
        )

    except Exception as error:
        return f"Image analysis error: {str(error)}"


# -------------------------------
# 3. CHAT INTERFACE
# -------------------------------

def travel_chat(message, history):
    if not message.strip():
        return "Please enter your travel question."

    try:
        from agents.master_agent import MasterTravelAgent

        agent = MasterTravelAgent()
        result = agent.chat(message)

        return str(result)

    except (ImportError, AttributeError):
        return (
            "Travel Assistant: I can help plan trips across India. "
            "Please use the trip planner to enter your source, "
            "destination, dates and budget. The AI chat backend "
            "is still being connected."
        )

    except Exception as error:
        return f"Assistant error: {str(error)}"


# -------------------------------
# 4. USER INTERFACE
# -------------------------------

with gr.Blocks(
    title=APP_TITLE,
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # ✈️ AI-POWERED SMART TRAVEL AGENT
        ### Your Intelligent Multi-Agent Travel Planner for India

        Plan journeys, explore destinations, discover hotels,
        restaurants and tourist attractions.
        """
    )

    with gr.Tabs():

        # TRIP PLANNER
        with gr.Tab("🧳 Trip Planner"):

            gr.Markdown("## Enter Your Travel Details")

            with gr.Row():
                source = gr.Textbox(
                    label="Starting City",
                    placeholder="e.g. Indore"
                )

                destination = gr.Textbox(
                    label="Destination",
                    placeholder="e.g. Manali"
                )

            with gr.Row():
                departure_date = gr.Textbox(
                    label="Departure Date",
                    placeholder="YYYY-MM-DD"
                )

                return_date = gr.Textbox(
                    label="Return Date",
                    placeholder="YYYY-MM-DD"
                )

            with gr.Row():
                travellers = gr.Number(
                    label="Number of Travellers",
                    value=1,
                    precision=0
                )

                budget = gr.Number(
                    label="Total Budget (₹)",
                    value=15000,
                    precision=0
                )

            with gr.Row():
                travel_mode = gr.Dropdown(
                    choices=["Train", "Bus", "Flight", "Car"],
                    label="Preferred Transport",
                    value="Train"
                )

                hotel_preference = gr.Dropdown(
                    choices=["Budget", "Standard", "Luxury"],
                    label="Hotel Preference",
                    value="Budget"
                )

            with gr.Row():
                interests = gr.Textbox(
                    label="Travel Interests",
                    placeholder="Nature, adventure, sightseeing..."
                )

                food_preference = gr.Dropdown(
                    choices=[
                        "Local / Street Food",
                        "Vegetarian",
                        "Non-Vegetarian",
                        "Any"
                    ],
                    label="Food Preference",
                    value="Any"
                )

            generate = gr.Button(
                "🚀 Generate Complete Trip Plan",
                variant="primary"
            )

            trip_output = gr.Markdown(
                label="Travel Plan"
            )

            generate.click(
                fn=run_master_agent,
                inputs=[
                    source,
                    destination,
                    departure_date,
                    return_date,
                    travellers,
                    budget,
                    travel_mode,
                    interests,
                    hotel_preference,
                    food_preference
                ],
                outputs=trip_output
            )

        # MULTI-AGENT ARCHITECTURE
        with gr.Tab("🤖 AI Agents"):

            gr.Markdown(
                """
                ## Multi-Agent System

                The Master AI Agent coordinates specialized agents.
                """
            )

            agent_data = [
                ["Master AI Agent", "Gemini-powered planning and coordination"],
                ["Destination Agent", "Destination details and attractions"],
                ["Transport Agent", "Train, bus and flight information"],
                ["Hotel Agent", "Hotel discovery"],
                ["Restaurant Agent", "Restaurant and food discovery"],
                ["Weather Agent", "Weather information"],
                ["Budget Agent", "Estimated trip budget"],
                ["Vision Agent", "Image processing using OpenCV"],
                ["Verification Agent", "Checks collected information"]
            ]

            gr.Dataframe(
                headers=["Agent", "Responsibility"],
                value=agent_data,
                interactive=False
            )

        # VISION AGENT
        with gr.Tab("📷 Image Recognition"):

            gr.Markdown(
                """
                ## Computer Vision Agent
                Upload a destination or landmark image for analysis.
                """
            )

            image_input = gr.Image(
                label="Upload Image",
                type="filepath"
            )

            analyze_button = gr.Button(
                "Analyze Image",
                variant="primary"
            )

            image_output = gr.Markdown()

            analyze_button.click(
                fn=analyze_image,
                inputs=image_input,
                outputs=image_output
            )

        # CHAT ASSISTANT
        with gr.Tab("💬 Travel AI Chat"):

            gr.Markdown(
                "## Ask Your Travel Assistant"
            )

            gr.ChatInterface(
                fn=travel_chat,
                chatbot=gr.Chatbot(height=400),
                textbox=gr.Textbox(
                    placeholder="Ask about your India trip..."
                )
            )

        # DATA SOURCES
        with gr.Tab("🌐 Data Sources"):

            gr.Markdown(
                """
                ## Public Data Sources

                | Source | Purpose |
                |---|---|
                | OpenStreetMap | Hotels, restaurants and attractions |
                | Nominatim | Location coordinates |
                | Open-Meteo | Weather forecast |
                | Wikipedia | Destination overview |
                | OpenCV | Image processing |
                | SQLite | Local project database |
                | Gemini API | AI reasoning and planning |

                Live transport fares, seats and booking are not
                claimed unless a verified data provider is connected.
                """
            )

    gr.Markdown(
        """
        ---
        **AI-Powered Smart Travel Agent – India**

        Academic Major Project | CSE-AIML
        """
    )


# -------------------------------
# 5. APPLICATION START
# -------------------------------

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=PORT
    )
