from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, ColorPicker, ColumnDataSource, Div, Button, Spinner
from bokeh.plotting import figure
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from pandasql import sqldf
import json

# ------------------ DATAPROSESSERING ------------------

class Interaktiv_Visualisering:

    @staticmethod
    def DataDict(Filename):
        if Filename.endswith(".json"):
            data_list = []
            with open(Filename, "r") as readfile:
                data = json.load(readfile)
                for observation in data.get("data", []):
                    date = observation["referenceTime"][:10]
                    value = observation["observations"][0].get("value", None)
                    if value is not None:
                        data_list.append((date, value))

            df = pd.DataFrame(data_list, columns=["Date", "Value"])
            df["Date"] = pd.to_datetime(df["Date"])
            df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
            df = df.dropna(subset=["Date", "Value"])
            df = df[df["Value"] >= 0]
            return df

        elif Filename.endswith(".csv"):
            try:
                df = pd.read_csv(
                    Filename,
                    sep=";",
                    encoding="utf-8",
                    decimal=",",
                    names=["Date", "Value", "Coverage"],
                    na_values=[""],
                )
                df.columns = ["Date", "Value", "Coverage"]
            except Exception as e:
                print(f"Error reading CSV: {e}")
                return pd.DataFrame()

            df = df.dropna(subset=["Value", "Coverage"], how="all")
            df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y %H:%M", errors='coerce', dayfirst=True)
            df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
            df = df.dropna(subset=["Date", "Value"])
            df = df[df["Value"] >= 0]
            return df
        else:
            print("Not a supported file format.")
            return pd.DataFrame()

    @staticmethod
    def AnalyzeDataWithSQL(df):
        if df.empty:
            print("No dataframe to be found")
            return pd.DataFrame()

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
    def Linear_Regression(df, x_col, y_col, future_steps=0, n_points=100):
        df = df.copy()
        if pd.api.types.is_datetime64_any_dtype(df[x_col]):
            df["x_num"] = df[x_col].map(pd.Timestamp.toordinal)
            is_date = True
        else:
            df["x_num"] = pd.to_numeric(df[x_col], errors='coerce')
            is_date = False

        df = df.dropna(subset=["x_num", y_col])
        X = df[["x_num"]]
        y = df[y_col]
        model = LinearRegression()
        model.fit(X, y)

        x_min = df["x_num"].min()
        x_max = df["x_num"].max() + future_steps
        x_pred_num = np.linspace(x_min, x_max, n_points).reshape(-1, 1)
        y_pred = model.predict(x_pred_num)

        if is_date:
            x_pred = [pd.to_datetime(pd.Timestamp.fromordinal(int(x))) for x in x_pred_num.flatten()]
        else:
            x_pred = x_pred_num.flatten()

        return x_pred, y_pred, model, is_date

# ------------------ INITIALISERING ------------------

FILENAME = "rotte.json"  # <-- Endre til din fil
df_raw = Interaktiv_Visualisering.DataDict(FILENAME)

# Kontroll-elementer
stat_select = Select(title="Statistikk", value="Avg", options=["Avg", "Min", "Max", "Median"])
plot_type_select = Select(title="Plottype", value="Lineplot", options=["Lineplot", "Barplot", "Scatterplot"])
color_picker = ColorPicker(title="Farge", color="#1f77b4")
future_slider = Spinner(title="Fremtid (år):", low=0, high=50, step=1, value=5)
regression_button = Button(label="Kjør regresjon", button_type="success")
status_text = Div(text=f"Filen '{FILENAME}' er lastet inn.")

# Kilder og plott
source = ColumnDataSource(data=dict(x=[], y=[]))
regression_source = ColumnDataSource(data=dict(x=[], y=[]))
plot = figure(title="Dataoversikt", x_axis_label="År", y_axis_label="Verdi")
prediction_plot = figure(title="Prediksjon", x_axis_label="År", y_axis_label="Verdi")

# ------------------ FUNKSJONER ------------------

def update_plot():
    df_summary = Interaktiv_Visualisering.AnalyzeDataWithSQL(df_raw)
    y_field = stat_select.value + "Value"
    x = df_summary["Year"]
    y = df_summary[y_field]
    source.data = dict(x=x, y=y)

    plot.renderers = []
    if plot_type_select.value == "Lineplot":
        plot.line(x='x', y='y', source=source, color=color_picker.color, line_width=2)
    elif plot_type_select.value == "Barplot":
        plot.vbar(x='x', top='y', source=source, width=0.7, color=color_picker.color)
    elif plot_type_select.value == "Scatterplot":
        plot.circle(x='x', y='y', source=source, size=8, color=color_picker.color)

def run_regression():
    df_summary = Interaktiv_Visualisering.AnalyzeDataWithSQL(df_raw)
    y_field = stat_select.value + "Value"

    if df_summary.empty or y_field not in df_summary:
        status_text.text = "Ingen data tilgjengelig for regresjon."
        regression_source.data = dict(x=[], y=[])
        prediction_plot.renderers = []
        return

    x_pred, y_pred, _, _ = Interaktiv_Visualisering.Linear_Regression(
        df_summary,
        "Year",
        y_field,
        future_steps=future_slider.value
    )

    regression_source.data = dict(x=x_pred, y=y_pred)

    prediction_plot.renderers = []
    prediction_plot.line(x='x', y='y', source=regression_source, line_width=2, line_color="firebrick")
    status_text.text = f"Regresjon kjørt med {future_slider.value} år frem i tid."

# ------------------ CALLBACKS ------------------

stat_select.on_change("value", lambda attr, old, new: update_plot())
plot_type_select.on_change("value", lambda attr, old, new: update_plot())
color_picker.on_change("color", lambda attr, old, new: update_plot())
regression_button.on_click(run_regression)

# ------------------ LAYOUT ------------------

left_column = column(stat_select, plot_type_select, color_picker, plot)
right_column = column(future_slider, regression_button, prediction_plot)

layout = column(
    row(left_column, right_column),
    status_text
)

curdoc().add_root(layout)
curdoc().title = "Interaktiv App m/ Regresjon"

# Kjør update_plot() etter at Bokeh har initialisert komponentene
def server_ready():
    update_plot()

curdoc().on_event('document_ready', lambda event: server_ready())

#Kjør koden i terminal: bokeh serve src/interaktiv_app.py --show --port 5006
