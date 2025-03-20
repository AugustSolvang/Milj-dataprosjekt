import requests
import pandas as pd

api_key = "f6ece757-0cb9-40c7-87cf-7817a5e6bb70"
url = "https://frost.met.no/observations/v0.jsonld"

headers = {
    "Authorization": f"Bearer {api_key}"
}

params = {
    "sources": "SN18700",
    "referencetime": "2000-01-01/2017-02-01",
    "elements": "air_temperature"
}

response = requests.get(url, headers=headers, params=params, auth=(api_key, ""))

if response.status_code == 200:
    data = response.json()

    observations = []
    observations = []
    for entry in data['data']:
        for obs in entry['observations']:
            observations.append({
                'Dato': entry['referenceTime'],
                'Temperatur (°C)': obs['value']
            })

    # Konvertere til Pandas DataFrame
    df = pd.DataFrame(observations)

    # Konvertere dato til riktig format
    df['Dato'] = pd.to_datetime(df['Dato']).dt.date  # Kun dato, ikke klokkeslett

    # Beregne daglig gjennomsnittstemperatur
    df_daily = df.groupby('Dato', as_index=False)['Temperatur (°C)'].mean()

    # Vise resultatet
    print(df_daily)


else:
    print(response.status_code)
    print(response.url)

