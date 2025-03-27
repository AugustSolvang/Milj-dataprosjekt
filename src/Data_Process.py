import matplotlib.pyplot as plt
import json
import pandas
import numpy

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


    def DataFrame(json):
        

        
