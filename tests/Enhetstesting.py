import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from process_data import fetch_data  # Importer fetch_data fra process_data.py

class TestFetchData(unittest.TestCase):

    @patch("process_data.requests.get")  # Patcher riktig sted
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

    @patch("process_data.requests.get")  # Patcher riktig sted
    def test_fetch_data_api_failure(self, mock_get):
        """Tester at fetch_data håndterer API-feil (f.eks. 500-serverfeil)."""

        # Simuler en feilmelding fra API
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        df = fetch_data("fake_api_key", "fake_url", "SN18700", "air_temperature")

        # Skal returnere None eller en tom DataFrame
        self.assertIsNone(df)

    @patch("process_data.requests.get")  # Patcher riktig sted
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

