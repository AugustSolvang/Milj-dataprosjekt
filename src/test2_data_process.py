# Test script (test_data_process.py)
from test_data_process import Data_Process  # Importer Data_Process-klassen fra den originale filen

# Bruk datafilen som ble laget
filename = "rotte.json"  # Sørg for at filen finnes i samme mappe som testfilen, eller gi den komplette stien

# 1. Test DataFrame-funksjonen
df = Data_Process.DataFrame(filename)
print("DataFrame:\n", df)

# 2. Test SQL-analyse
if not df.empty:
    result_df = Data_Process.AnalyzeDataWithSQL(df)
    print("Gjennomsnitt per dag (SQL-analyse):\n", result_df)

# 3. Test plotting
if not df.empty:
    Data_Process.PlotData(df)
