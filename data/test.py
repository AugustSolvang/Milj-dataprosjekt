import requests
from requests.auth import HTTPBasicAuth  

api_key = "2e53c5fc-1cab-435f-bf3d-5b1cd9352d86"
url = "https://frost.met.no/api/v1/sources"

params = {
    "types": "SensorSystem",
    "geometry": "nearest(10,59.91,10.75)"
}

# Bruk Basic Auth (API-nøkkel som brukernavn, tomt passord)
response = requests.get(url, auth=HTTPBasicAuth(api_key, ""), params=params)

if response.status_code == 200:
    print(response.json())  # ✅ Skriver ut tilgjengelige stasjoner
else:
    print(f"Feil: {response.status_code}, {response.text}")
