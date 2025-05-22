from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, ColorPicker, ColumnDataSource, Div, Button, Spinner
from bokeh.plotting import figure
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from pandasql import sqldf
import json
import os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandasql import sqldf
import json
import csv
from Data_Process import Data_Process


FILENAME = "Air_Quality.csv"  # <-- Put your file here
df_raw = Data_Process.DataFrame(os.path.join("data", FILENAME))  # Reads and cleans data

# These are the widgets (User controls)
stat_select = Select(
    title="Statistikk",
    value="Avg",
    options=["Avg", "Min", "Max", "Median"]
)
plot_type_select = Select(
    title="Plottype",
    value="Lineplot",
    options=["Lineplot", "Barplot", "Scatterplot"]
)
color_picker = ColorPicker(title="Farge", color="#1f77b4")
future_slider = Spinner(title="Fremtid (år):", low=0, high=50, step=1, value=5)
regression_button = Button(label="Kjør regresjon", button_type="success")
status_text = Div(text=f"Filen '{FILENAME}' er lastet inn.")

# There are for the sources and plot
source = ColumnDataSource(data=dict(x=[], y=[]))               # Dataset for main plot
regression_source = ColumnDataSource(data=dict(x=[], y=[]))   # Dataset for prediction plot

plot = figure(title="Dataoversikt", x_axis_label="År", y_axis_label="Verdi")
prediction_plot = figure(title="Prediksjon", x_axis_label="År", y_axis_label="Verdi")


def update_plot():
    """
    Updates main plot based on chosen statistics and plot type
    """
    df_summary = Data_Process.AnalyzeDataWithSQL(df_raw)
    y_field = stat_select.value + "Value"
    x = df_summary["Year"]
    y = df_summary[y_field]
    source.data = dict(x=x, y=y)

    # Remove existing plot
    plot.renderers = []

    # Draw chosen plot type
    if plot_type_select.value == "Lineplot":
        plot.line(x='x', y='y', source=source,
                  color=color_picker.color, line_width=2)
    elif plot_type_select.value == "Barplot":
        plot.vbar(x='x', top='y', source=source,
                  width=0.7, color=color_picker.color)
    elif plot_type_select.value == "Scatterplot":
        plot.circle(x='x', y='y', source=source,
                    size=8, color=color_picker.color)


def run_regression():
    """
    Initialises regression and updates the prediction plot
    """
    df_summary = Data_Process.AnalyzeDataWithSQL(df_raw)
    y_field = stat_select.value + "Value"

    if df_summary.empty or y_field not in df_summary:
        status_text.text = "Ingen data tilgjengelig for regresjon."
        regression_source.data = dict(x=[], y=[])
        prediction_plot.renderers = []
        return

    # Runs regression
    x_pred, y_pred, _, _ = Data_Process.Linear_Regression(
        df_summary,
        "Year",
        y_field,
        future_steps=future_slider.value
    )

    regression_source.data = dict(x=x_pred, y=y_pred)

    prediction_plot.renderers = []
    prediction_plot.line(x='x', y='y', source=regression_source,
                         line_width=2, line_color="firebrick")
    status_text.text = f"Regresjon kjørt med {future_slider.value} år frem i tid."


# Associates the update functions with interactive elements
stat_select.on_change("value", lambda attr, old, new: update_plot())
plot_type_select.on_change("value", lambda attr, old, new: update_plot())
color_picker.on_change("color", lambda attr, old, new: update_plot())
regression_button.on_click(run_regression)

# Organizes layout in two columns
left_column = column(stat_select, plot_type_select, color_picker, plot)
right_column = column(future_slider, regression_button, prediction_plot)

layout = column(
    row(left_column, right_column),
    status_text
)

# Adds the layout for the Bokeh-document
curdoc().add_root(layout)
curdoc().title = "Interaktiv App m/ Regresjon"


# Run first update after the server is ready
def server_ready():
    update_plot()


curdoc().on_event('document_ready', lambda event: server_ready())

# To run the program:
# bokeh serve src/Interactive_Plot.py --show --port 5006
