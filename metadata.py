import requests
from datetime import datetime

from config import GOOGLE_MAPS_API_KEY, WEATHER_API_KEY

def calc_time_of_day(lat, lng):
    timestamp = int(datetime.now().timestamp())
    params = {
        'location': f'{lat},{lng}',
        'timestamp': timestamp,
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get('https://maps.googleapis.com/maps/api/timezone/json', params=params)
    data = response.json()

    dst_offset = data.get('dstOffset', 0)
    raw_offset = data.get('rawOffset', 0)

    local_time = datetime.fromtimestamp(timestamp + dst_offset + raw_offset)
    
    if 5 <= local_time.hour < 12:
        return 'morning'
    elif 12 <= local_time.hour < 18:
        return 'afternoon'
    elif 18 <= local_time.hour < 21:
        return 'evening'
    else:
        return 'night'
    
def weather(lat, lng):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    
    if weather_data['cod'] == 200:
        weather_main = weather_data['weather'][0]['main'].lower()  # e.g., "rain", "clear"
        weather_desc = weather_data['weather'][0]['description'].lower()  # e.g., "light rain"
        temp = weather_data['main']['temp']  # in Celsius
        return weather_main, weather_desc, temp
    else:
        print(f"Weather API error: {weather_data['message']}")
        return None, None, None

def find_place(name, near_location=None, radius=50000):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': name,
        'key': GOOGLE_MAPS_API_KEY
    }
    
    if near_location:
        params['location'] = f"{near_location['lat']},{near_location['lng']}"
        params['radius'] = radius

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK' and len(data['results']) > 0:
        place = data['results'][0]
        return place['geometry']['location'], place['name']
    else:
        print(f"Google Places API error: {data['status']}")
        return None, None

def decide_mode(distance, time_of_day):
    if distance < 2:  
        return 'walking'
    if distance<5:
        return 'biking'
    elif time_of_day in ['morning', 'evening']:  
        return 'transit'
    else:
        return 'driving'