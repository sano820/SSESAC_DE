import requests
import pandas as pd
from dotenv import load_dotenv
import os, json

load_dotenv()
api_key = os.getenv("weather_api_key")

import requests

base_url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    'q' : 'Seoul',
    'appid' : api_key, # 각자의 API Key 값
}

response = requests.get(base_url, params=params)
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, ensure_ascii=False, indent=4))

    # 필요한 데이터 추출
    lon = data["coord"].get("lon", "N/A")
    lat = data["coord"].get("lat", "N/A")
    weather_main = data["weather"][0].get("main", "N/A")
    weather_desc = data["weather"][0].get("description", "N/A")
    temp = data["main"].get("temp", "N/A")
    feels_like = data["main"].get("feels_like", "N/A")
    humidity = data["main"].get("humidity", "N/A")
    wind_speed = data["wind"].get("speed", "N/A")
    clouds = data["clouds"].get("all", "N/A")
    country = data["sys"].get("country", "N/A")
    city = data.get("name", "N/A")

    # DataFrame 생성
    df = pd.DataFrame([{
        "city": city,
        "country": country,
        "lon": lon,
        "lat": lat,
        "weather_main": weather_main,
        "weather_desc": weather_desc,
        "temp(K)": temp,
        "feels_like(K)": feels_like,
        "humidity(%)": humidity,
        "wind_speed(m/s)": wind_speed,
        "clouds(%)": clouds
    }])

    # CSV로 저장
    df.to_csv("./1113/outputs/weather_seoul.csv", index=False, encoding="utf-8-sig")
else:
    print("API 요청 실패:", response.status_code)
