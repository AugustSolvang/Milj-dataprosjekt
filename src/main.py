# Import necessary modules and custom classes for data processing and plotting
import pandas as pd
from Data_Process import Data_Process
from Data_Plot import Data_Plot
import json
import os

# Function for generating a simple static plot based on user input
def Simple_Plot():
    # Ask the user which dataset they want to visualize
    Data_type = input("What data do you want to visualize? (Air temperature/Precipitation):")
    xlabel = "Date"
    
    # Set file name, y-axis label and plot title based on data type
    if Data_type.lower() == "air temperature":
        filename = os.path.join("data", "Air_Temp_Anomaly_1961-1990.json")
        ylabel = "Value"
        title = "Homogenized mean air temperature for the period 1961-1990 (degC)"
    elif Data_type.lower() == "precipitation":
        filename = os.path.join("data", "Precipitation_Sum_Anomaly_1961-1990.json")
        ylabel = "Value"
        title = "Homogenized mean precipitation sum for the period 1961-1990 (percent)"
    else:
        print("The wrong data type was written.")
    
    # Read and clean the data using the custom Data_Process class
    df = Data_Process.DataFrame(filename)
    print(df)  # Print raw data for debugging

    # If the DataFrame is not empty, perform analysis using SQL-like queries
    if not df.empty:
        dp = Data_Process()
        result = dp.AnalyzeDataWithSQL(df)
        print(result)  # Print summary results
    else:
        print("No data available")

    # Ask the user for the type of plot to create
    Plot_type = input("What type of visualization do you want? (Line/Bar/Scatter):")
    
    # Plot based on the chosen type using the custom Data_Plot class
    if Plot_type.lower() == "line":
        Data_Plot.plot_lineplot(df, xlabel, ylabel, title)
    elif Plot_type.lower() == "bar":
        Data_Plot.plot_barplot(df, xlabel, ylabel, title)
    elif Plot_type.lower() == "scatter":
        Data_Plot.plot_scatterplot(df, xlabel, ylabel, title)
    else:
        print("The wrong plot type was written.")

# Entry point when the script is run directly
if __name__ == "__main__":
    # Ask the user if they want an interactive or static plot
    Interactive = input("Do you want a interactive plot? (Yes/No):")
    if Interactive.lower() == "yes":
        # Instructions for running the interactive Bokeh app
        print("Change 'FILENAME' in 'Interactive_Plot.py' to the desired data type and save")
        print("Type this 'bokeh serve src/Interactive_Plot.py --show --port 5006' in the PowerShell Terminal")
        print("For each time you run the code in the terminal you need to change the '5006'")
    elif Interactive.lower() == "no":
        # Run the static plotting function
        Simple_Plot()
    else:
        print("The wrong input was given.")


