import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
api_key = os.getenv('API_KEY')
database_url = os.getenv('DATABASE_URL')

city = 'Oslo'

api_key = os.getenv('API_KEY')
url = os.getenv('DATABASE_URL')

url +=f"?q={city}&appid={api_key}&units=metric"

res = requests.get(url)
data = res.json()

humidity = data['main']['humidity']
pressure = data['main']['pressure']
wind = data['wind']['speed']
description = data['weather'][0]['description']
temp = data['main']['temp']

print('Temperature:',temp,'°C')
print('Wind:',wind)
print('Pressure: ',pressure)
print('Humidity: ',humidity)
print('Description:',description)

