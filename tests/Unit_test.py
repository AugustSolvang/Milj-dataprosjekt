import unittest
import pandas as pd
import numpy as np
import os
from Data_Process import Data_Process
from Data_Plot import Data_Plot
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Data files are found relative to this file, so the tests can be run from any folder
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


class TestDataProcess(unittest.TestCase):
    # Tests if files are in proper condition to be tested
    def setUp(self):
        self.valid_csv_file = os.path.join(DATA_DIR, "Air_Quality.csv")
        self.valid_json_file = os.path.join(DATA_DIR, "Air_Temp_Anomaly_1961-1990.json")
        self.invalid_file = "invalid.txt"

        self.df = pd.DataFrame({
            "Year": [2020, 2021, 2022],
            "Value": [100, 150, 200]
        })


# Below this line are unit tests for data proessing presented

# Tests if a valid JSON-file returns a non-empty DataFrame with correct columnname
    def test_valid_json_sreturns_dataframe(self):
        filename = self.valid_json_file
        df = Data_Process.DataDict(filename)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("Date", df.columns)
        self.assertIn("Value", df.columns)

# Tests if negative values are kept, since the JSON data are anomalies from the 1961-1990 normal
    def test_valid_json_keeps_negative_values(self):
        df = Data_Process.DataDict(self.valid_json_file)
        self.assertTrue((df["Value"] < 0).any())

# Tests if a valid JSON-file returns a non-empty DataFrame with columnname including coverage
    def test_valid_csv_returns_dataframe(self):
        filename = self.valid_csv_file
        df = Data_Process.DataDict(filename)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("Date", df.columns)
        self.assertIn("Value", df.columns)
        self.assertIn("Coverage", df.columns)

# Tests if AnalyzeDataWithSQL returns correct structured columns
    def test_analyze_data_with_valid_df(self):
        df = pd.DataFrame({
            "Date": pd.to_datetime(["2021-01-01", "2021-06-01", "2022-01-01"]),
            "Value": [10, 20, 30]
        })
        result = Data_Process.AnalyzeDataWithSQL(df)
        self.assertFalse(result.empty)
        self.assertIn("AvgValue", result.columns)
        self.assertIn("MinValue", result.columns)
        self.assertIn("MaxValue", result.columns)
        self.assertIn("MedianValue", result.columns)

# Tests if a non-valid filtype returns an empty DataFrame
    def test_invalid_filetype_returns_empty_dataframe(self):
        filename = self.invalid_file
        df = Data_Process.DataDict(filename)
        self.assertTrue(df.empty)

# Tests if AnalyzeDataWithSQL returns an empty DataFrame if no data was introduced
    def test_empty_dataframe_analysis_returns_empty(self):
        df = pd.DataFrame()
        result = Data_Process.AnalyzeDataWithSQL(df)
        self.assertTrue(result.empty)

# Tests if a JSON-file with wrong structure returns an empty DataFrame
    def test_json_missing_data_structure_returns_empty(self):
        broken_json_path = "broken.json"
        with open(broken_json_path, "w") as f:
            f.write('{"wrongkey": []}')  # intentionally broken
        df = Data_Process.DataDict(broken_json_path)
        self.assertTrue(df.empty)
        os.remove(broken_json_path)

# Tests if a csv-file with invalid data gets correctly handled and cleaned
    def test_csv_with_invalid_data_returns_cleaned(self):
        broken_csv_path = "broken.csv"
        with open(broken_csv_path, "w") as f:
            f.write("Dato;Verdi;Dekning\n01.01.2021 12:00;abc;")
        df = Data_Process.DataDict(broken_csv_path)
        self.assertTrue(df.empty or df["Value"].isnull().all())
        os.remove(broken_csv_path)


# Below this line are unit tests for linear regression presented

# Tests if linear regression works correctly with numeric x-data
    def test_linear_regression_with_numeric_x(self):
        df = pd.DataFrame({
            "x": np.arange(20),
            "y": np.arange(20) * 2 + 1
        })
        x_pred, y_pred, model, is_date = Data_Process.Linear_Regression(
            df, "x", "y", future_steps=5, n_points=15)
        self.assertEqual(len(x_pred), 15)
        self.assertEqual(len(y_pred), 15)
        self.assertIsInstance(model, LinearRegression)
        self.assertAlmostEqual(model.coef_[0], 2, places=1)
        self.assertAlmostEqual(model.intercept_, 1, places=1)
        self.assertAlmostEqual(y_pred[0], 1, places=1)
        self.assertFalse(is_date)

        plt.figure()
        plt.scatter(df["x"], df["y"], label="Original data")
        plt.plot(x_pred, y_pred, color="red", label="Prediction")
        plt.title("Linear Regression with Numeric x")
        plt.legend()
        plt.grid(True)
        plt.show()

# Tests linear regression with date as x-axis and checks if output is timestamps
    def test_linear_regression_with_date_x(self):
        df = pd.DataFrame({
            "date": pd.date_range("2023-01-01", periods=10),
            "y": np.arange(10) * 3 + 5
        })
        x_pred, y_pred, model, is_date = Data_Process.Linear_Regression(
            df, "date", "y", future_steps=10, n_points=20)
        self.assertEqual(len(x_pred), 20)
        self.assertEqual(len(y_pred), 20)
        self.assertIsInstance(model, LinearRegression)
        self.assertTrue(all(isinstance(x, pd.Timestamp) for x in x_pred))
        self.assertTrue(is_date)

        plt.figure()
        plt.scatter(df["date"], df["y"], label="Original data")
        plt.plot(x_pred, y_pred, color="red", label="Prediction")
        plt.title("Linear Regression with Date x")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

# Tests if regression gives error if x-column is not found in DataFrame
    def test_linear_regression_missing_x_column(self):
        df = pd.DataFrame({
            "a": [1, 2, 3],
            "y": [4, 5, 6]
        })
        with self.assertRaises(KeyError):
            Data_Process.Linear_Regression(df, "x", "y")

# Tests if regression gives error if y-column is not found in DataFame
    def test_linear_regression_missing_y_column(self):
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "b": [4, 5, 6]
        })
        with self.assertRaises(KeyError):
            Data_Process.Linear_Regression(df, "x", "y")

# Tests if regression gives error if y-values are non-numeric
    def test_linear_regression_non_numeric_y(self):
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": ["a", "b", "c"]
        })
        with self.assertRaises(ValueError):
            Data_Process.Linear_Regression(df, "x", "y")


# Below this line are unit tests for plotting presented

class TestDataPlot(unittest.TestCase):

    # Produces numeric and categorical testdata
    def setUp(self):
        self.df_numeric = pd.DataFrame({
            "x": np.arange(10),
            "y": np.arange(10) * 2 + 1
        })

        self.df_categorical = pd.DataFrame({
            "category": ["A", "B", "C", "A", "B", "C"],
            "value": [5, 7, 6, 8, 9, 5]
        })

    # Tests if a lineplot is drawn without errors
    def test_plot_lineplot(self):
        Data_Plot.plot_lineplot(self.df_numeric, "x", "y", "Test Line Plot")

    # Tests if a scatterplot is drawn without errors
    def test_plot_scatterplot(self):
        Data_Plot.plot_scatterplot(self.df_numeric, "x", "y", "Test Scatter Plot")

    # Tests if a barplot is drawn without errors from categorical data
    def test_plot_barplot(self):
        Data_Plot.plot_barplot(self.df_categorical, "category", "value", "Test Bar Plot")


if __name__ == "__main__":
    unittest.main()
