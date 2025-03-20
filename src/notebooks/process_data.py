from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import date

load_dotenv()

def fetch_data(Api_Key, Url, Sources, Elements):
    Start_Year = 1900
    End_Year = date.today().year

    for year in range(Start_Year, End_Year + 1):
        data_list = []
        Added_Dates = set()

        Start_Date = f"{year}-01-01"
        End_Date = f"{year}-12-31"
        Reference_Time = f"{Start_Date}/{End_Date}"
        Endpoint = f"{Url}?sources={Sources}&elements={Elements}&referencetime={Reference_Time}"
        res = requests.get(Endpoint, auth = (Api_Key, ""))
        
        if res.status_code == 200:
            data = res.json()
            for observation in data.get("data", []):
                Date = observation["referenceTime"][:10]
                if Date not in Added_Dates:
                    Value = observation["observations"][0]["value"]
                    data_list.append([Date, Value])
                    Added_Dates.add(Date)
        else:
            print("Error. Statuscode er ikke lik 200")
            print(res.status_code)
        
        df = pd.DataFrame(data_list, columns = ["Date", "Temp[°C]"])
        print(df)


Api_Key = os.getenv("API_Key_MET")
Url = os.getenv("Base_MET_URL")
Sources = "SN18700"
Elements = "air_temperature"


if __name__ == "__main__":
    df = fetch_data(Api_Key, Url, Sources, Elements)
    print(df)


# Databehandling
