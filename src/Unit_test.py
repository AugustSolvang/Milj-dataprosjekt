import unittest
import pandas as pd
import os
from Data_Process import Data_Process
from dataplot import Data_Plot


class TestDataProcess(unittest.TestCase):
    def setUp(self):
        self.valid_csv_file = "Test_Data.csv"
        self.valid_json_file = "rotte.json"
        self.invalid_file = "invalid.txt"

        self.df = pd.DataFrame({
            "Year": [2020, 2021, 2022],
            "Value": [100, 150, 200]
    })


    def test_valid_json_sreturns_dataframe(self):
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

    def test_plot_lineplot_runs_without_error(self):
        # Act + Assert: Ingen exceptions
        try:
            Data_Plot.plot_lineplot(self.df, "Year", "Value", "Test Lineplot")
        except Exception as e:
            self.fail(f"plot_lineplot() raised an exception: {e}")

    def test_plot_scatterplot_runs_without_error(self):
        try:
            Data_Plot.plot_scatterplot(self.df, "Year", "Value", "Test Scatterplot")
        except Exception as e:
            self.fail(f"plot_scatterplot() raised an exception: {e}")

    def test_plot_regplot_runs_without_error(self):
        try:
            Data_Plot.plot_regplot(self.df, "Year", "Value", "Test Regplot")
        except Exception as e:
            self.fail(f"plot_regplot() raised an exception: {e}")

    def test_plot_barplot_runs_without_error(self):
        try:
            Data_Plot.plot_barplot(self.df, "Year", "Value", "Test Barplot")
        except Exception as e:
            self.fail(f"plot_barplot() raised an exception: {e}")

    def test_plot_bokeh_saves_file(self):
        # Arrange
        output_filename = "test_bokeh_plot.html"
        if os.path.exists(output_filename):
            os.remove(output_filename)

        # Act
        Data_Plot.plot_bokeh(self.df, "Year", "Value", "Test Bokeh", chart_type="line", output_filename=output_filename)

        # Assert
        self.assertTrue(os.path.exists(output_filename), "Bokeh file was not created.")

        # Cleanup
        os.remove(output_filename)

    def test_plot_bokeh_invalid_chart_type_raises_valueerror(self):
        # Act + Assert
        with self.assertRaises(ValueError) as context:
            Data_Plot.plot_bokeh(self.df, "Year", "Value", "Test Invalid", chart_type="pie")

        self.assertIn("Invalid chart_type", str(context.exception))


if __name__ == "__main__":
    unittest.main()
