import requests
import json
from pathlib import Path

# Load API key from config.json
config_path = Path("config.json")
with config_path.open() as config_file:
    config = json.load(config_file)

api_key = config.get("VISUAL_CROSSING_API_KEY")

# List of states to retrieve weather data for
states = [
    "California", "Connecticut", "Florida", "Georgia", "Maryland",
    "Michigan", "New York", "Pennsylvania", "Texas", "Washington"
]

# Define API endpoint and base params
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Set output folder
output_folder = Path("data/weather_data_json")

output_folder.mkdir(parents=True, exist_ok=True)

# Request and save data for each state
for state in states:
    url = f"{base_url}/{state}/2021-01-01/2021-12-31"
    params = {
        "unitGroup": "us",
        "key": api_key,
        "contentType": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        file_path = output_folder / f"weather_data_{state[:2].upper()}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Saved data for {state} to {file_path}")
    else:
        print(f"Failed to retrieve data for {state}: {response.status_code}")