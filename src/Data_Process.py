import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np

class Data_Process:

    def DataDict(Filename):
        if Filename.endswith(".json"):
            with open(Filename, "r") as readfile:
                data = json.load(readfile)
                DataDict = {}

                for observation in data.get("data", []):
                    Date = observation["referenceTime"][:10]
                    Value = observation["observations"][0]["value"]

                    if Date not in DataDict:
                        DataDict[Date] = []
                    DataDict[Date].append(Value)
                return DataDict
            
        else:
            print("Ikke en json fil")


    def DataFrame(Filename):
        DataDict = DataDict(Filename)
        DataList = [[Date, Value] for Date, Value in DataDict.items()]
        df = pd.DataFrame(DataList, columns = ["Date", "Anomoly [°C]"])
        return df
    
    