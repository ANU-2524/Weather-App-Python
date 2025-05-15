import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

# Weather API Functions (similar to before)
def get_weather(city, api_key, units="metric"):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": units}
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}
    
    data = response.json()
    
    if response.status_code != 200:
        return {"error": data.get("message", "Error fetching weather")}
    
    return data

def get_forecast(city, api_key, units="metric"):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": units}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}
    
    data = response.json()
    if response.status_code != 200:
        return {"error": data.get("message", "Error fetching forecast")}
    
    return data

def unix_to_localtime(unix_time, tz_offset):
    return datetime.utcfromtimestamp(unix_time + tz_offset).strftime('%H:%M:%S')

# GUI App Class
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.api_key = "5e4ba7a06642956f63cb3e134815dbfa"  # Replace with your API key
        
        # City Input
        tk.Label(root, text="Enter City:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.city_var = tk.StringVar()
        tk.Entry(root, textvariable=self.city_var).grid(row=0, column=1, padx=5, pady=5)

        # Units dropdown
        tk.Label(root, text="Units:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.units_var = tk.StringVar(value="metric")
        units_combo = ttk.Combobox(root, textvariable=self.units_var, values=["metric", "imperial"], state="readonly")
        units_combo.grid(row=1, column=1, padx=5, pady=5)
        units_combo.set("metric")  # default Celsius

        # Search Button
        tk.Button(root, text="Get Weather", command=self.fetch_weather).grid(row=2, column=0, columnspan=2, pady=10)

        # Output Text
        self.output = tk.Text(root, width=50, height=15, state='disabled')
        self.output.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def fetch_weather(self):
        city = self.city_var.get().strip()
        units = self.units_var.get()
        
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        
        self.output.configure(state='normal')
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Fetching weather for {city}...\n")
        self.output.configure(state='disabled')
        self.root.update()

        weather = get_weather(city, self.api_key, units)
        if "error" in weather:
            messagebox.showerror("Error", weather["error"])
            return
        
        forecast = get_forecast(city, self.api_key, units)
        if "error" in forecast:
            messagebox.showwarning("Warning", f"Could not fetch forecast: {forecast['error']}")

        self.display_weather(weather, forecast, units)

    def display_weather(self, weather, forecast, units):
        self.output.configure(state='normal')
        self.output.delete(1.0, tk.END)

        city = weather['name']
        tz_offset = weather['timezone']

        temp_unit = "°C" if units == "metric" else "°F"

        self.output.insert(tk.END, f"🌤️ Weather in {city}\n")
        self.output.insert(tk.END, f"Temperature: {weather['main']['temp']}{temp_unit}\n")
        self.output.insert(tk.END, f"Feels like: {weather['main']['feels_like']}{temp_unit}\n")
        self.output.insert(tk.END, f"Description: {weather['weather'][0]['description'].title()}\n")
        self.output.insert(tk.END, f"Humidity: {weather['main']['humidity']}%\n")
        self.output.insert(tk.END, f"Wind Speed: {weather['wind']['speed']} m/s\n")
        self.output.insert(tk.END, f"Sunrise: {unix_to_localtime(weather['sys']['sunrise'], tz_offset)}\n")
        self.output.insert(tk.END, f"Sunset: {unix_to_localtime(weather['sys']['sunset'], tz_offset)}\n\n")

        if forecast and "list" in forecast:
            self.output.insert(tk.END, "📅 5-day Forecast (3-hour intervals):\n")
            for entry in forecast['list'][:8]:
                time_txt = entry['dt_txt']
                temp = entry['main']['temp']
                desc = entry['weather'][0]['description'].title()
                self.output.insert(tk.END, f"{time_txt}: {temp}{temp_unit}, {desc}\n")
        
        self.output.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
