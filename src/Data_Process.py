from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from pandasql import sqldf
import json
import csv


class Data_Process:

    # The DataDict function takes in either a json or csv file and cleans each file respectively 
    @staticmethod
    def DataDict(Filename):
        """Read JSON or CSV file and return a cleaned DataFrame."""
        
        # This part handles the json file
        if Filename.endswith(".json"):
            data_list = []

            with open(Filename, "r") as readfile:
                data = json.load(readfile)
                for observation in data.get("data", []):
                    # Extract date and value from file
                    date = observation["referenceTime"][:10]
                    value = observation["observations"][0].get("value", None)
                    if value is not None:
                        data_list.append((date, value))

            # Create DataFrame and clean
            df = pd.DataFrame(data_list, columns=["Date", "Value"])
            df["Date"] = pd.to_datetime(df["Date"])  # Convert to datetime
            df["Value"] = pd.to_numeric(df["Value"], errors="coerce")  # Ensure numeric values
            df = df.dropna(subset=["Date", "Value"])  # Drop rows with missing values
            df = df[df["Value"] >= 0]  # Keep only non-negative values
            return df

        # This part handles the csv file
        elif Filename.endswith(".csv"):
            try:
                # Reads the csv file
                df = pd.read_csv(
                    Filename,
                    sep=";",
                    encoding="utf-8",
                    decimal=",",
                    names=["Date", "Value", "Coverage"],
                    na_values=[""],
                )
                df.columns = ["Date", "Value", "Coverage"]  # Set column names
            except Exception as e:
                print(f"Error reading CSV: {e}")
                return pd.DataFrame()

            print("Column name set manually:", df.columns)

            # Drop rows with missing Value and Coverage
            df = df.dropna(subset=["Value", "Coverage"], how="all")

            # Convert columns to proper types
            df["Date"] = pd.to_datetime(
                df["Date"],
                format="%d.%m.%Y %H:%M",
                errors="coerce",
                dayfirst=True
            )
            df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

            # Final cleanup
            df = df.dropna(subset=["Date", "Value"])
            df = df[df["Value"] >= 0]
            print("Cleaned data:", df.head())
            return df

        # Returns empty dataframe if invalid file format
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

    # SQL query to calculate annual statistics
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

    # Add median calculation separately using Pandas
    df["Year"] = df["Date"].dt.year
    median_df = df.groupby("Year")["Value"].median().reset_index(
        name="MedianValue"
    )

    # Ensure consistent data types before merge
    result["Year"] = result["Year"].astype(int)
    median_df["Year"] = median_df["Year"].astype(int)

    # Merge SQL results with median values
    full_result = pd.merge(result, median_df, on="Year")

    return full_result


@staticmethod
def Linear_Regression(df, x_col, y_col, future_steps=0, n_points=100):
    """Apply linear regression on data and predict future values."""
    
    df = df.copy()

    # Convert datetime to ordinal if needed or to numeric value
    if pd.api.types.is_datetime64_any_dtype(df[x_col]):
        df["x_num"] = df[x_col].map(pd.Timestamp.toordinal)
        is_date = True
    else:
        df["x_num"] = pd.to_numeric(df[x_col], errors='coerce')
        is_date = False

    # Drop rows with missing values in x or y
    df = df.dropna(subset=["x_num", y_col])

    # Train linear regression model
    X = df[["x_num"]] # Define the x-coordinates
    y = df[y_col] # Define the y-coordinates
    model = LinearRegression()
    model.fit(X, y) 

    # Create prediction range from existing min to future max
    x_min = df["x_num"].min() # Defines the min x-values
    x_max = df["x_num"].max() + future_steps # Defines the max x-values
    x_pred_num = np.linspace(x_min, x_max, n_points).reshape(-1, 1) # Makes new x-values for the prediction
    y_pred = model.predict(x_pred_num) # Predicts the y-values 

    # Convert predicted x back to datetime if original was dates
    if is_date:
        x_pred = [
            pd.to_datetime(pd.Timestamp.fromordinal(int(x)))
            for x in x_pred_num.flatten()
        ]
    else:
        x_pred = x_pred_num.flatten()

    return x_pred, y_pred, model, is_date
