from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
import seaborn as sns
import matplotlib.pyplot as plt


# various functions for plotting graphs
class Data_Plot:

    @staticmethod
    def plot_lineplot(df, xlabel, ylabel, title):
        sns.lineplot(data=df, x=xlabel, y=ylabel)  # plots a line chart
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_scatterplot(df, xlabel, ylabel, title):
        sns.scatterplot(data=df, x=xlabel, y=ylabel)  # plots a scatter chart
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_regplot(df, xlabel, ylabel, title):
        sns.regplot(data=df, x=xlabel, y=ylabel)  # plots scatter with regression line
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_barplot(df, xlabel, ylabel, title):
        sns.barplot(data=df, x=xlabel, y=ylabel)  # plots a bar chart
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_bokeh(df, xlabel, ylabel, title, chart_type="line", output_filename="bokeh_plot.html"):
        """Takes in a dataframe and chart type and returns a link with interactive graphs"""

        chart_type = chart_type.lower()

        # Sjekk at kolonner finnes i df
        if xlabel not in df.columns:
            raise ValueError(f"Missing x column: '{xlabel}'")
        if ylabel not in df.columns:
            raise ValueError(f"Missing y column: '{ylabel}'")

        output_file(output_filename)
        source = ColumnDataSource(df)

        p = figure(
            title=title,
            x_axis_label=xlabel,
            y_axis_label=ylabel,
            width=700,
            height=400,
            tools="pan,wheel_zoom,box_zoom,reset,save",
        )

        if chart_type == "line":
            p.line(x=xlabel, y=ylabel, source=source, line_width=2, legend_label=ylabel)
            p.circle(x=xlabel, y=ylabel, source=source, size=6, color="navy", alpha=0.5)
        elif chart_type == "scatter":
            p.circle(x=xlabel, y=ylabel, source=source, size=8, color="green", alpha=0.6, legend_label=ylabel)
        elif chart_type == "bar":
            # Barplot requires x to be strings (categories)
            df[xlabel] = df[xlabel].astype(str)
            source = ColumnDataSource(df)
            p.vbar(x=xlabel, top=ylabel, source=source, width=0.7, legend_label=ylabel)
        else:
            raise ValueError(f"Invalid chart_type: '{chart_type}'. Use 'line', 'scatter' or 'bar'.")

        p.legend.location = "top_left"
        save(p)
