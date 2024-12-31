# Technical Test QA Automation ADL Indonesia
# Name : Mega Kristina Marbun

import requests
import time
from jsonschema import validate

BASE_URL = "https://api.openweathermap.org/data/2.5"
API_KEY = "ae7c2ef04770563b21e876654ad8344c"

def test_get_5_day_forecast():
    """Test 5-day weather forecast for Jakarta"""
    params = {
        "q": "Jakarta,ID",  # Nama kota (Jakarta, tanpa 'Selatan', OpenWeather menggunakan nama kota utama seperti Jakarta tanpa menambahkan Selatan.)
        "appid": API_KEY,   
        "units": "metric"  
    }
    response = requests.get(f"{BASE_URL}/forecast", params=params)

    # 1. Periksa Status Code
    assert response.status_code == 200, f"Response code bukan 200, tapi {response.status_code}"

    # 2. Validasi JSON Schema
    forecast_schema = {
        "type": "object",
        "properties": {
            "list": {"type": "array"},
            "city": {"type": "object"},
        },
        "required": ["list", "city"]
    }
    validate(instance=response.json(), schema=forecast_schema)

    # 3. Periksa atribut 
    data = response.json()
    assert data["city"]["name"].lower() == "jakarta", "Nama kota tidak sesuai"
    assert len(data["list"]) > 0, "Data prakiraan kosong"

    
    time.sleep(2)

def test_get_current_air_pollution():
    """Test current air pollution for Jakarta Selatan"""
    params = {
        "lat": -6.29,  # Latitude Jakarta Selatan
        "lon": 106.82, # Longitude Jakarta Selatan
        "appid": API_KEY
    }
    response = requests.get(f"{BASE_URL}/air_pollution", params=params)

    # 1. Periksa Status Code
    assert response.status_code == 200, f"Response code bukan 200, tapi {response.status_code}"

    # 2. Validasi JSON Schema
    air_pollution_schema = {
        "type": "object",
        "properties": {
            "coord": {"type": "object"},
            "list": {"type": "array"}
        },
        "required": ["coord", "list"]
    }
    validate(instance=response.json(), schema=air_pollution_schema)

    # 3. Periksa atribut 
    data = response.json()
    assert len(data["list"]) > 0, "Data polusi udara kosong"

    
    time.sleep(2)
