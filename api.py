import requests
import json

BASE_URL = "https://api.usaspending.gov/api/v2/spending/"
FY = "2025"
QUARTER = "2"

# Step 1: Get top-level agency spending
agency_payload = {
    "type": "agency",
    "filters": {
        "fy": FY,
        "quarter": QUARTER
    }
}

agency_response = requests.post(BASE_URL, json=agency_payload)
agency_data = agency_response.json()

results = []

# Step 2: For each agency, get breakdown by program activity
for agency in agency_data.get("results", []):
    agency_id = agency.get("id")
    agency_name = agency.get("name")

    # Skip if agency_id is missing
    if agency_id is None:
        continue

    program_activity_payload = {
        "type": "program_activity",
        "filters": {
            "fy": FY,
            "quarter": QUARTER,
            "agency": int(agency_id)
        }
    }

    pa_response = requests.post(BASE_URL, json=program_activity_payload)
    if pa_response.status_code == 200:
        pa_data = pa_response.json()
        for item in pa_data.get("results", []):
            results.append({
                "agency": agency_name,
                "program": item["name"],
                "amount": item["amount"]
            })

# Print first 10 results
for r in results:
    print(f"{r['agency']} → {r['program']} → ${r['amount']:,.2f}")

with open("spending_data.json", "w") as f:
    json.dump(results, f, indent=2)