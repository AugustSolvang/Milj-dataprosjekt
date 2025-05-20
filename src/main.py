import pandas as pd
from Data_Process import Data_Process

data = pd.read_csv("data/Air_Quality.csv")

df = Data_Process.DataFrame(data)
print("DataFrame:\n", df)

if not df.empty:
    result_df = Data_Process.AnalyzeDataWithSQL(df)
    print("Avg/Min/Max Values (SQL):\n", result_df)


if not df.empty:
    Data_Process.PlotData(df)


if __name__ == "__main__":
    filename = "rotte.json" #Choose between JSON/CSV
    df = Data_Process.DataFrame(filename)
    print(df)

    if not df.empty:
        dp = Data_Process()
        result = dp.AnalyzeDataWithSQL(df)
        print(result)

        Data_Process.PlotData(df)
    else:
        print("No data available")