import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
from pandasql import sqldf

class Data_Process:

    @staticmethod
    def DataDict(Filename):
        """Les JSON-fil og returner en ordbok med data organisert per dato."""
        if Filename.endswith(".json"):
            with open(Filename, "r") as readfile:
                data = json.load(readfile)
                DataDict = {}

                for observation in data.get("data", []):
                    Date = observation["referenceTime"][:10]
                    Value = observation["observations"][0]["value"]

                    if Date not in DataDict:
                        DataDict[Date] = []
                    DataDict[Date].append(Value)
                
                return DataDict
        else:
            print("Ikke en json fil")

    @staticmethod
    def DataFrame(Filename):
        """Konverter data fra JSON til en Pandas DataFrame og rens dataene."""
        DataDict = Data_Process.DataDict(Filename)
        
        if not DataDict:
            return pd.DataFrame()  # Returnerer en tom DataFrame hvis ingen data
        
        # Omforme DataDict til en liste av tuples for konvertering til DataFrame
        data_list = [(date, value) for date, values in DataDict.items() for value in values]

        # Konvertere til Pandas DataFrame
        df = pd.DataFrame(data_list, columns=["Date", "Value"])

        # Konvertere 'Date' kolonnen til datetime format for enklere manipulering
        df["Date"] = pd.to_datetime(df["Date"])

        # Rense data: Håndtere manglende verdier (for eksempel hvis noen verdier er None)
        df = df.dropna(subset=["Value"])  # Fjerne rader med manglende 'Value'
        
        # (Valgfritt) Fylle eventuelle NaN verdier med gjennomsnittet for 'Value'
        # df["Value"].fillna(df["Value"].mean(), inplace=True)

        # Rens uregelmessigheter: Hvis det er ulogiske verdier (f.eks. negative temperaturer)
        df = df[df["Value"] >= 0]  # Filtrer ut negative verdier

        return df

    @staticmethod
    def AnalyzeDataWithSQL(df):
        """Analyser data ved hjelp av SQL (sqldf) på DataFrame."""
        # Eksempel på SQL-spørring: Beregn gjennomsnittlig verdi per dag
        query = """
        SELECT Date, AVG(Value) as AvgValue
        FROM df
        GROUP BY Date
        ORDER BY Date
        """
        # Kjør SQL-spørringen på DataFrame
        result = sqldf(query, locals())
        return result

    @staticmethod
    def PlotData(df):
        """Plotter dataene som en tidsserie."""
        plt.figure(figsize=(10, 6))
        plt.plot(df["Date"], df["Value"], label="Value over Time")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.title("Data over Time")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Bruk av klassene
if __name__ == "__main__":
    filename = "data.json"  # Erstatt med stien til din JSON-fil

    # Les og rens data
    df = Data_Process.DataFrame(filename)

    if not df.empty:
        # Utfør analyse med SQL
        result_df = Data_Process.AnalyzeDataWithSQL(df)
        print("Gjennomsnitt per dag:\n", result_df)

        # Plot data
        Data_Process.PlotData(df)
    else:
        print("Ingen data tilgjengelig.")



