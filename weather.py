import requests
from datetime import datetime
import time
import tkinter as tk
from tkinter import ttk, messagebox

def get_weather(city, api_key, units="metric"):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": units}
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad status
    except requests.exceptions.RequestException as e:
        print(f"\n⚠️ Network error or invalid request: {e}")
        return None
    
    data = response.json()
    
    if response.status_code != 200:
        print(f"\n⚠️ Error: {data.get('message', 'Unknown error')}")
        return None
    
    return data

def get_forecast(city, api_key, units="metric"):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": units}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\n⚠️ Forecast fetch error: {e}")
        return None
    
    data = response.json()
    if response.status_code != 200:
        print(f"\n⚠️ Error fetching forecast: {data.get('message', 'Unknown error')}")
        return None
    
    return data

def unix_to_localtime(unix_time, tz_offset):
    return datetime.utcfromtimestamp(unix_time + tz_offset).strftime('%H:%M:%S')

def print_weather(data, units):
    city = data['name']
    tz_offset = data['timezone']
    print(f"\n🌤️ Weather in {city}")
    print(f"Temperature: {data['main']['temp']}°{'C' if units == 'metric' else 'F'}")
    print(f"Feels like: {data['main']['feels_like']}°{'C' if units == 'metric' else 'F'}")
    print(f"Description: {data['weather'][0]['description'].title()}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")
    print(f"Sunrise: {unix_to_localtime(data['sys']['sunrise'], tz_offset)}")
    print(f"Sunset: {unix_to_localtime(data['sys']['sunset'], tz_offset)}")

def print_forecast(data, units):
    print("\n📅 5-day Forecast (3-hour intervals):")
    for entry in data['list'][:8]:  # First 8 entries (~24 hours)
        time_txt = entry['dt_txt']
        temp = entry['main']['temp']
        desc = entry['weather'][0]['description'].title()
        print(f"{time_txt}: {temp}°{'C' if units == 'metric' else 'F'}, {desc}")

def main():
    api_key = "5e4ba7a06642956f63cb3e134815dbfa"  # Replace with your real API key
    city = input("Enter city name: ").strip()
    unit_choice = input("Choose units - Celsius (C) or Fahrenheit (F) [Default C]: ").strip().upper()
    units = "imperial" if unit_choice == "F" else "metric"

    weather_data = get_weather(city, api_key, units)
    if weather_data:
        print_weather(weather_data, units)
        
        forecast_data = get_forecast(city, api_key, units)
        if forecast_data:
            print_forecast(forecast_data, units)

if __name__ == "__main__":
    main()
