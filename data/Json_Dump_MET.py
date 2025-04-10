from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import date
import json

def fetch_data(Filename, Api_Key, Url, Sources, Elements, Reference_Time):
    Endpoint = f"{Url}?sources={Sources}&elements={Elements}&referencetime={Reference_Time}"
    res = requests.get(Endpoint, auth = (Api_Key, ""))

    if res.status_code == 200:
        data = res.json()
        with open(Filename, "a") as f:
            json.dump(data, f, indent = 4)
        print(Endpoint)
    else:
        print("Feil")
        print(res.status_code)

load_dotenv()

Filename = "Precipitation_Sum_Anomaly_1961-1990.json"
Api_Key = os.getenv("API_Key_MET")
Url = os.getenv("Base_MET_URL")
Sources = "SN18700"
Elements = "best_estimate_sum(precipitation_amount_anomaly P1M 1961_1990)"
Reference_Time = "1940-01-01/2025-01-01"

fetch_data(Filename, Api_Key, Url, Sources, Elements, Reference_Time)
