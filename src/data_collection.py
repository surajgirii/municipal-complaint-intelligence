import os
import pandas as pd
import requests


def download_nyc_311_data(limit=50000, output_path="data/raw/raw_complaints.csv"):
    """Fetches a sample of NYC 311 Service Requests data directly via the Socrata Open Data API

    and saves it locally as a CSV file.
    """
    print("⏳ Fetching NYC 311 Complaint Data from API...")

    # NYC Open Data Socrata API endpoint for 311 Service Requests
    api_url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

    # Select key analytical fields to keep the dataset lean and relevant
    select_fields = (
        "unique_key, created_date, closed_date, agency, agency_name, "
        "complaint_type, descriptor, location_type, incident_zip, "
        "incident_address, street_name, city, landmark, facility_type, "
        "status, resolution_description, resolution_action_updated_date, "
        "borough, latitude, longitude"
    )

    # API query parameters
    params = {
        "$select": select_fields,
        "$limit": limit,
        "$order": "created_date DESC",  # Fetch recent complaints
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Ensure raw folder exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save to raw CSV
        df.to_csv(output_path, index=False)
        print(f"✅ Data successfully downloaded!")
        print(f"📊 Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"📁 Saved to: {output_path}")
    else:
        print(
            f"❌ Failed to download data. HTTP Status Code: {response.status_code}"
        )


if __name__ == "__main__":
    download_nyc_311_data()