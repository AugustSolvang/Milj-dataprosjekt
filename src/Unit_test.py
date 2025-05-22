import unittest
import pandas as pd
import numpy as np
import os
from Data_Process import Data_Process
from Data_Plot import Data_Plot
import pytest
import sys
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import webbrowser



class TestDataProcess(unittest.TestCase):
    def setUp(self):
        self.valid_csv_file = "Air_Quality.csv"
        self.valid_json_file = "Air_Temp_Anomaly_1961-1990.json"
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
        x_pred, y_pred, model, is_date = Data_Process.Linear_Regression(df, "x", "y", future_steps=5, n_points=15)
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
        x_pred, y_pred, model, is_date = Data_Process.Linear_Regression(df, "date", "y", future_steps=10, n_points=20)
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

# Below this line are unit tests for bokeh-plotting presented

# Tests if a line-plot HTML-file is created and opened in the webbrowser 
def test_plot_bokeh_lineplot_creates_file(tmp_path):
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 20, 30]})
    output_file = tmp_path / "lineplot.html"
    Data_Plot.plot_bokeh(df, xlabel='x', ylabel='y', title='Line Plot', chart_type='line', output_filename=str(output_file))
    assert output_file.exists()
    webbrowser.open(str(output_file))


# Tests if a scatterplot HTML-file is created and opened in the webbrowser
def test_plot_bokeh_scatterplot_creates_file(tmp_path):
    df = pd.DataFrame({'x': [4, 5, 6], 'y': [15, 25, 35]})
    output_file = tmp_path / "scatterplot.html"
    Data_Plot.plot_bokeh(df, xlabel='x', ylabel='y', title='Scatter Plot', chart_type='scatter', output_filename=str(output_file))
    assert output_file.exists()
    webbrowser.open(str(output_file))


# Tests if a barplot HTML-file is created and x-values are converted to strings
def test_plot_bokeh_barplot_converts_x_to_str_and_creates_file(tmp_path):
    df = pd.DataFrame({'cat': [100, 200, 300], 'val': [1, 2, 3]})
    output_file = tmp_path / "barplot.html"
    Data_Plot.plot_bokeh(df, xlabel='cat', ylabel='val', title='Bar Plot', chart_type='bar', output_filename=str(output_file))
    assert output_file.exists()
    assert df['cat'].dtype == object  # Barplot skal konvertere til string
    webbrowser.open(str(output_file))

# Tests 
def test_plot_bokeh_invalid_chart_type_raises_valueerror():
    df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
    with pytest.raises(ValueError) as excinfo:
        Data_Plot.plot_bokeh(df, xlabel='x', ylabel='y', title='Bad Chart', chart_type='wrongtype')
    assert "Invalid chart_type" in str(excinfo.value)


def test_plot_bokeh_missing_xlabel_column_raises_valueerror():
    df = pd.DataFrame({'wrong_x': [1, 2], 'y': [3, 4]})
    with pytest.raises(ValueError) as excinfo:
        Data_Plot.plot_bokeh(df, xlabel='x', ylabel='y', title='Missing X', chart_type='line')
    assert "Missing x column" in str(excinfo.value).lower() or "missing" in str(excinfo.value).lower()


def test_plot_bokeh_missing_ylabel_column_raises_valueerror():
    df = pd.DataFrame({'x': [1, 2], 'wrong_y': [3, 4]})
    with pytest.raises(ValueError) as excinfo:
        Data_Plot.plot_bokeh(df, xlabel='x', ylabel='y', title='Missing Y', chart_type='line')
    assert "Missing y column" in str(excinfo.value).lower() or "missing" in str(excinfo.value).lower()


class TestDataPlot(unittest.TestCase):
    def setUp(self):
        # Numerisk data for line, scatter, reg
        self.df_numeric = pd.DataFrame({
            "x": np.arange(10),
            "y": np.arange(10) * 2 + 1
        })
        # Kategoriske data for barplot
        self.df_categorical = pd.DataFrame({
            "category": ["A", "B", "C", "A", "B", "C"],
            "value": [5, 7, 6, 8, 9, 5]
        })

        # Lag mappe for bokeh output
        self.output_dir = "test_outputs"
        os.makedirs(self.output_dir, exist_ok=True)

    def test_plot_lineplot(self):
        Data_Plot.plot_lineplot(self.df_numeric, "x", "y", "Test Line Plot")

    def test_plot_scatterplot(self):
        Data_Plot.plot_scatterplot(self.df_numeric, "x", "y", "Test Scatter Plot")

    def test_plot_regplot(self):
        Data_Plot.plot_regplot(self.df_numeric, "x", "y", "Test Reg Plot")

    def test_plot_barplot(self):
        Data_Plot.plot_barplot(self.df_categorical, "category", "value", "Test Bar Plot")

    def test_plot_bokeh_line(self):
        output_file = os.path.join(self.output_dir, "bokeh_line.html")
        Data_Plot.plot_bokeh(self.df_numeric, "x", "y", "Bokeh Line Plot", chart_type="line", output_filename=output_file)
        self.assertTrue(os.path.exists(output_file))
        webbrowser.open(f"file://{os.path.abspath(output_file)}")

    def test_plot_bokeh_scatter(self):
        output_file = os.path.join(self.output_dir, "bokeh_scatter.html")
        Data_Plot.plot_bokeh(self.df_numeric, "x", "y", "Bokeh Scatter Plot", chart_type="scatter", output_filename=output_file)
        self.assertTrue(os.path.exists(output_file))
        webbrowser.open(f"file://{os.path.abspath(output_file)}")

    def test_plot_bokeh_bar(self):
        output_file = os.path.join(self.output_dir, "bokeh_bar.html")
        Data_Plot.plot_bokeh(self.df_categorical, "category", "value", "Bokeh Bar Plot", chart_type="bar", output_filename=output_file)
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(self.df_categorical['category'].dtype == object or self.df_categorical['category'].dtype.name == 'category')
        webbrowser.open(f"file://{os.path.abspath(output_file)}")

    def test_plot_bokeh_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            Data_Plot.plot_bokeh(self.df_numeric, "x", "y", "Invalid Chart", chart_type="invalidtype")

    def test_plot_bokeh_missing_columns_raise(self):
        with self.assertRaises(ValueError):
            Data_Plot.plot_bokeh(self.df_numeric, "missing_x", "y", "Missing X")

        with self.assertRaises(ValueError):
            Data_Plot.plot_bokeh(self.df_numeric, "x", "missing_y", "Missing Y")


if __name__ == "__main__":
    unittest.main()
