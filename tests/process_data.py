from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import date
import unittest
from unittest.mock import patch, MagicMock


load_dotenv()

def fetch_data(Api_Key, Url, Sources, Elements):
    Start_Year = 1900
    End_Year = date.today().year

    for year in range(Start_Year, End_Year + 1):
        data_dict = {}

        Start_Date = f"{year}-01-01"
        End_Date = f"{year}-12-31"
        Reference_Time = f"{Start_Date}/{End_Date}"
        Endpoint = f"{Url}?sources={Sources}&elements={Elements}&referencetime={Reference_Time}"
        res = requests.get(Endpoint, auth = (Api_Key, ""))
        
        if res.status_code == 200:
            data = res.json()
            for observation in data.get("data", []):
                Date = observation["referenceTime"][:10]
                Value = observation["observations"][0]["value"]

                if Date not in data_dict:
                    data_dict[Date] = []
                data_dict[Date].append(Value)
                    
    
        else:
            print("Error. Statuscode er ikke lik 200")
            print(res.status_code)
        
        data_list = [[Date, sum(Values)/len(Values)] for Date, Values in data_dict.items()]

        df = pd.DataFrame(data_list, columns = ["Date", "Temp[°C]"])
        print(df)

Api_Key = os.getenv("API_Key_MET")
Url = os.getenv("Base_MET_URL")
Sources = "SN18700"
Elements = "air_temperature"

if __name__ == "__main__":
    df = fetch_data(Api_Key, Url, Sources, Elements)
    print(df)

#Databehandling

class TestFetchData(unittest.TestCase):

    @patch("your_script_name.requests.get")
    def test_fetch_data_success(self, mock_get):
        """Tester at fetch_data håndterer en suksessfull API-respons korrekt."""

        # Simulert API-respons (mock)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"referenceTime": "2023-01-01T00:00:00Z", "observations": [{"value": 5.0}]},
                {"referenceTime": "2023-01-01T12:00:00Z", "observations": [{"value": 7.0}]},
                {"referenceTime": "2023-01-02T00:00:00Z", "observations": [{"value": 3.0}]},
            ]
        }
        mock_get.return_value = mock_response

        df = fetch_data("fake_api_key", "fake_url", "SN18700", "air_temperature")

        # Sjekk at DataFrame har riktig struktur
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (2, 2))  # To datoer, to kolonner

        # Sjekk verdiene
        self.assertAlmostEqual(df.iloc[0]["Temp[°C]"], 6.0)  # (5+7)/2 = 6.0
        self.assertAlmostEqual(df.iloc[1]["Temp[°C]"], 3.0)  # 3.0 alene

    @patch("your_script_name.requests.get")
    def test_fetch_data_api_failure(self, mock_get):
        """Tester at fetch_data håndterer API-feil (f.eks. 500-serverfeil)."""

        # Simuler en feilmelding fra API
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        df = fetch_data("fake_api_key", "fake_url", "SN18700", "air_temperature")

        # Skal returnere None eller en tom DataFrame
        self.assertIsNone(df)

    @patch("your_script_name.requests.get")
    def test_fetch_data_empty_response(self, mock_get):
        """Tester at fetch_data håndterer en tom respons korrekt."""

        # Simuler API-respons uten data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response

        df = fetch_data("fake_api_key", "fake_url", "SN18700", "air_temperature")

        # Skal returnere en tom DataFrame
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

if __name__ == "__main__":
    unittest.main()

