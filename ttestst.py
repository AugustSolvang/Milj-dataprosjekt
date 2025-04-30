import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandasql import sqldf
import json
import csv
import os

class Data_Process:

    @staticmethod
    def DataFrame(Filename):
        """Convert data from CSV to a Pandas DataFrame and clean the data."""
        if Filename.endswith(".csv"):
            try:
                df = pd.read_csv(Filename, sep=";", encoding="utf-8", decimal=",", names=["Date", "Value", "Coverage"], na_values=[""])
                df.columns = ["Date", "Value", "Coverage"]
            except Exception as e:
                print(f"Error reading CSV: {e}")
                return pd.DataFrame()
            print("Column names set manually:", df.columns)

            df = df.dropna(subset=["Value", "Coverage"], how = "all")

            # Konverter dato og verdi til riktige typer
            df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y %H:%M", errors='coerce', dayfirst=True)
            df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

            # Fjern rader som ikke kunne konverteres
            df = df.dropna(subset=["Date", "Value"])

            # Fjern eventuelle negative verdier (om ønskelig)
            df = df[df["Value"] >= 0]

            # For debugging – viser korrekt matchet kolonne
            print("Cleaned data:", df.head())

            return df

        else:
            print("Not a CSV-file.")
            return pd.DataFrame()

    @staticmethod
    def AnalyzeDataWithSQL(df):
        """Analyze data using SQL (sqldf) on DataFrame."""
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
    def PlotData(df):
        """Plots the average of the data per year with moving average."""
        result_df = Data_Process.AnalyzeDataWithSQL(df)
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
    filename = "Test_Data.csv"
    df = Data_Process.DataFrame(filename)
    print(df)

    if not df.empty:
        dp = Data_Process()
        result = dp.AnalyzeDataWithSQL(df)
        print(result)
        Data_Process.PlotData(df)
    else:
        print("No data available") 
