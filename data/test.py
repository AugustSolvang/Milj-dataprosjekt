import requests
import json

api_key = "2e53c5fc-1cab-435f-bf3d-5b1cd9352d86"
url_base = "https://frost.met.no/api/v0/"
url_endpoint = "timeseries"  # Riktig endepunkt for værdata
url = f"{url_base}{url_endpoint}"

headers = {
    "Authorization": f"Bearer {api_key}"
}

params = {
    "station": "Oslo",  # Sjekk at stasjonen er riktig
    "start_date": "2020-01-01",
    "end_date": "2020-12-31"
}

response = requests.get(url, headers=headers, params=params)

print(f"Status Code: {response.status_code}")  # Sjekk statuskoden
if response.status_code == 200:
    try:
        data = response.json()
        with open('Weather_Data_MET.json', 'a') as json_file:
            json.dump(data, json_file, indent=4)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
else:
    print(f"Error: {response.status_code}")
    print(f"Response: {response.text}")  # Skriver ut feilmeldingen fra serveren



