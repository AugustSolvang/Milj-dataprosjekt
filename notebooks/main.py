from fetch_data import fetch_weather_data, save_json
from analyze_data import load_data, analyze_temperature

# Hent værdata
data = fetch_weather_data(59.91, 10.75)  # Oslo koordinater
save_json(data)

# Analyser dataene
df = load_data()
filtered_data = analyze_temperature(df)
print(filtered_data)

