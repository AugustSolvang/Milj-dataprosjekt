import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_Key_MET")
url = os.getenv("MET_URL")


print(api_key)
print(url)

