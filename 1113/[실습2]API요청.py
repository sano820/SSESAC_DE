import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("weather_api_key")

import requests

base_url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    'q' : 'Seoul',
    'appid' : api_key, # 각자의 API Key 값
}

response = requests.get(base_url, params=params)
if response.status_code == 200: # 요청에 성공했으면 
    data = response.json() # 응답 바디 가져오기
    print(json.dumps(data, ensure_ascii=False, indent =4))
    
    lon = data["coord"].get("lon","N/A")
    lat = data["coord"].get("lon","N/A")
    weather = data["weather"].get("description", "N/A")
    wid_speed = data["wind"].get("speed", "N/A")
    clouds = data["clouds"].get("all", "N/A")
