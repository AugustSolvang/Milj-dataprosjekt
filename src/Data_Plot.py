from Data_Process import Data_Process
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Data_Plot:

    @staticmethod
    def plot_lineplot(df, xlabel, ylabel, title):
        sns.lineplot(data = df, x = xlabel, y = ylabel)
        
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_regplot(df, xlabel, ylabel, title):
        sns.regplot(data = df, x = xlabel, y = ylabel)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()



