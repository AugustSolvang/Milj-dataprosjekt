from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
import seaborn as sns
import matplotlib.pyplot as plt
from Data_Process import Data_Process


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
    def Plot_Regression(df, x_col, y_col, x_pred, y_pred, is_date=False):
        """
        Plot data points and linear regression line.

        Parameters:
        - df: original dataframe with data points
        - x_col: name of x column in df
        - y_col: name of y column in df
        - x_pred: predicted x values from Linear_Regression
        - y_pred: predicted y values from Linear_Regression
        - is_date: bool, whether x values are dates
        """
        plt.figure(figsize=(10, 6))

        # Plot original data points
        plt.scatter(df[x_col], df[y_col], color='blue', label='Data points')

        # Plot regression line
        plt.plot(x_pred, y_pred, color='red', label='Linear regression')

        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'Linear Regression of {y_col} vs {x_col}')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def PlotData(df):
        """Plots the average of the data per year using a moving average."""
        result_df = Data_Process.AnalyzeDataWithSQL(df)
        if result_df.empty:
            print("No data to plot.")
            return

        result_df['Smoothed'] = result_df['AvgValue'].rolling(window=2).mean()

        plt.figure(figsize=(10, 6))
        plt.plot(result_df["Year"], result_df["AvgValue"], marker='o', label="Avg Value per Year")
        plt.plot(result_df["Year"], result_df["Smoothed"], color="red", label="Smoothed (Moving Avg)")
        plt.xlabel("Year")
        plt.ylabel("Avg Value")
        plt.title("Smoothed Average Value per Year with Moving Average")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()