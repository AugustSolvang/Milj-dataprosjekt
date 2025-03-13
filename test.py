import requests

def get_oslo_info():
    url = "https://api.met.no/weatherapi/nowcast/2.0/complete?lat=59.9333&lon=10.7166"
    headers = {
        "User-Agent": "MyWeatherApp/1.0 (your_email@example.com)"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        oslo_data = response.json()
        print(oslo_data)  # Skriv ut hele JSON-dataen
        return oslo_data
    else:
        print(f"Feil ved henting av data: {response.status_code} - {response.text}")
        return None

# Kall funksjonen for å teste
get_oslo_info()
