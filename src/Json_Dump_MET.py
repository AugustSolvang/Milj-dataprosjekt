# Load environment variables from a .env file
from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import date
import json

# Function to fetch data from the MET API and save it to a local JSON file
def fetch_data(Filename, Api_Key, Url, Sources, Elements, Reference_Time):
    # Construct the full endpoint URL with query parameters
    Endpoint = f"{Url}?sources={Sources}&elements={Elements}&referencetime={Reference_Time}"
    
    # Send a GET request to the API with basic authentication
    res = requests.get(Endpoint, auth = (Api_Key, ""))

    # If the request is successful (HTTP 200 OK)
    if res.status_code == 200:
        data = res.json()  # Parse the JSON response
        with open(Filename, "a") as f:
            json.dump(data, f, indent = 4)  # Append the data to the file in JSON format
        print(Endpoint)  # Print the URL used (for debugging or reference)
    else:
        # If the request fails, print the error status
        print("Error")
        print(res.status_code)

# Load environment variables (such as API keys and URLs) from .env file
load_dotenv()

# Set variables used for the API request
Filename = "Precipitation_Sum_Anomaly_1961-1990.json"
Api_Key = os.getenv("API_Key_MET")  # Fetch API key from environment
Url = os.getenv("Base_MET_URL")     # Fetch base URL from environment
Sources = "SN18700"                 # MET station ID
Elements = "best_estimate_sum(precipitation_amount_anomaly P1M 1961_1990)"  # Requested data element
Reference_Time = "1940-01-01/2025-01-01"  # Time period for the data

# Call the function to fetch and save the data
fetch_data(Filename, Api_Key, Url, Sources, Elements, Reference_Time)

