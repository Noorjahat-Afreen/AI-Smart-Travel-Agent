
import requests

from config import REQUEST_TIMEOUT, USER_AGENT


WIKIPEDIA_API = (
    "https://en.wikipedia.org/w/api.php"
)


def get_destination_overview(destination):

    if not destination or not destination.strip():
        return {
            "error": "Destination name is required."
        }

    headers = {
        "User-Agent": USER_AGENT
    }

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "redirects": 1,
        "titles": destination.strip()
    }

    try:
        response = requests.get(
            WIKIPEDIA_API,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():

            if page.get("missing") is not None:
                continue

            title = page.get("title")
            extract = page.get("extract", "")

            if not extract:
                continue

            return {
                "title": title,
                "overview": extract,
                "source": "Wikipedia",
                "url": (
                    "https://en.wikipedia.org/wiki/"
                    + title.replace(" ", "_")
                )
            }

        return {
            "error": "Destination information not found.",
            "source": "Wikipedia"
        }

    except requests.RequestException as error:
        return {
            "error": "Wikipedia service unavailable.",
            "details": str(error)
        }

    except (ValueError, TypeError):
        return {
            "error": "Unable to process Wikipedia response."
        }
