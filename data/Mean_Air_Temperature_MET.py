from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import date
import json

def fetch_data(Filename, API_Key, URL, Sources, Elements, Reference_Time):
    Endpoint = f"{URL}?sources={Sources}&elements={Elements}&referencetime={Reference_Time}"
    res = requests.get(Endpoint, auth = (API_Key, ""))

    if res.status_code == 200:
        data = res.json()
        with open(Filename, "a") as f:
            json.dump(data, f, indent = 4)
    else:
        print("Feil")
        print(res.status_code)

load_dotenv()

Filename = "Air_Temp_MET_1960-1990.json"
Api_Key = os.getenv("API_Key_MET")
Url = os.getenv("Base_MET_URL")
Sources = "SN18700"
Elements = "air_temperature"
Reference_Time = "1960-01-01/1991-01-01"

fetch_data(Filename, Api_Key, Url, Sources, Elements, Reference_Time)

Filename = "Air_Temp_MET_1991-2000.json"
Reference_Time = "1991-01-01/2001-01-01"

fetch_data(Filename, Api_Key, Url, Sources, Elements, Reference_Time)

Filename = "Air_Temp_MET_2001-2010.json"
Reference_Time = "2001-01-01/2011-01-01"

fetch_data(Filename, Api_Key, Url, Sources, Elements, Reference_Time)

Filename = "Air_Temp_MET_2011-2020.json"
Reference_Time = "2011-01-01/2021-01-01"

fetch_data(Filename, Api_Key, Url, Sources, Elements, Reference_Time)


