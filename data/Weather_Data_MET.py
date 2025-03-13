import requests
import json

api_key = "2e53c5fc-1cab-435f-bf3d-5b1cd9352d86"
url = "https://frost.met.no/observations/v0.jsonld"

headers = {
    "Authorization": f"Bearer {api_key}"
}

params = {
    "station": "Oslo",
    "start": "2020-01-01",
    "end": "2020-12-31"
}

response = requests.get(url, headers=headers, params=params, auth=(api_key, ""))

if response.status_code == 200:
    data = response.json()

    with open('Weather_Data_MET.json', 'a') as json_file:
        json.dump(data, json_file, indent=4)

else:
    print("Error")
    print(response.url)
