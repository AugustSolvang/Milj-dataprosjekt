from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandasql import sqldf
import json
import csv


class Data_Process:

    @staticmethod
    def DataDict(Filename):
        """Read JSON or CSV file and return a cleaned DataFrame."""
        if Filename.endswith(".json"):
            data_list = []
            with open(Filename, "r") as readfile:
                data = json.load(readfile)
                for observation in data.get("data", []):
                    date = observation["referenceTime"][:10]
                    value = observation["observations"][0].get("value", None)
                    if value is not None:
                        data_list.append((date, value))

            df = pd.DataFrame(data_list, columns=["Date", "Value"])
            df["Date"] = pd.to_datetime(df["Date"])
            df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
            df = df.dropna(subset=["Date", "Value"])
            df = df[df["Value"] >= 0]
            return df

        elif Filename.endswith(".csv"):
            try:
                df = pd.read_csv(
                    Filename,
                    sep=";",
                    encoding="utf-8",
                    decimal=",",
                    names=["Date", "Value", "Coverage"],
                    na_values=[""],
                )
                df.columns = ["Date", "Value", "Coverage"]
            except Exception as e:
                print(f"Error reading CSV: {e}")
                return pd.DataFrame()

            print("Column name set manually:", df.columns)
            df = df.dropna(subset=["Value", "Coverage"], how="all")
            df["Date"] = pd.to_datetime(
                df["Date"],
                format="%d.%m.%Y %H:%M",
                errors='coerce',
                dayfirst=True
            )
            df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
            df = df.dropna(subset=["Date", "Value"])
            df = df[df["Value"] >= 0]
            print("Cleaned data:", df.head())
            return df

        else:
            print("Not a supported file format.")
            return pd.DataFrame()

    @staticmethod
    def DataFrame(Filename):
        """Return cleaned DataFrame from JSON or CSV file."""
        df = Data_Process.DataDict(Filename)
        return df

    @staticmethod
    def AnalyzeDataWithSQL(df):
        """Analyze data using SQL (sqldf) on DataFrame."""
        if df.empty:
            print("No dataframe to be found")
            return pd.DataFrame()

        query = """
        SELECT strftime('%Y', Date) as Year, 
        AVG(Value) as AvgValue,
        MIN(Value) as MinValue,
        MAX(Value) as MaxValue
        FROM df
        GROUP BY Year
        ORDER BY Year
        """
        result = sqldf(query, locals())

        df["Year"] = df["Date"].dt.year
        median_df = df.groupby("Year")["Value"].median().reset_index(name="MedianValue")

        result["Year"] = result["Year"].astype(int)
        median_df["Year"] = median_df["Year"].astype(int)

        full_result = pd.merge(result, median_df, on="Year")
        return full_result

    @staticmethod
    def Linear_Regression(df, x_col, y_col, future_steps=0, n_points=100):
        """Apply linear regression on data and predict future values."""
        df = df.copy()

        if pd.api.types.is_datetime64_any_dtype(df[x_col]):
            df["x_num"] = df[x_col].map(pd.Timestamp.toordinal)
            is_date = True
        else:
            df["x_num"] = pd.to_numeric(df[x_col], errors='coerce')
            is_date = False

        df = df.dropna(subset=["x_num", y_col])

        X = df[["x_num"]]
        y = df[y_col]
        model = LinearRegression()
        model.fit(X, y)

        x_min = df["x_num"].min()
        x_max = df["x_num"].max() + future_steps
        x_pred_num = np.linspace(x_min, x_max, n_points).reshape(-1, 1)
        y_pred = model.predict(x_pred_num)

        if is_date:
            x_pred = [pd.to_datetime(pd.Timestamp.fromordinal(int(x))) for x in x_pred_num.flatten()]
        else:
            x_pred = x_pred_num.flatten()

        return x_pred, y_pred, model, is_date

    @staticmethod
    def Plot_Regression(df, x_col, y_col, x_pred, y_pred, is_date=False):
        """
        Plot data points and linear regression line.

        Parameters:
        - df: original dataframe with data points
        - x_col: name of x column in df
        - y_col: name of y column in df
        - x_pred: predicted x values from Linear_Regression
        - y_pred: predicted y values from Linear_Regression
        - is_date: bool, whether x values are dates
        """
        plt.figure(figsize=(10, 6))

        # Plot original data points
        plt.scatter(df[x_col], df[y_col], color='blue', label='Data points')

        # Plot regression line
        plt.plot(x_pred, y_pred, color='red', label='Linear regression')

        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'Linear Regression of {y_col} vs {x_col}')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def PlotData(df):
        """Plots the average of the data per year using a moving average."""
        result_df = Data_Process.AnalyzeDataWithSQL(df)
        if result_df.empty:
            print("No data to plot.")
            return

        result_df['Smoothed'] = result_df['AvgValue'].rolling(window=2).mean()

        plt.figure(figsize=(10, 6))
        plt.plot(result_df["Year"], result_df["AvgValue"], marker='o', label="Avg Value per Year")
        plt.plot(result_df["Year"], result_df["Smoothed"], color="red", label="Smoothed (Moving Avg)")
        plt.xlabel("Year")
        plt.ylabel("Avg Value")
        plt.title("Smoothed Average Value per Year with Moving Average")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    filename = "Test_Data.csv"  # Choose between JSON/CSV
    df = Data_Process.DataFrame(filename)
    print(df)

    if not df.empty:
        dp = Data_Process()
        result = dp.AnalyzeDataWithSQL(df)
        print(result)

        Data_Process.PlotData(df)

        # Example of using regression and plotting:
        x_pred, y_pred, model, is_date = Data_Process.Linear_Regression(
            df,
            'Date',
            'Value',
            future_steps=3650,
            n_points=100
        )
        Data_Process.Plot_Regression(df, 'Date', 'Value', x_pred, y_pred, is_date)
    else:
        print("No data available")
