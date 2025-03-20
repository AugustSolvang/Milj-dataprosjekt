from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import date
from pandasql import sqldf

load_dotenv()

def fetch_data(Api_Key, Url, Sources, Elements):
    Start_Year = 1900
    End_Year = date.today().year
    data_list = []

    # Henter data for hvert år
    for year in range(Start_Year, End_Year + 1):
        Start_Date = f"{year}-01-01"
        End_Date = f"{year}-12-31"
        Reference_Time = f"{Start_Date}/{End_Date}"
        Endpoint = f"{Url}?sources={Sources}&elements={Elements}&referencetime={Reference_Time}"

        print(f"Henter data for {year}...", flush=True)  # Utskrift mens vi henter data

        res = requests.get(Endpoint, auth=(Api_Key, ""))
        
        if res.status_code == 200:
            data = res.json()
            
            # List comprehension for effektiv datainnsamling og fjerning av nullverdier
            for obs in data.get("data", []):
                Date = obs["referenceTime"][:10]
                Value = obs["observations"][0].get("value", None)
                
                if Value is not None:
                    data_list.append([Date, Value])
                    print(f"Data for {Date}: {Value}°C", flush=True)  # Print data for hver dag
        else:
            print(f"Feil ved henting av data for {year}: {res.status_code}", flush=True)

    print("Datahenting fullført, behandler data...", flush=True)

    # Konverter til Pandas DataFrame
    df = pd.DataFrame(data_list, columns=["Date", "Temp[°C]"])

    # Rense og behandle data
    df = clean_temperature_data(df)

    return df


def clean_temperature_data(df):
    """Renser data: håndterer nullverdier, fjerner duplikater, og bruker Pandas SQL"""
    
    df["Date"] = pd.to_datetime(df["Date"])  # Konverterer dato til datetime-format

    # Fjerner eventuelle duplikater og grupperer på dato (tar gjennomsnitt)
    print("Fjerner duplikater og grupperer data...", flush=True)
    df = df.groupby("Date", as_index=False).mean()

    # Pandas SQL - Fjerner urealistiske temperaturer
    print("Filtrerer urealistiske temperaturer...", flush=True)
    query = "SELECT * FROM df WHERE `Temp[°C]` > -50 AND `Temp[°C]` < 50"
    df = sqldf(query, locals())

    return df


Api_Key = os.getenv("API_Key_MET")
Url = os.getenv("Base_MET_URL")
Sources = "SN18700"
Elements = "air_temperature"


if __name__ == "__main__":
    df = fetch_data(Api_Key, Url, Sources, Elements)
    print("Ferdig med databehandling!")
    print(df.head())
