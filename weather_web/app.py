from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = "5e4ba7a06642956f63cb3e134815dbfa"  # Replace with your OpenWeatherMap API key

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city.title(),
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "feels_like": data["main"]["feels_like"],
            "wind": data["wind"]["speed"]
        }
    else:
        return None

def get_forecast(city, units="metric"):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": units}
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        if res.status_code != 200:
            return None
        return data
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        weather = get_weather(city)
        if not weather:
            error = "City not found or invalid API key."
    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)