import json
import pandas as pd
from pandasql import sqldf


def save_json(data, filename="data/weather.json"):
    """Lagrer API-data som en JSON-fil"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Data lagret i {filename}")

def save_csv(data, filename="data/weather.csv"):
    """Lagrer data som CSV-fil"""
    df = pd.DataFrame(data)  # Konverterer JSON til Pandas DataFrame
    df.to_csv(filename, index=False)
    print(f"✅ Data lagret i {filename}")

def load_data(filename="data/weather.csv"):
    """Laster inn CSV-data som Pandas DataFrame"""
    return pd.read_csv(filename)

def analyze_temperature(df):
    """Bruker SQL for å filtrere data med temperatur over 15°C"""
    query = "SELECT * FROM df WHERE temperature > 15"
    return sqldf(query, locals())

if __name__ == "__main__":
    df = load_data()
    result = analyze_temperature(df)
    print(result)

