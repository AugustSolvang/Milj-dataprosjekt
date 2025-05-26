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
    def plot_barplot(df, xlabel, ylabel, title):
        sns.barplot(data=df, x=xlabel, y=ylabel)  # plots a bar chart
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()
