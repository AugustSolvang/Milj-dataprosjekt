from Data_Process import Data_Process
import pandas
import matplotlib.pyplot as plt

class Data_Plot:
    def plot(df, x_col, y_col, x_label, y_label):
        x_values = df.columns[0]
        y_values = df.columns[1]
        plt.plot(x_values, y_values)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.show()
    
    def 
