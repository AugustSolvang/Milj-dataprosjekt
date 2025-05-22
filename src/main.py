import pandas as pd
from Data_Process import Data_Process
from Data_Plot import Data_Plot
from Interactive_Plot import Interactive_Plot

def Main():
    Data_type = input("What data do you want to visualize? (Air quality/Air temperature/Precipitation):")
    xlabel = "Date"
    if Data_type.lower() == "air quality":
        filename = "Air_Quality.csv"
        ylabel = "NO µg/m³"
        title = "Historic air quality"
    elif Data_type.lower() == "air temperature":
        filename = "Air_Temp_Anomaly_1961-1990.json"
        ylabel = "degC"
        title = "Homogenized mean air temperature for the period 1961-1990"
    elif Data_type.lower() == "precipitation":
        filename = "Precipitation_Sum_Anomaly_1961-1990.json"
        ylabel = "percent"
        title = "Homogenized mean precipitation sum for the period 1961-1990"
    else:
        print("The wrong data type was written.")
    
    df = Data_Process.DataFrame(filename)
    print(df)
    if not df.empty:
        dp = Data_Process()
        result = dp.AnalyzeDataWithSQL(df)
        print(result)

    else:
<<<<<<< HEAD
        print("No data available")
=======
        print("No data available")

    Plot_type = input("What type of visualization do you want? (Line/Bar/Scatter/Reg):")
    if Plot_type.lower() == "line":
        Data_Plot.plot_lineplot(df, xlabel, ylabel, title)
    elif Plot_type.lower() == "bar":
        Data_Plot.plot_barplot(df, xlabel, ylabel, title)
    elif Plot_type.lower() == "scatter":
        Data_Plot.plot_scatterplot(df, xlabel, ylabel, title)
    elif Plot_type.lower() == "reg":
        Data_Plot.plot_regplot(df, xlabel, ylabel, title)
    else:
        print("The wrong plot type was written.")
        

if __name__ == "__main__":
    Main()
>>>>>>> aa66e52f9c6d9424a74e6d5c418a7fdc6a49cb31
