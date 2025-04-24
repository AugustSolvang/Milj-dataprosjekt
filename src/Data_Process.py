import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandasql import sqldf
import json
import csv


class Data_Process:

    @staticmethod
    def DataDict(Filename):
        """Les JSON-fil eller CSV.fil og returner en ordbok med data organisert per dato."""
        DataDict = {}
        if Filename.endswith(".json"):
            with open(Filename, "r") as readfile:
                data = json.load(readfile)
                for observation in data.get("data", []):
                    Date = observation["referenceTime"][:10]
                    Value = observation["observations"][0]["value"]

                    if Date not in DataDict:
                        DataDict[Date] = []
                    DataDict[Date].append(Value)

        elif Filename.endswith(".csv"):
            with open(Filename, "r") as readfile:
                reader = csv.DictReader(readfile)
                for row in reader:
                    Date = row.get("dato")
                    if Date:
                        if Date not in DataDict:
                            DataDict[Date] = []
                        DataDict[Date].append(row)
        else:
            print("Ikke en json/csv fil")

        return DataDict

    @staticmethod
    def DataFrame(Filename):
        """Konverter data fra JSON til en Pandas DataFrame og rens dataene."""
        DataDict = Data_Process.DataDict(Filename)
        if not DataDict:
            return pd.DataFrame()
        data_list = [(date, value) for date, values in DataDict.items() for value in values]
        df = pd.DataFrame(data_list, columns=["Date", "Value"])
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.dropna(subset=["Value"])
        df = df[df["Value"] >= 0]

        return df

    @staticmethod
    def AnalyzeDataWithSQL(df):
        """Analyser data ved hjelp av SQL (sqldf) på DataFrame."""
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
        """Plotter gjennomsnittet av dataene per år med glidende gjennomsnitt."""
        # Beregn gjennomsnitt per år
        result_df = Data_Process.AnalyzeDataWithSQL(df)

        # Glidende gjennomsnitt
        result_df['Smoothed'] = result_df['AvgValue'].rolling(window=2).mean()  # Glatt ut med et vindu på 2

        # Plot gjennomsnittet per år
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
    filename = "rotte.json"  # Erstatt med stien til din JSON-fil
    # Les og rens data
    df = Data_Process.DataFrame(filename)
    print(df)
    dp = Data_Process()
    result = dp.AnalyzeDataWithSQL(df)
    print(result)
    
    if not df.empty:
        # Plot gjennomsnittet per år med glidende gjennomsnitt
        Data_Process.PlotData(df)
    else:
        print("Ingen data tilgjengelig")