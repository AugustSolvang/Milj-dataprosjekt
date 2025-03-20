import requests
import datetime
import pandas as pd

API_KEY = "f6ece757-0cb9-40c7-87cf-7817a5e6bb70"
BASE_URL = "https://frost.met.no/observations/v0.jsonld"
STATION = "SN18700"  # Endre til ønsket værstasjon
ELEMENT = "air_temperature"

def fetch_temperature_data():
    """Henter daglig temperatur fra Frost API i mindre intervaller og returnerer en Pandas DataFrame."""
    start_year = 1950  # Juster etter behov
    end_year = datetime.date.today().year
    data_list = []
    
    for year in range(start_year, end_year + 1):
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        date_range = f"{start_date}/{end_date}"
        url = f"{BASE_URL}?sources={STATION}&elements={ELEMENT}&referencetime={date_range}"
        
        response = requests.get(url, auth=(API_KEY, ""))
        if response.status_code == 200:
            data = response.json()
            for obs in data.get("data", []):
                date = obs["referenceTime"][:10]
                temp = obs["observations"][0]["value"]
                data_list.append([date, temp])
        else:
            print(f"Feil ved henting av data for {year}: {response.text}")
    
    df = pd.DataFrame(data_list, columns=["Dato", "Temperatur (°C)"])
    return df

if __name__ == "__main__":
    df = fetch_temperature_data()
    print(df)


