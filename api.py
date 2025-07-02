# api.py

import requests

BASE_URL = "https://api.usaspending.gov/api/v2/spending/"
FY = "2025"
QUARTER = "2"

def fetch_spending_data():
    """Fetches spending data for all agencies and their program activities."""
    agency_payload = {
        "type": "agency",
        "filters": {
            "fy": FY,
            "quarter": QUARTER
        }
    }

    try:
        agency_response = requests.post(BASE_URL, json=agency_payload)
        agency_response.raise_for_status()
        agency_data = agency_response.json()
    except Exception as e:
        print(f"Failed to retrieve agency data: {e}")
        return []

    results = []

    for agency in agency_data.get("results", []):
        agency_id = agency.get("id")
        agency_name = agency.get("name")

        # Skip if missing required data
        if not agency_id or not agency_name:
            continue

        program_activity_payload = {
            "type": "program_activity",
            "filters": {
                "fy": FY,
                "quarter": QUARTER,
                "agency": int(agency_id)
            }
        }

        try:
            pa_response = requests.post(BASE_URL, json=program_activity_payload)
            pa_response.raise_for_status()
            pa_data = pa_response.json()

            for item in pa_data.get("results", []):
                program_name = item.get("name")
                amount = item.get("amount")

                if program_name and amount is not None:
                    results.append({
                        "agency": agency_name,
                        "program": program_name,
                        "amount": amount
                    })

        except Exception as e:
            print(f"Error retrieving programs for {agency_name}: {e}")
            continue

    return results
