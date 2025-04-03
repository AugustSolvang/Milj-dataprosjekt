from Data_Process import Data_Process

filename = "rotte.json"

df = Data_Process.DataFrame(filename)
print("DataFrame:\n", df)

if not df.empty:
    result_df = Data_Process.AnalyzeDataWithSQL(df)
    print("Avg/Min/Max Values (SQL):\n", result_df)
