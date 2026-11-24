
class VerificationAgent:
    """
    Checks whether travel recommendations
    are supported by collected data.
    """

    REQUIRED_FIELDS = [
        "name",
        "category"
    ]

    def verify_places(self, places):

        if not isinstance(places, list):
            return {
                "verified": False,
                "message": "Invalid places data."
            }

        verified = []
        rejected = []

        for place in places:

            if not isinstance(place, dict):
                rejected.append({
                    "reason": "Invalid place record"
                })
                continue

            name = place.get("name")
            category = place.get("category")

            if not name or not category:
                rejected.append({
                    "place": name or "Unknown",
                    "reason": "Name or category missing"
                })
                continue

            verified.append({
                **place,
                "verification_status": "Present in collected data"
            })

        return {
            "verified_places": verified,
            "rejected_places": rejected,
            "total_checked": len(places),
            "total_verified": len(verified),
            "total_rejected": len(rejected)
        }

    def verify_plan_data(self, collected_data):

        if not isinstance(collected_data, dict):
            return {
                "status": "Failed",
                "message": "Invalid collected data."
            }

        results = {}

        for section, data in collected_data.items():

            if data is None or data == [] or data == {}:
                results[section] = (
                    "details unavailable in collected data"
                )
            else:
                results[section] = (
                    "Data received; source verification required"
                )

        return {
            "status": "Checked",
            "sections": results,
            "note": (
                "This agent checks data presence. "
                "It does not independently prove source accuracy."
            )
        }
