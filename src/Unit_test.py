import unittest
import pandas as pd
import os
from Data_Process import Data_Process


class TestDataProcess(unittest.TestCase):

    def setUp(self):
        """Kjør før hver test"""
        self.valid_json_file = "rotte.json"
        self.valid_csv_file = "Test_Data.csv"
        self.invalid_file = "invalid_file.txt"
        self.empty_df = pd.DataFrame()

    # ----------- POSITIVE TESTER -----------

    def test_valid_json_returns_dataframe(self):
        # Arrange
        filename = self.valid_json_file

        # Act
        df = Data_Process.DataDict(filename)

        # Assert
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("Date", df.columns)
        self.assertIn("Value", df.columns)

    def test_valid_csv_returns_dataframe(self):
        # Arrange
        filename = self.valid_csv_file

        # Act
        df = Data_Process.DataDict(filename)

        # Assert
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("Date", df.columns)
        self.assertIn("Value", df.columns)
        self.assertIn("Coverage", df.columns)

    def test_analyze_data_with_valid_df(self):
        # Arrange
        df = pd.DataFrame({
            "Date": pd.to_datetime(["2021-01-01", "2021-06-01", "2022-01-01"]),
            "Value": [10, 20, 30]
        })

        # Act
        result = Data_Process.AnalyzeDataWithSQL(df)

        # Assert
        self.assertFalse(result.empty)
        self.assertIn("AvgValue", result.columns)
        self.assertIn("MinValue", result.columns)
        self.assertIn("MaxValue", result.columns)
        self.assertIn("MedianValue", result.columns)

    # ----------- NEGATIVE TESTER -----------

    def test_invalid_filetype_returns_empty_dataframe(self):
        # Arrange
        filename = self.invalid_file

        # Act
        df = Data_Process.DataDict(filename)

        # Assert
        self.assertTrue(df.empty)

    def test_empty_dataframe_analysis_returns_empty(self):
        # Arrange
        df = pd.DataFrame()

        # Act
        result = Data_Process.AnalyzeDataWithSQL(df)

        # Assert
        self.assertTrue(result.empty)

    def test_json_missing_data_structure_returns_empty(self):
        # Arrange
        broken_json_path = "broken.json"
        with open(broken_json_path, "w") as f:
            f.write('{"wrongkey": []}')  # intentionally broken

        # Act
        df = Data_Process.DataDict(broken_json_path)

        # Assert
        self.assertTrue(df.empty)

        # Cleanup
        os.remove(broken_json_path)

    def test_csv_with_invalid_data_returns_cleaned(self):
        # Arrange
        broken_csv_path = "broken.csv"
        with open(broken_csv_path, "w") as f:
            f.write("Dato;Verdi;Dekning\n01.01.2021 12:00;abc;")

        # Act
        df = Data_Process.DataDict(broken_csv_path)

        # Assert
        self.assertTrue(df.empty or df["Value"].isnull().all())

        # Cleanup
        os.remove(broken_csv_path)


if __name__ == '__main__':
    unittest.main()
