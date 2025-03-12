import requests
import os
from dotenv import load_dotenv

# Laster miljøvariabler fra .env
load_dotenv()

API_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
HEADERS = {"User-Agent": "miljodata-prosjekt"}

def fetch_weather_data(lat, lon):
    """Henter værdata fra MET API basert på breddegrad/lengdegrad"""
    response = requests.get(f"{API_URL}?lat={lat}&lon={lon}", headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()  # Returnerer JSON-data
    else:
        print(f"Feil: {response.status_code}")
        return None

# Testkall
if __name__ == "__main__":
    data = fetch_weather_data(59.91, 10.75)  # Oslo koordinater
    print(data)
