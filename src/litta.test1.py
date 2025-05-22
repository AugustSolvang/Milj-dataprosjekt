import os
import webbrowser
import pandas as pd
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Category10

from Data_Process import Data_Process


def plot_bokeh_static(df, chart_type="line", output_filename="bokeh_output.html"):
    df = df.sort_values("Date").reset_index(drop=True)
    source = ColumnDataSource(df)

    plot = figure(
        x_axis_type="datetime", 
        width=800, 
        height=400, 
        title=f"Bokeh {chart_type.capitalize()} Plot"
    )

    if chart_type == "line":
        plot.line("Date", "Value", source=source, line_width=2, color=Category10[3][0])
    elif chart_type == "scatter":
        plot.circle("Date", "Value", source=source, size=8, color=Category10[3][1], alpha=0.6)
    elif chart_type == "bar":
        df["DateStr"] = df["Date"].dt.strftime("%Y-%m-%d")
        source = ColumnDataSource(df)
        plot.vbar(x="DateStr", top="Value", source=source, width=0.8, color=Category10[3][2])
    else:
        raise ValueError(f"Ugyldig chart_type: {chart_type}")

    output_file(output_filename)
    save(plot)
    print(f"Plot lagret som {output_filename}")
    webbrowser.open(f"file://{os.path.abspath(output_filename)}")


if __name__ == "__main__":
    print("✅ Kjører som testscript")
    try:
        df = Data_Process.DataFrame("rotte.json")
        plot_bokeh_static(df, chart_type="line", output_filename="bokeh_line.html")
        plot_bokeh_static(df, chart_type="scatter", output_filename="bokeh_scatter.html")
        plot_bokeh_static(df, chart_type="bar", output_filename="bokeh_bar.html")
        print("✅ Ferdig med å generere alle plots.")

    except Exception as e:
        print("🚨 Feil oppsto:")
        print(e)
