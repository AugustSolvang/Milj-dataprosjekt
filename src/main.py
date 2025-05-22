import pandas as pd
from Data_Process import Data_Process
from Data_Plot import Data_Plot

data = pd.read_csv("data/Air_Quality.csv")

df = Data_Process.DataFrame(data)
print("DataFrame:\n", df)

if not df.empty:
    result_df = Data_Process.AnalyzeDataWithSQL(df)
    print("Avg/Min/Max Values (SQL):\n", result_df)


if not df.empty:
    Data_Process.PlotData(df)



def Main():
    
    xlabel = "Dato"
    Data_Type = input("Hvilken type data vil du plotte? (Luftkvalitet/ Temperatur/ Nedbør):")

    if Data_Type.lower() == "luftkvalitet":
        data = "Air_Quality.csv"
        ylabel = "NO µg/m³"
        title = "Historisk luftkvalitetsdata (måned)"
    elif Data_Type.lower() == "temperatur":
        data = "Air_Temp_Anomaly_1961-1990.json"
        ylabel = "degC"
        title = "Homogenisert månedsmiddel for temperatur."
    elif Data_Type.lower() == "nedbør":
        data = "Precipitation_Sum_Anomaly_1961-1990.json"
        ylabel = "percent"
        title = "Homogenisert månedssum for nedbør"
    else:
        data = ""
        print("Det er gitt feil input til Data_Type")

    if not data == "":
        df = Data_Process.DataFrame(data)
        
        Regression = input("Vil du foutsi hvordan dataen vil se ut i fremtiden? (Ja/ Nei):")
        
        if Regression.lower() == "ja":
            Future_Steps = int(input("Hvor mange dager inn i fremtiden ønsker du å forutsi?:"))
            df = Data_Process.Linear_Regression(df, "date", "value", Future_Steps)
        elif Regression.lower() == "nei":
            None
        else:
            print("Det er feil input for Regression")
        
        Bokeh = input("Vil du ha et interaktivt plot på en nettside? (Ja/ Nei):")

        if Bokeh.lower() == "ja":
            Plot_Type = input("Hva slags type plot vil du ha? (Linje/ Punkt/ Søyle):")
            Data_Plot.plot_bokeh(df, xlabel, ylabel, title, Plot_Type, "bokeh_plot.html")
        elif Bokeh.lower() == "nei":
            Plot_Type = input("Hva slags type plot vil du ha? (Linje/ Punkt/ Søyle/ Reg):")
            if Plot_Type.lower() == "linje":
                Data_Plot.plot_lineplot(df, xlabel, ylabel, title)
            elif Plot_Type.lower() == "punkt":
                Data_Plot.plot_scatterplot(df, xlabel, ylabel, title)
            elif Plot_Type.lower() == "søyle":
                Data_Plot.plot_barplot(df, xlabel, ylabel, title)
            elif Plot_Type.lower() == "reg":
                Data_Plot.plot_regplot(df, xlabel, ylabel, title)
            else:
                print("Feil input til Plot_Type")
        else:
            print("Det er feil input til Bokeh")

Main()

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