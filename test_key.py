import requests

api_key = "5e4ba7a06642956f63cb3e134815dbfa"  # replace this
city = "Delhi"

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
print(response.status_code)
print(response.json())
