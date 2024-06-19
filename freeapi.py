import requests
import csv
from datetime import datetime, timedelta

# Replace with your API key
API_KEY = " 56cdd10fcb5c468cbb4193934241803"

# Set the location and date range for historic weather data
location = "Patna"
start_date = datetime(2024, 6, 13)  # Start date (YYYY, MM, DD)
end_date = datetime(2024, 6, 19)   # End date (YYYY, MM, DD)

# Set the base URL and parameters for the API request
base_url = "http://api.weatherapi.com/v1/history.json"
params = {
    "key": API_KEY,
    "q": location,
    "dt": start_date.strftime("%Y-%m-%d")
}

# Initialize an empty list to store weather data
weather_data = []

# Loop through the date range and fetch weather data for each day
current_date = start_date
while current_date <= end_date:
    params["dt"] = current_date.strftime("%Y-%m-%d")
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for forecast in data["forecast"]["forecastday"]:
            for hour in forecast["hour"]:
                weather_data.append({
                    "Date": hour["time"].split(" ")[0],
                    "Time": hour["time"].split(" ")[1],
                    "Temperature (C)": hour["temp_c"],
                    "Humidity": hour["humidity"],
                    "Wind Speed (km/h)": hour["wind_kph"],
                    "Precipitation (mm)": hour["precip_mm"]
                })
    else:
        print(f"Error fetching data for {current_date}: {response.status_code} - {response.text}")
    
    current_date += timedelta(days=1)

# Save weather data to a CSV file
with open("historic_weather_data.csv", "w", newline="") as csvfile:
    fieldnames = ["Date", "Time", "Temperature (C)", "Humidity", "Wind Speed (km/h)", "Precipitation (mm)"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for data in weather_data:
        writer.writerow(data)

print("Historic weather data saved to historic_weather_data.csv")